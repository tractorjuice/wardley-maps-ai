# Importing required packages
import streamlit as st
from streamlit_chat import message
import os
import openai
import re
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

openai.api_key = st.secrets["OPENAI_API_KEY"]
DATA_STORE_DIR = "data_store"

model = "gpt-3.5-turbo"

st.set_page_config(page_title="Chat with SimonGPT")
st.title("Chat with SimonGPT")
#st.sidebar.markdown("#Query this book using AI")

st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.0.2")
st.sidebar.markdown("Not optimised")
st.sidebar.markdown("May run out of OpenAI credits")

if os.path.exists(DATA_STORE_DIR):
  vector_store = FAISS.load_local(
      DATA_STORE_DIR,
      OpenAIEmbeddings()
  )
else:
  st.write(f"Missing files. Upload index.faiss and index.pkl files to {DATA_STORE_DIR} directory first")

system_template="""You are SimonGPT a strategy researcher based in the UK.
            “Researcher” means in the style of a strategy researcher with over twenty years research in strategy and cloud computing.
            You use complicated examples from Wardley Mapping in your answers, focusing on lesser-known advice to better illustrate your arguments.
            Your language should be for a 12 year old to understand.
            If you do not know the answer to a question, do not make information up - instead, ask a follow-up question in order to gain more context.
            Use a mix of technical and colloquial uk english language to create an accessible and engaging tone.
            Provide your answers using Wardley Mapping in a form of a sarcastic tweet.
            """

messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{"I want to learn about Wardley Mapping"}")
    ]
prompt = ChatPromptTemplate.from_messages(messages)
#print("prompt")

chain_type_kwargs = {"prompt": prompt}
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, max_tokens=256)  # Modify model_name if you have access to GPT-4
chain = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs
)

#-------------------------------

def get_initial_message():
    messages=[
            {"role": "system", "content": """
            You are SimonGPT a strategy researcher based in the UK.
            “Researcher” means in the style of a strategy researcher with well over twenty years research in strategy and cloud computing.
            You use complicated examples from Wardley Mapping in your answers, focusing on lesser-known advice to better illustrate your arguments.
            Your language should be for an 12 year old to understand.
            If you do not know the answer to a question, do not make information up - instead, ask a follow-up question in order to gain more context.
            Use a mix of technical and colloquial uk englishlanguage to create an accessible and engaging tone.
            Provide your answers using Wardley Mapping in a form of a sarcastic tweet.
            """},
            {"role": "user", "content": "I want to learn about Wardley Mapping"},
            {"role": "assistant", "content": "Thats awesome, what do you want to know aboout Wardley Mapping"}
        ]
    return messages

def get_chatgpt_response(messages, model="gpt-3.5-turbo"):
    response = response = chain(query)
    return response

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
    
if 'past' not in st.session_state:
    st.session_state['past'] = []

query = st.text_input("Question: ", "What is Wardley Mapping?", key="input")

#if 'messages' not in st.session_state:
#    st.session_state['messages'] = get_initial_message()

if query:
    with st.spinner("generating..."):
        #messages = st.session_state['messages']
        #messages = update_chat(messages, "user", query)
        #response = get_chatgpt_response(messages, model)
        
        response = chain(query)
        st.write(response)
        
        #messages = update_chat(messages, "assistant", response)
        #st.session_state.past.append(query)
        #st.session_state.generated.append(response)

#if st.session_state['generated']:

    #for i in range(len(st.session_state['generated'])-1, -1, -1):
        #message(st.session_state["generated"][i], key=str(i))
        #message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

 
