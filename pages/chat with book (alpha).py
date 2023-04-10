import os
import openai
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

openai.api_key = st.secrets["OPENAI_API_KEY"]

REPO_URL = "https://github.com/tractorjuice/wardley-maps-ai"  # Source URL#
DOCS_FOLDER = "wmdocs"  # Folder to check out to
REPO_DOCUMENTS_PATH = "index"  # Set to "" to index the whole data folder
DOCUMENT_BASE_URL = "https://github.com/tractorjuice/wardley-maps-ai/tree/main/index"  # Actual URL
DATA_STORE_DIR = "data_store"

# Upload the files `$DATA_STORE_DIR/index.faiss` and `$DATA_STORE_DIR/index.pkl` to local

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

#search_result = vector_store.similarity_search_with_score("What is the history of Wardley Maps?")
#st.write(search_result)

query = "What is the history of Wardley Mapping?"
result = chain(query)
st.write("### Question:")
st.write(quey)
st.write("### Answer:")
st.write({result['answer']}
st.write("### Sources:")
st.write({result['sources']})      
#st.write(result)

#from IPython.display import display, Markdown
#def print_result(result):
#  output_text = f"""### Question: 
#  {query}
#  ### Answer: 
#  {result['answer']}
#  ### Sources: 
#  {result['sources']}
#  ### All relevant sources:
#  {' '.join(list(set([doc.metadata['source'] for doc in result['source_documents']])))}
#  """
#  display(Markdown(output_text))

if st.button("Send"):
    with st.spinner("Generating response..."):
        
        response = index.query(prompt)
        text.text_area("Messages", response, height=250)

if st.button("Clear"):
    st.session_state["messages"] = BASE_PROMPT
    show_messages(text)
