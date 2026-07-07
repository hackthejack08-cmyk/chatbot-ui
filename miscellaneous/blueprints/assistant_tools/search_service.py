def search_web_placeholder(query: str) -> dict:
    return {
        "query": query,
        "results": [],
        "message": "Web search is not connected yet. Add a search API or source-specific fetcher later.",
    }


def fetch_agenda_placeholder(topic: str) -> dict:
    return {
        "topic": topic,
        "items": [],
        "message": "Agenda/meme fetching is not connected yet.",
    }
