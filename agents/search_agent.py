import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_agent(query: str, max_results: int = 5) -> dict:
    response = client.search(query=query, max_results=max_results, include_raw_content=True)
    results = response.get("results", [])
    sources = [r.get("url", "") for r in results]
    contents = [r.get("content", "") for r in results]
    return {
        "agent": "SearchAgent",
        "output": "\n\n".join(contents),
        "sources": sources,
        "raw": results
    }
