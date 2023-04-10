import os
import openai
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

openai.api_key = st.secrets["OPENAI_API_KEY"]

REPO_URL = "https://github.com/tractorjuice/wardley-maps-ai"  # Source URL#
DOCS_FOLDER = "wmdocs"  # Folder to check out to
REPO_DOCUMENTS_PATH = "index"  # Set to "" to index the whole data folder
DOCUMENT_BASE_URL = "https://github.com/tractorjuice/wardley-maps-ai/tree/main/index"  # Actual URL
DATA_STORE_DIR = "data_store"

# Upload the files `$DATA_STORE_DIR/index.faiss` and `$DATA_STORE_DIR/index.pkl` to local
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

if os.path.exists(DATA_STORE_DIR):
  vector_store = FAISS.load_local(
      DATA_STORE_DIR,
      OpenAIEmbeddings()
  )
else:
  print(f"Missing files. Upload index.faiss and index.pkl files to {DATA_STORE_DIR} directory first")

prompt = st.text_input("Prompt", value="What is this video about?")

if st.button("Send"):
    with st.spinner("Generating response..."):
        
        response = index.query(prompt)
        text.text_area("Messages", response, height=250)

if st.button("Clear"):
    st.session_state["messages"] = BASE_PROMPT
    show_messages(text)
