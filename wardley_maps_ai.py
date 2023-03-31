import streamlit as st
import requests
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

API_ENDPOINT = "https://api.onlinewardleymaps.com/v1/maps/fetch?id="

template = """
    Assistant is a large language model trained by OpenAI.
    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.
    
    Your goal is to: Provide assistance on wardley maps and always give a verbose answer.

    Below is the map and question:
    WARDLEY MAP: {map}
    QUESTION: {question}
    
    YOUR RESPONSE:
"""

# Define the Streamlit app
def app():

    # Set the page title and layout
    st.set_page_config(page_title="Wardley Maps with AI")
    st.title("Wardley Maps with AI")
        
    # Define the form to enter the map ID
    map_id = st.text_input("Enter the ID of the Wardley Map: For example https://onlinewardleymaps.com/#mUJtoSmOfqlfXhNMJP, enter: mUJtoSmOfqlfXhNMJP")
    question = st.text_input(label="Question ", placeholder="How many components are in this map?", key="q_input", max_chars=150)
    if len(question.split(" ")) > 700:
        st.write("Please enter a shorter question about your Wardley Map")
        st.stop()

    # Load the map data when the user submits the form
    if st.button("Ask Question to Wardley AI"):
        # Fetch the map data from the API
        url = f"https://api.onlinewardleymaps.com/v1/maps/fetch?id={map_id}"
        response = requests.get(url)

        # Check if the map was found
        if response.status_code == 200:
            map_data = response.json()

            # Display the map
            #st.write(map_data)
            
            prompt = PromptTemplate(
                input_variables=["map", "question"],
                template=template,
            )
            
            #st.markdown("### Prompt:")
            #st.write(prompt)
            
            def load_LLM(openai_api_key):
                """Logic for loading the chain you want to use should go here."""
                llm = OpenAI(temperature=0.1, openai_api_key=st.secrets["OPENAI_API_KEY"])
                return llm
            
            llm = load_LLM(["OPENAI_API_KEY"])
            
            prompt_wardley_ai = prompt.format(question=question, map=map_data)
            response = llm(prompt_wardley_ai)
            
            #st.markdown("### Input Prompt:")
            #st.write(prompt_wardley_ai)
            
            #st.markdown("### Question:")
            #st.write(question)
            
            st.markdown("### Response:")
            st.write(response)
                   
        else:
            st.error("Map not found. Please enter a valid ID.")
                                                                                                                          
if __name__ == "__main__":
    app()
