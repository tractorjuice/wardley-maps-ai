import os
import re
import openai
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Chat with Simon Wardley's Book")
st.title("Chat with Simon Wardley's Book")
st.sidebar.markdown("# Query this book using AI")

st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.0.2")
st.sidebar.markdown("Not optimised")
st.sidebar.markdown("May run out of OpenAI credits")

# Get datastore
DATA_STORE_DIR = "data_store"

if os.path.exists(DATA_STORE_DIR):
  #st.write("Loading database")
  vector_store = FAISS.load_local(
      DATA_STORE_DIR,
      OpenAIEmbeddings()
  )
else:
  st.write(f"Missing files. Upload index.faiss and index.pkl files to {DATA_STORE_DIR} directory first")
  
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

system_template="""Use the following pieces of context to answer the users question.
Take note of the sources and include them in the answer in the format: "SOURCES: source1 source2", use "SOURCES" in capital letters regardless of the number of sources.
If you don't know the answer, just say that "I don't know", don't try to make up an answer.
----------------
{summaries}"""
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}")
    ]
prompt = ChatPromptTemplate.from_messages(messages)

chain_type_kwargs = {"prompt": prompt}
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, max_tokens=256)  # Modify model_name if you have access to GPT-4
chain = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs
)

with st.spinner("Thinking..."):
    query = st.text_input("Question for the book?", value="What is the history or Wardley Mapping?")
    result = chain(query)
    
st.write("### Answer:")
st.write(result['answer'])
st.write(result)
#st.write("### Sources:")
#st.write(result['sources'])
#st.write("### All relevant sources:")
#source_docs = {' '.join(list(set([doc.metadata['source'] for doc in result['source_documents']])))}
#numbers = re.findall(r'\d+', source_docs)
#st.write("From pages: ", numbers)
#st.json(source_docs)
