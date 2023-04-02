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
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

template = """
Your goal is to provide assistance on wardley maps and always give a verbose answer. The following explains how the wardley map is formatted:

Thank you for providing the detailed explanation of the Wardley Map formatting. Here is a summary of the elements in the format:

Title: The title of the Wardley Map.
Components: Name of the component. Component Name [Visibility, Maturity].
Market: Create a market with market Name [Visibility, Maturity].
Inertia: Indicate resistance to change with inertia.
Evolve: Evolution of a component. volve Name (X Axis).
Links: Link components with Start Component->End Component.
Flow: Indicate flow. Component->>Component.
Pipeline: Set a component as a pipeline with pipeline Component Name [X Axis (start), X Axis (end)].
Pioneers, Settlers, Townplanners area: Add areas to indicate the working approach with pioneers, settlers, and townplanners.
Build, buy, outsource: Indicate the method of execution with build, buy, or outsource.
Submap: Link a submap to a component with submap Component [visibility, maturity] url(urlName) and url urlName [URL].
Stages of Evolution: Customize the stages of evolution labels with evolution.
Y-Axis Labels: The visibility of the component
Notes: Notes about this Wardley Map.
Styles: The style of the Wardley Map.
This formatting makes it easy to create and modify Wardley Maps, and it's helpful for understanding the structure and connections between components.

WARDLEY MAP: {map}
QUESTION: {question}
    
    YOUR RESPONSE:
"""
def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    llm = OpenAI(temperature=0.7, openai_api_key, max_tokens=500)
    return llm

# Define the Streamlit app
def app():

    # Set the page title and layout
    st.set_page_config(page_title="Wardley Maps with AI")
    st.title("Wardley Maps with AI")
    
    #st.sidebar.image("images/shakespeare.png")
    st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
    st.sidebar.markdown("Current Version: 0.0.2")
        
    # Define the form to enter the map ID
    map_id = st.text_input("Enter the ID of the Wardley Map: For example https://onlinewardleymaps.com/#clone:OXeRWhqHSLDXfOnrfI, enter: OXeRWhqHSLDXfOnrfI", value="OXeRWhqHSLDXfOnrfI")
    question = st.text_input(label="Question ", value="What are the components in this wardley map. Display as a list", key="q_input", max_chars=150)
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
            
            st_write(OPENAI_API_KEY)
                        
            llm = load_LLM(OPENAI_API_KEY)
            
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
