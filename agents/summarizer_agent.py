import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama3-70b-8192", api_key=os.getenv("GROQ_API_KEY"), temperature=0.3)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research summarizer. Summarize the content clearly and concisely."),
    ("human", "Query: {query}\n\nContent:\n{content}\n\nProvide a detailed, well-structured summary.")
])

chain = prompt | llm

def summarizer_agent(query: str, content: str) -> dict:
    response = chain.invoke({"query": query, "content": content[:6000]})
    return {
        "agent": "SummarizerAgent",
        "output": response.content
    }
