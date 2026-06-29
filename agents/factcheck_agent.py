import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama3-70b-8192", api_key=os.getenv("GROQ_API_KEY"), temperature=0.1)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a fact-checking expert. Analyze the summary and identify claims that are verified, unverified, or potentially misleading."),
    ("human", "Original Query: {query}\n\nSummary to fact-check:\n{summary}\n\nProvide a structured fact-check report with: VERIFIED, UNVERIFIED, and MISLEADING sections.")
])

chain = prompt | llm

def factcheck_agent(query: str, summary: str) -> dict:
    response = chain.invoke({"query": query, "summary": summary})
    return {
        "agent": "FactCheckAgent",
        "output": response.content
    }
