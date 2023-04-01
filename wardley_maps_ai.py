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
    
    Your goal is to: Provide assistance on wardley maps and always give a verbose answer. The following explains how the wardley map is formatted:

Usage
To set the title
Example:

title My Wardley Map
To create a component
component Name [Visibility (Y Axis), Maturity (X Axis)]
Example:

component Customer [0.9, 0.5]
component Cup of Tea [0.9, 0.5]
To create a market
market Name [Visibility (Y Axis), Maturity (X Axis)]
Example:

market Customer [0.9, 0.5]
market Cup of Tea [0.9, 0.5]
evolve Customer 0.9 (market)
Inertia - component likely to face resistance to change.
component Name [Visibility (Y Axis), Maturity (X Axis)] inertia
Example:

component Customer [0.95, 0.5] inertia
component Cup of Tea [0.9, 0.5] inertia
market Cup of Tea [0.9, 0.5] inertia
To evolve a component
evolve Name (X Axis)
Example:

evolve Customer 0.8
evolve Cup of Tea evolve 0.8
To link components
Example:

Start Component->End Component
Customer->Cup of Tea
To indicate flow
Example:

Start Component+<>End Component
Customer+<>Cup of Tea
To set component as pipeline:
pipeline Component Name [X Axis (start), X Axis (end)]
Example:

pipeline Customer [0.15, 0.9]
pipeline Customer
To indicate flow - past components only
Example:

Start Component+<End Component
Hot Water+<Kettle
To indicate flow - future components only
Example:

Start Component+>End Component
Hot Water+>Kettle
To indicate flow - with label
Example:

Start Component+'insert text'>End Component
Hot Water+'$0.10'>Kettle
Pioneers, Settlers, Townplanners area
Add areas indicating which type of working approach supports component development Example:

pioneers [<visibility>, <maturity>, <visibility2>, <maturity2>]
settlers [0.59, 0.43, 0.49, 0.63]
townplanners [0.31, 0.74, 0.15, 0.95]
Build, buy, outsource components
Highlight a component with a build, buy, or outsource method of execution Example:

build <component>
buy <component>
outsource <component>
component Customer [0.9, 0.2] (buy)
component Customer [0.9, 0.2] (build)
component Customer [0.9, 0.2] (outsource)
evolve Customer 0.9 (outsource)
evolve Customer 0.9 (buy)
evolve Customer 0.9 (build)
Link submap to a component
Add a reference link to a submap. A component becomes a link to an other Wardley Map Example:

submap Component [<visibility>, <maturity>] url(urlName)
url urlName [URL]
submap Website [0.83, 0.50] url(submapUrl)
url submapUrl [https://onlinewardleymaps.com/#clone:qu4VDDQryoZEnuw0ZZ]
Stages of Evolution
Change the stages of evolution labels on the map Example:

evolution First->Second->Third->Fourth
evolution Novel->Emerging->Good->Best
Y-Axis Labels
Change the text of the y-axis labels Example:

y-axis Label->Min->Max
y-axis Value Chain->Invisible->Visible
Add notes
Add text to any part of the map Example:

note Note Text [0.9, 0.5]
note +future development [0.9, 0.5]
Available styles
Change the look and feel of a map Example:

style wardley
style handwritten
style colour"""

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
    map_id = st.text_input("Enter the ID of the Wardley Map: For example https://onlinewardleymaps.com/#clone:mUJtoSmOfqlfXhNMJP, enter: mUJtoSmOfqlfXhNMJP")
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
            
            st.markdown("### Prompt:")
            st.write(prompt)
            
            def load_LLM(openai_api_key):
                """Logic for loading the chain you want to use should go here."""
                llm = OpenAI(temperature=0.1, openai_api_key=st.secrets["OPENAI_API_KEY"])
                return llm
            
            llm = load_LLM(["OPENAI_API_KEY"])
            
            prompt_wardley_ai = prompt.format(question=question, map=map_data)
            response = llm(prompt_wardley_ai)
            
            st.markdown("### Input Prompt:")
            st.write(prompt_wardley_ai)
            
            st.markdown("### Question:")
            st.write(question)
            
            st.markdown("### Response:")
            st.write(response)
                   
        else:
            st.error("Map not found. Please enter a valid ID.")
                                                                                                                          
if __name__ == "__main__":
    app()
