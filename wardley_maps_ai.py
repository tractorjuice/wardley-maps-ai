import streamlit as st
import requests

st.set_page_config(page_title="Wardley Map Viewer")

# Define the base URL for the API
BASE_URL = "https://api.onlinewardleymaps.com/v1/maps/fetch?id="

def fetch_wardley_map(map_id):
    """
    Fetches the wardley map with the given ID from the API.
    """
    url = BASE_URL + map_id
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Create the sidebar
st.sidebar.title("Wardley Map Viewer")
map_id = st.sidebar.text_input("Enter the ID of the wardley map:")

# Fetch the map data and display it if available
if map_id:
    map_data = fetch_wardley_map(map_id)
    if map_data:
        st.write("## Wardley Map")
        st.image(map_data["image_url"])
    else:
        st.write("Invalid map ID")

# Create a box to ask questions about the wardley map
st.write("## Ask a Question")
question = st.text_input("Enter your question here:")
if question:
    st.write(f"You asked: {question}")
    # Code to process the question and provide an answer goes here
