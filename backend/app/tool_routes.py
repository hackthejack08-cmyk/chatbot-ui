import csv
import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from backend.app.rag import save_uploaded_chunks


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

UPLOAD_FOLDER = BACKEND_ROOT / "storage" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LOCAL_WHISPER_MODEL = os.getenv("LOCAL_WHISPER_MODEL", "tiny")
LOCAL_WHISPER_DEVICE = os.getenv("LOCAL_WHISPER_DEVICE", "cpu")
LOCAL_WHISPER_COMPUTE_TYPE = os.getenv("LOCAL_WHISPER_COMPUTE_TYPE", "int8")
LOCAL_WHISPER_LANGUAGE = os.getenv("LOCAL_WHISPER_LANGUAGE") or None

DOC_EXTENSIONS = {".pdf", ".csv", ".txt", ".md"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".webm", ".ogg", ".flac", ".aac", ".mp4", ".mpeg", ".mpga"}

router = APIRouter(prefix="/tools", tags=["tools"])
_local_whisper_model = None


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    location: str = "India"
    hl: str = "en"
    gl: str = "in"


class WebPageRequest(BaseModel):
    url: str = Field(min_length=8)


def make_safe_filename(file_name: str) -> str:
    clean_name = re.sub(r"[^a-zA-Z0-9._-]", "-", file_name).strip("-")
    return clean_name or "bytebot-upload"


def make_preview_text(text: str, max_length: int = 700) -> str:
    compact_text = (
        " ".join(text.split())
        .replace("\ufeff", "")
        .replace("ï»¿", "")
    )
    if len(compact_text) <= max_length:
        return compact_text

    return f"{compact_text[:max_length].rstrip()}..."


def get_percentile(sorted_values: list[float], percentile: float) -> float:
    if not sorted_values:
        return 0.0

    position = (len(sorted_values) - 1) * percentile
    lower_index = int(position)
    upper_index = min(lower_index + 1, len(sorted_values) - 1)
    weight = position - lower_index
    return sorted_values[lower_index] * (1 - weight) + sorted_values[upper_index] * weight


def make_csv_summary(file_path: Path) -> str:
    """Create a small CSV analysis chunk for later chat questions.

    This gives Byte-Bot useful context for questions like "any outliers?"
    without needing a full vector database yet.
    """
    with file_path.open("r", encoding="utf-8-sig", errors="ignore", newline="") as csv_file:
        rows = list(csv.DictReader(csv_file))

    if not rows:
        return "CSV analysis: the file has headers but no data rows."

    numeric_columns: dict[str, list[tuple[int, float]]] = {}

    for row_index, row in enumerate(rows, start=1):
        for column_name, raw_value in row.items():
            if raw_value is None:
                continue

            clean_value = str(raw_value).replace(",", "").strip()
            if not clean_value:
                continue

            try:
                number_value = float(clean_value)
            except ValueError:
                continue

            numeric_columns.setdefault(column_name, []).append((row_index, number_value))

    if not numeric_columns:
        return f"CSV analysis: {len(rows)} rows loaded. No numeric columns were detected for outlier analysis."

    summary_lines = [f"CSV analysis summary: {len(rows)} rows loaded."]

    for column_name, row_values in numeric_columns.items():
        values = [value for _, value in row_values]
        sorted_values = sorted(values)
        q1 = get_percentile(sorted_values, 0.25)
        q3 = get_percentile(sorted_values, 0.75)
        iqr = q3 - q1
        lower_limit = q1 - 1.5 * iqr
        upper_limit = q3 + 1.5 * iqr
        outliers = [
            (row_index, value)
            for row_index, value in row_values
            if value < lower_limit or value > upper_limit
        ]
        average_value = sum(values) / len(values)

        line = (
            f"Column '{column_name}': min={min(values):.2f}, max={max(values):.2f}, "
            f"average={average_value:.2f}, IQR outliers={len(outliers)}"
        )

        if outliers:
            examples = ", ".join(
                f"row {row_index} value {value:g}"
                for row_index, value in outliers[:8]
            )
            line = f"{line}. Example outliers: {examples}"
        else:
            line = f"{line}. No IQR outliers found."

        summary_lines.append(line)

    return "\n".join(summary_lines)


