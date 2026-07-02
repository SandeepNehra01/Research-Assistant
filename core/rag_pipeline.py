from core.vector_store import store_documents, retrieve_context

def index_search_results(results: list[dict]):
    texts = [r.get("content", "") for r in results if r.get("content")]
    sources = [r.get("url", "unknown") for r in results if r.get("content")]
    if texts:
        store_documents(texts, sources)

def get_rag_context(query: str) -> str:
    return retrieve_context(query)
