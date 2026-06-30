from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from agents.search_agent import search_agent
from agents.summarizer_agent import summarizer_agent
from agents.factcheck_agent import factcheck_agent
from core.rag_pipeline import index_search_results, get_rag_context
import json

ws_router = APIRouter()

@ws_router.websocket("/ws/research")
async def websocket_research(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        payload = json.loads(data)
        query = payload.get("query", "")
        max_sources = payload.get("max_sources", 5)

        await websocket.send_json({"agent": "SearchAgent", "status": "running", "message": "Searching the web..."})
        search_result = search_agent(query, max_results=max_sources)
        await websocket.send_json({"agent": "SearchAgent", "status": "done", "message": f"Found {len(search_result['sources'])} sources", "sources": search_result["sources"]})

        index_search_results(search_result["raw"])
        rag_context = get_rag_context(query)

        await websocket.send_json({"agent": "SummarizerAgent", "status": "running", "message": "Summarizing content..."})
        summary_result = summarizer_agent(query, search_result["output"] + "\n\n" + rag_context)
        await websocket.send_json({"agent": "SummarizerAgent", "status": "done", "message": summary_result["output"]})

        await websocket.send_json({"agent": "FactCheckAgent", "status": "running", "message": "Fact checking..."})
        factcheck_result = factcheck_agent(query, summary_result["output"])
        await websocket.send_json({"agent": "FactCheckAgent", "status": "done", "message": factcheck_result["output"]})

        await websocket.send_json({"status": "completed"})

    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"status": "error", "message": str(e)})
