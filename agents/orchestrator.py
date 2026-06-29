from agents.search_agent import search_agent
from agents.summarizer_agent import summarizer_agent
from agents.factcheck_agent import factcheck_agent
from core.rag_pipeline import index_search_results, get_rag_context
from models.schemas import ResearchResponse, AgentResult

def orchestrator(query: str, max_sources: int = 5) -> ResearchResponse:
    agents_trace = []

    # Step 1: Search
    search_result = search_agent(query, max_results=max_sources)
    agents_trace.append(AgentResult(agent=search_result["agent"], output=f"Found {len(search_result['sources'])} sources"))

    # Step 2: Index into RAG
    index_search_results(search_result["raw"])

    # Step 3: Get RAG context + summarize
    rag_context = get_rag_context(query)
    combined_content = search_result["output"] + "\n\n" + rag_context

    summary_result = summarizer_agent(query, combined_content)
    agents_trace.append(AgentResult(agent=summary_result["agent"], output=summary_result["output"]))

    # Step 4: Fact check
    factcheck_result = factcheck_agent(query, summary_result["output"])
    agents_trace.append(AgentResult(agent=factcheck_result["agent"], output=factcheck_result["output"]))

    return ResearchResponse(
        query=query,
        summary=summary_result["output"],
        fact_check=factcheck_result["output"],
        sources=search_result["sources"],
        agents_trace=agents_trace
    )
