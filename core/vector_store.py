from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = Chroma(embedding_function=embeddings, persist_directory="./chroma_db")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

def store_documents(texts: list[str], sources: list[str]):
    docs = [Document(page_content=t, metadata={"source": s}) for t, s in zip(texts, sources)]
    chunks = splitter.split_documents(docs)
    vector_store.add_documents(chunks)

def retrieve_context(query: str, k: int = 4) -> str:
    results = vector_store.similarity_search(query, k=k)
    return "\n\n".join([r.page_content for r in results])
