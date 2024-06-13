import streamlit as st
from pdf_utils import process_pdf_texts
from github_utils import process_repo_texts
from query_utils import rank_doc, rag

st.set_page_config(page_title="PDF & GitHub Query Assistant with Reranker", layout="wide")

st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type=['pdf'])
repo_url = st.sidebar.text_input("Enter GitHub Repository URL")

if uploaded_file and api_key:
    formatted_texts = process_pdf_texts(uploaded_file)
    st.session_state.processed_texts = formatted_texts

if repo_url and api_key:
    formatted_texts = process_repo_texts(repo_url)
    st.session_state.processed_texts = formatted_texts

st.title("Free PDF & GitHub Query Assistant with Reranker")
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if st.session_state.chat_history:
    for query, response in st.session_state.chat_history:
        st.container().markdown(f"**Q**: {query}")
        st.container().markdown(f"**A**: {response}")

query = st.text_input("Type your question here:", key="query")

if st.button("Submit Query"):
    if 'processed_texts' in st.session_state and query and api_key:
        with st.spinner('Processing...'):
            retrieved_documents = rank_doc(query, st.session_state.processed_texts)
            output_wrapped = rag(query, retrieved_documents, api_key)
            st.session_state.chat_history.append((query, output_wrapped))
            st.container().markdown(f"**Q**: {query}")
            st.container().markdown(f"**A**: {output_wrapped}")
    else:
        st.error("Please upload a PDF or enter a GitHub repository URL, ensure the API key is set, and type a question.")