def split_documents(documents: list[Any]) -> list[Any]:
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
    except ImportError as error:
        raise HTTPException(
            status_code=503,
            detail="Install langchain-text-splitters before using document chunking.",
        ) from error

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )
    return splitter.split_documents(documents)


def load_documents_from_file(file_path: Path) -> list[Any]:
    try:
        from langchain_community.document_loaders import CSVLoader, PyPDFLoader, TextLoader
    except ImportError as error:
        raise HTTPException(
            status_code=503,
            detail="Install langchain-community before uploading PDF, CSV, or text files.",
        ) from error

    file_extension = file_path.suffix.lower()

    if file_extension == ".pdf":
        loader = PyPDFLoader(str(file_path))
    elif file_extension == ".csv":
        loader = CSVLoader(str(file_path), encoding="utf-8-sig")
    elif file_extension in {".txt", ".md"}:
        loader = TextLoader(str(file_path), encoding="utf-8")
    else:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, CSV, TXT, and MD files can be converted into text chunks right now.",
        )

    return loader.load()


def run_serpapi(params: dict[str, Any]) -> dict[str, Any]:
    if not SERPAPI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="SERPAPI_API_KEY is missing. Add it to .env before using web or image search.",
        )

    try:
        import serpapi
    except ImportError as error:
        raise HTTPException(
            status_code=503,
            detail="Install the serpapi Python package before using SerpApi search.",
        ) from error

    client = serpapi.Client(api_key=SERPAPI_API_KEY)
    return dict(client.search(params))


def get_local_whisper_model():
    """Load the free local Whisper model once and reuse it.

    This uses faster-whisper instead of the paid OpenAI Whisper API. The model
    downloads on first use, then stays cached on this machine.
    """
    global _local_whisper_model

    if _local_whisper_model is not None:
        return _local_whisper_model

    try:
        from faster_whisper import WhisperModel
    except ImportError as error:
        raise HTTPException(
            status_code=503,
            detail="Local Whisper is not installed. Run: pip install faster-whisper",
        ) from error

    try:
        _local_whisper_model = WhisperModel(
            LOCAL_WHISPER_MODEL,
            device=LOCAL_WHISPER_DEVICE,
            compute_type=LOCAL_WHISPER_COMPUTE_TYPE,
        )
    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=f"Local Whisper model could not load: {error}",
        ) from error

    return _local_whisper_model


def simplify_result(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "title": result.get("title") or result.get("name") or "Untitled result",
        "link": result.get("link") or result.get("source") or result.get("thumbnail"),
        "snippet": result.get("snippet") or result.get("description") or result.get("source"),
        "thumbnail": result.get("thumbnail"),
    }


@router.post("/search/google")
async def search_google(payload: SearchRequest):
    search_data = run_serpapi(
        {
            "engine": "google",
            "q": payload.query,
            "location": payload.location,
            "google_domain": "google.com",
            "hl": payload.hl,
            "gl": payload.gl,
        }
    )
    organic_results = search_data.get("organic_results", [])[:5]
    return {
        "query": payload.query,
        "results": [simplify_result(result) for result in organic_results],
    }


@router.post("/search/twitter")
async def search_twitter(payload: SearchRequest):
    search_data = run_serpapi(
        {
            "engine": "google",
            "q": payload.query,
            "location": payload.location,
            "hl": payload.hl,
            "gl": payload.gl,
        }
    )
    twitter_results = search_data.get("twitter_results", [])[:5]
    return {
        "query": payload.query,
        "results": [simplify_result(result) for result in twitter_results],
    }


@router.post("/search/images")
async def search_images(payload: SearchRequest):
    search_data = run_serpapi(
        {
            "engine": "google_images",
            "q": payload.query,
            "location": payload.location,
            "hl": payload.hl,
            "gl": payload.gl,
        }
    )
    image_results = search_data.get("images_results", [])[:8]
    return {
        "query": payload.query,
        "results": [simplify_result(result) for result in image_results],
    }


