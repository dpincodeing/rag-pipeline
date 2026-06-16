import time
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from db import init_db, log_query

init_db()

embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="./chroma_db", embedding_function=embedding)
llm = OllamaLLM(model="llama3.2")



start = time.time()

results = db.similarity_search(question, k=1)

context = "\n\n".join([r.page_content for r in results])

prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"

answer = llm.invoke(prompt)

end = time.time()
response_time_ms = int((end - start) * 1000)

chunks = [r.page_content for r in results]
log_query(question, answer, chunks, response_time_ms)

print(f"\nQuestion: {question}")
print(f"\nAnswer: {answer}")
print(f"\nResponse time: {response_time_ms}ms")