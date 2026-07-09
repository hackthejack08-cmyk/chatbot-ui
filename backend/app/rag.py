import json
import re
from pathlib import Path


KNOWLEDGE_FOLDER = Path(__file__).with_name("knowledge")
BACKEND_ROOT = Path(__file__).resolve().parents[1]
UPLOADED_KNOWLEDGE_FILE = BACKEND_ROOT / "storage" / "uploaded_knowledge.jsonl"
ALLOWED_TEXT_FILES = {".txt", ".md"}
MAX_CONTEXT_CHARS = 6000
SEARCH_STOP_WORDS = {
    "the", "and", "are", "you", "your", "for", "from", "with", "this", "that",
    "what", "who", "why", "how", "when", "where", "according", "about", "into",
    "does", "did", "can", "could", "would", "should", "have", "has", "had",
}


def build_retriever():
    if not KNOWLEDGE_FOLDER.exists():
        return []

    knowledge_chunks = []

    for file_path in KNOWLEDGE_FOLDER.iterdir():
        if file_path.suffix.lower() not in ALLOWED_TEXT_FILES:
            continue

        file_text = file_path.read_text(encoding="utf-8", errors="ignore")
        small_chunks = [chunk.strip() for chunk in file_text.split("\n\n") if chunk.strip()]

        for chunk_text in small_chunks:
            knowledge_chunks.append(
                {
                    "source_name": file_path.name,
                    "text": chunk_text,
                }
            )

    return knowledge_chunks


def save_uploaded_chunks(session_id: str, source_name: str, chunks: list, extra_texts: list[str] | None = None):
    """Append uploaded file chunks to a tiny JSONL knowledge store.

    This is intentionally simple for the beginner project stage. Later this
    file can be replaced by a vector database such as Chroma, FAISS, or MongoDB
    Atlas Vector Search.
    """
    UPLOADED_KNOWLEDGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    safe_session_id = (session_id or "bytebot-guest").strip() or "bytebot-guest"
    texts_to_store = list(extra_texts or [])

    for chunk in chunks:
        chunk_text = getattr(chunk, "page_content", str(chunk)).strip()
        if chunk_text:
            texts_to_store.append(chunk_text)

    with UPLOADED_KNOWLEDGE_FILE.open("a", encoding="utf-8") as knowledge_file:
        for index, chunk_text in enumerate(texts_to_store[:300], start=1):
            clean_chunk_text = chunk_text.replace("\ufeff", "").replace("ï»¿", "")
            record = {
                "session_id": safe_session_id,
                "source_name": source_name,
                "chunk_id": index,
                "text": clean_chunk_text,
            }
            knowledge_file.write(json.dumps(record, ensure_ascii=True) + "\n")


def load_uploaded_chunks(session_id: str | None = None) -> list[dict]:
    if not UPLOADED_KNOWLEDGE_FILE.exists():
        return []

    safe_session_id = (session_id or "").strip()
    uploaded_chunks = []

    with UPLOADED_KNOWLEDGE_FILE.open("r", encoding="utf-8") as knowledge_file:
        for line in knowledge_file:
            clean_line = line.lstrip("\ufeff").strip()
            if not clean_line:
                continue

            try:
                record = json.loads(clean_line)
            except json.JSONDecodeError:
                continue

            if safe_session_id and record.get("session_id") != safe_session_id:
                continue

            uploaded_chunks.append(
                {
                    "source_name": record.get("source_name", "uploaded-file"),
                    "text": record.get("text", ""),
                }
            )

    return uploaded_chunks


def clear_uploaded_knowledge(session_id: str):
    if not UPLOADED_KNOWLEDGE_FILE.exists():
        return

    safe_session_id = (session_id or "").strip()
    if not safe_session_id:
        return

    kept_lines = []
    with UPLOADED_KNOWLEDGE_FILE.open("r", encoding="utf-8") as knowledge_file:
        for line in knowledge_file:
            clean_line = line.lstrip("\ufeff").strip()
            if not clean_line:
                continue

            try:
                record = json.loads(clean_line)
            except json.JSONDecodeError:
                continue

            if record.get("session_id") != safe_session_id:
                kept_lines.append(clean_line + "\n")

    UPLOADED_KNOWLEDGE_FILE.write_text("".join(kept_lines), encoding="utf-8")


def get_search_words(user_message: str) -> set[str]:
    return {
        word.lower()
        for word in re.findall(r"[a-zA-Z0-9_]+", user_message)
        if len(word) > 2 and word.lower() not in SEARCH_STOP_WORDS
    }


def get_context(knowledge_chunks, user_message: str, session_id: str | None = None) -> str:
    # Re-read the project knowledge files on every chat request.
    # This keeps beginner edits simple: save the txt/md file, ask again, and
    # Byte-Bot can use the new content without rebuilding the whole project.
    current_file_chunks = build_retriever()
    uploaded_chunks = load_uploaded_chunks(session_id)
    all_chunks = current_file_chunks + uploaded_chunks

    if not current_file_chunks and knowledge_chunks:
        all_chunks = list(knowledge_chunks or []) + uploaded_chunks

    if not all_chunks:
        return "No extra knowledge loaded yet."

    search_words = get_search_words(user_message)
    file_question_words = {
        "file", "uploaded", "upload", "document", "pdf", "csv", "txt",
        "content", "summary", "summarize", "analyze", "analysis", "outlier",
        "outliers", "data", "dataset", "column", "columns", "row", "rows",
    }

    scored_chunks = []

    for chunk in all_chunks:
        chunk_text_lower = chunk["text"].lower()
        source_name_lower = chunk["source_name"].lower()
        match_score = sum(1 for word in search_words if word in chunk_text_lower or word in source_name_lower)

        if match_score > 0:
            scored_chunks.append((match_score, chunk))

    if not scored_chunks:
        if uploaded_chunks and search_words.intersection(file_question_words):
            scored_chunks = [(1, chunk) for chunk in uploaded_chunks[:8]]
        else:
            return "No matching knowledge found."

    scored_chunks.sort(key=lambda item: item[0], reverse=True)
    best_chunks = [item[1] for item in scored_chunks[:8]]

    context_parts = []
    total_length = 0

    for chunk in best_chunks:
        context_part = f"Source: {chunk['source_name']}\n{chunk['text']}"
        if total_length + len(context_part) > MAX_CONTEXT_CHARS:
            break
        context_parts.append(context_part)
        total_length += len(context_part)

    if not context_parts:
        return "No matching knowledge found."

    return "\n\n".join(context_parts)
