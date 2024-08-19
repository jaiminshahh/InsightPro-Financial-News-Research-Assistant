import os
import streamlit as st
import pickle
import time
from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(page_title="InsightPro: Financial & News Research Assistant 📊", layout="wide")

# Custom CSS for background, fonts, and other styling
page_bg_img = '''
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

.stApp {
    background: linear-gradient(135deg, #6a11cb, #2575fc);
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    font-family: 'Poppins', sans-serif;
}

.sidebar .sidebar-content {
    background: rgba(255, 255, 255, 0.8); /* Semi-transparent background for sidebar */
    color: #000000;  /* Set text color to black in the sidebar */
    font-family: 'Poppins', sans-serif;
}

.sidebar .sidebar-title {
    color: #000000;  /* Set sidebar title color to black */
}

h1 {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    font-size: 2.5rem;  /* Ensure font size is large */
    color: #FFFFFF;  /* Set white color for visibility */
    padding-top: 20px;
    margin-top: 0;
    z-index: 100;
}

h2, h3, h4, h5 {
    font-family: 'Poppins', sans-serif;
}

button, label, input {
    font-family: 'Poppins', sans-serif;
    color: #000000; /* Set text color to black in inputs and buttons */
}

/* Apply styles to Streamlit text input and markdown */
.stTextInput label {
    font-size: 1.2rem;  /* Increase font size for text input label */
    color: #FFFFFF;  /* Set the label color to white */
}

.stMarkdown p, .stMarkdown h2, .stMarkdown h3 {
    font-size: 1.3rem;  /* Increase font size for markdown text */
    color: #FFFFFF;  /* Set white color for markdown text */
}

.stAlert p {
    font-size: 1.3rem;  /* Increase font size for alerts (e.g., success messages) */
    color: #FFFFFF;  /* Set white color for alert text */
}

/* Footer text styling */
footer .stMarkdown p {
    font-size: 1.3rem;  /* Increase font size for footer text */
    color: #FFFFFF;  /* Set the footer text to white */
}
</style>
'''

# Insert CSS into the Streamlit app
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title and sidebar
st.title("InsightPro: Financial & News Research Assistant 📊")
st.sidebar.title("News Article URLs")

# Collapsible section for URLs in the sidebar
with st.sidebar.expander("Enter URLs to Analyze"):
    urls = []
    for i in range(3):
        url = st.text_input(f"URL {i+1}", help="Enter the URL of the article you want to analyze")
        urls.append(url)

# Button to process URLs
process_url_clicked = st.sidebar.button("Process URLs")
file_path = "faiss_store_openai.pkl"

# Placeholder for dynamic content updates
main_placeholder = st.empty()

# Initialize the language model
llm = ChatOpenAI(model='gpt-4', temperature=0.9, max_tokens=500)

if process_url_clicked:
    with st.spinner("Loading and processing data..."):
        try:
            # Load data
            loader = UnstructuredURLLoader(urls=urls)
            data = loader.load()

            # Split data into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                separators=['\n\n', '\n', '.', ','],
                chunk_size=1000
            )
            docs = text_splitter.split_documents(data)

            # Create embeddings and build the FAISS index
            embeddings = OpenAIEmbeddings()
            vectorstore_openai = FAISS.from_documents(docs, embeddings)

            # Save the FAISS index to a pickle file
            with open(file_path, "wb") as f:
                pickle.dump(vectorstore_openai, f)

            st.success("Data processing completed successfully! You can now ask questions.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Query input box
query = main_placeholder.text_input("Ask a question about the articles:", placeholder="E.g., What is the main financial impact of the news?")

if query:
    if os.path.exists(file_path):
        with st.spinner("Fetching the answer..."):
            with open(file_path, "rb") as f:
                vectorstore = pickle.load(f)
                chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
                result = chain({"question": query}, return_only_outputs=True)
                
                # Display the answer
                st.header("Answer")
                st.write(result["answer"])

                # Display the sources with clickable links
                sources = result.get("sources", "")
                if sources:
                    st.subheader("Sources:")
                    sources_list = sources.split("\n")  # Split the sources by newline
                    for source in sources_list:
                        st.markdown(f"- [{source}]({source})", unsafe_allow_html=True)

# Footer Call to Action
st.markdown("---")
st.markdown("🔍 **Refine your query or analyze another article for deeper insights.**")
