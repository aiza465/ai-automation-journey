import streamlit as st
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import os
import tempfile

load_dotenv()

st.set_page_config(page_title="Chat with your PDF", page_icon="📄")
st.title("📄 Chat with your PDF")
st.write("Upload a PDF and ask questions about it")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

if uploaded_file is not None:
    if "qa_chain" not in st.session_state:
        with st.spinner("Reading and processing your PDF..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            loader = PyPDFLoader(tmp_path)
            pages = loader.load()



            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = splitter.split_documents(pages)

            if len(chunks) == 0:
                st.error(
                    "This PDF appears to be scanned/image-based with no extractable text. Try a different PDF with actual text content.")
                st.stop()



            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            vectorstore = Chroma.from_documents(chunks, embeddings)

            st.session_state.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
                return_source_documents=True
            )

        st.success(f"PDF processed! {len(chunks)} chunks ready.")

    question = st.text_input("Ask a question about your PDF:")

    if question:
        with st.spinner("Thinking..."):
            result = st.session_state.qa_chain.invoke({"query": question})

        st.write("### Answer")
        st.write(result["result"])

        with st.expander("View sources"):
            for doc in result["source_documents"]:
                st.write(f"Page {doc.metadata.get('page', 'unknown')}")
                st.write(doc.page_content[:200] + "...")