@router.post("/upload")
async def upload_knowledge_file(
    file: UploadFile = File(...),
    session_id: str = Form("bytebot-guest"),
):
    original_name = file.filename or "bytebot-upload"
    safe_name = make_safe_filename(original_name)
    file_extension = Path(safe_name).suffix.lower()
    saved_path = UPLOAD_FOLDER / safe_name

    with saved_path.open("wb") as output_file:
        shutil.copyfileobj(file.file, output_file)

    if file_extension in DOC_EXTENSIONS:
        documents = load_documents_from_file(saved_path)
        chunks = split_documents(documents)
        extra_texts = []

        if file_extension == ".csv":
            extra_texts.append(make_csv_summary(saved_path))

        save_uploaded_chunks(session_id=session_id, source_name=safe_name, chunks=chunks, extra_texts=extra_texts)
        preview = make_preview_text("\n".join(chunk.page_content for chunk in chunks[:2]))
        if extra_texts:
            preview = make_preview_text(f"{extra_texts[0]}\n\n{preview}")

        return {
            "file_name": safe_name,
            "file_type": file_extension.replace(".", ""),
            "documents_loaded": len(documents),
            "chunks_created": len(chunks),
            "preview": preview,
            "message": "File uploaded, split into chunks, and saved into this chat session context.",
        }

    if file_extension in IMAGE_EXTENSIONS:
        return {
            "file_name": safe_name,
            "file_type": "image",
            "message": "Image uploaded. Image understanding can be connected later.",
        }

    if file_extension in AUDIO_EXTENSIONS:
        return {
            "file_name": safe_name,
            "file_type": "audio",
            "message": "Audio uploaded. Use /tools/transcribe to convert it with local Whisper.",
        }

    raise HTTPException(
        status_code=400,
        detail="Unsupported file type. Try PDF, CSV, TXT, MD, PNG, JPG, WEBP, GIF, MP3, WAV, M4A, WEBM, OGG, FLAC, AAC, MP4, MPEG, or MPGA.",
    )


@router.post("/web-page")
async def load_web_page(payload: WebPageRequest):
    try:
        from langchain_community.document_loaders import WebBaseLoader
    except ImportError as error:
        raise HTTPException(
            status_code=503,
            detail="Install langchain-community and beautifulsoup4 before loading web pages.",
        ) from error

    documents = WebBaseLoader(payload.url).load()
    chunks = split_documents(documents)
    preview = make_preview_text("\n".join(chunk.page_content for chunk in chunks[:2]))

    return {
        "url": payload.url,
        "documents_loaded": len(documents),
        "chunks_created": len(chunks),
        "preview": preview,
    }


@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    file_extension = Path(file.filename or "audio.webm").suffix.lower() or ".webm"

    if file_extension not in AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Voice input accepts MP3, WAV, M4A, WEBM, OGG, FLAC, AAC, MP4, MPEG, and MPGA files.",
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = Path(temp_file.name)

    try:
        model = get_local_whisper_model()
        segments, info = model.transcribe(
            str(temp_path),
            beam_size=5,
            language=LOCAL_WHISPER_LANGUAGE,
        )
        transcript_text = " ".join(segment.text.strip() for segment in segments).strip()

        return {
            "text": transcript_text,
            "provider": "local faster-whisper",
            "model": LOCAL_WHISPER_MODEL,
            "language": getattr(info, "language", None),
        }
    finally:
        temp_path.unlink(missing_ok=True)


# OLD OPENAI WHISPER API VERSION KEPT FOR REFERENCE:
# This needed a paid OPENAI_API_KEY, so Byte-Bot now uses local faster-whisper
# above. If you ever want to restore OpenAI Whisper later, this is the shape:
#
# from openai import OpenAI
# client = OpenAI(api_key=OPENAI_API_KEY)
# with temp_path.open("rb") as audio_file:
#     transcription = client.audio.transcriptions.create(
#         model="whisper-1",
#         file=audio_file,
#     )
# return {"text": transcription.text}
