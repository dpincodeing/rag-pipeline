from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

loader = PyPDFLoader("document.pdf")
pages = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(pages)

print(f"Total chunks: {len(chunks)}")
print(f"\nFirst chunk:\n{chunks[0].page_content}")
print(f"\nSecond chunk:\n{chunks[1].page_content}")

embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

db = Chroma.from_documents(chunks, embedding, persist_directory="./chroma_db")

print(f"\nVector store created. Total vectors stored: {db._collection.count()}")