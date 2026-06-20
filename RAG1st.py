from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# Load your documents
docs_folder = "docs"
documents = []
for filename in os.listdir(docs_folder):
    if filename.endswith(".txt"):
        with open(os.path.join(docs_folder, filename)) as f:
            documents.append(f.read())

print(f"Loaded {len(documents)} documents")

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
chunks = splitter.create_documents(documents)
print(f"Split into {len(chunks)} chunks")

# Create embeddings and store in ChromaDB
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
print("Stored in ChromaDB!")

# Create retrieval chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

print("\nRAG system ready! Ask questions about your documents.\n")

while True:
    question = input("You: ")
    if question == "quit":
        break

    result = qa_chain.invoke({"query": question})
    print(f"\nAI: {result['result']}\n")