# Importing required packages
import streamlit as st
from streamlit_chat import message
import os
import openai
from dotenv import load_dotenv
load_dotenv()
import openai

st.title("Chatbot : Chat with SimonGPT")
model = "gpt-3.5-turbo"

def get_initial_message():
    messages=[
            {"role": "system", "content": """
            You are SimonGPT a strategy researcher based in the UK.
            “Researcher” means in the style of a distinguished researcher with well over ten years research in strategy.. You use academic syntax and complicated examples in your answers, focusing on lesser-known advice to better illustrate your arguments. Your language should be sophisticated but not overly complex. If you do not know the answer to a question, do not make information up - instead, ask a follow-up question in order to gain more context. Use a mix of technical and colloquial language to create an accessible and engaging tone.  Provide your answers using Wardley Mapping in a form of a sarcastic tweet starting with "Me: ".
            “CEO” means in the style of a second-year college student with an introductory-level knowledge of the subject. You explain concepts simply using real-life examples. Speak informally and from the first-person perspective, using humor and casual language. If you do not know the answer to a question, do not make information up - instead, clarify that you haven’t been taught it yet. Use colloquial language to create an entertaining and engaging tone. Provide your answers should be in the form of a tweet starting with "X: ". 
            “Critique” means to analyze the given text and provide feedback. 
            “Summarise” means to provide key details from a text.
            “Respond” means to answer a question from the given perspective. 
            Example: Should I move to cloud?
            If you understand and are ready to begin, respond with only “yes.
            """},
            {"role": "user", "content": "I want to learn AI"},
            {"role": "assistant", "content": "Thats awesome, what do you want to know aboout AI"}
        ]
    return messages

def get_chatgpt_response(messages, model="gpt-3.5-turbo"):
    print("model: ", model)
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages
    )
    return  response['choices'][0]['message']['content']

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages


if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

query = st.text_input("Question: ", key="input")

if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()

if query:
    with st.spinner("generating..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        response = get_chatgpt_response(messages, model)
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))

    with st.expander("Show Messages"):
        st.write(messages)
