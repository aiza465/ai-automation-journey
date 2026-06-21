from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

pdf_folder = "pdfs"
all_chunks = []

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

for filename in os.listdir(pdf_folder):
    if filename.endswith(".pdf"):
        path = os.path.join(pdf_folder, filename)
        loader = PyPDFLoader(path)
        pages = loader.load()
        chunks = splitter.split_documents(pages)
        all_chunks.extend(chunks)
        print(f"Processed {filename}: {len(chunks)} chunks")

print(f"\nTotal chunks: {len(all_chunks)}")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(all_chunks, embeddings, persist_directory="./pdf_chroma_db")
print("Stored in ChromaDB!")

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

print("\nPDF chat ready! Ask anything about your PDF.\n")

while True:
    question = input("You: ")
    if question == "quit":
        break

    result = qa_chain.invoke({"query": question})
    print(f"\nAI: {result['result']}\n")

    print("Sources used:")
    for doc in result['source_documents']:
        print(f"- Page {doc.metadata.get('page', 'unknown')}")