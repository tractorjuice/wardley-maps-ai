import streamlit as st
import requests

# Define the API URL
API_URL = "https://api.onlinewardleymaps.com/v1/maps/fetch"

def get_wardley_map(map_id):
    # Call the API with the provided map_id
    response = requests.get(f"{API_URL}?id={map_id}")
    # Check the status code of the response
    if response.status_code == 200:
        # Return the JSON response
        return response.json()
    else:
        # Raise an exception if there was an error
        raise Exception(f"Error fetching Wardley Map with ID {map_id}. Status code: {response.status_code}")

# Create a Streamlit app
def app():
    # Set the app title
    st.set_page_config(page_title="Wardley Maps Viewer")

    # Add a form to input the map ID
    map_id = st.text_input("Enter the ID of the Wardley Map you want to view:")
    # Add a button to submit the form
    if st.button("Load Map"):
        # Call the get_wardley_map function to fetch the map data
        map_data = get_wardley_map(map_id)
        # Display the map using an iframe
        st.components.v1.iframe(src=f"https://onlinewardleymaps.com/maps/{map_id}", height=600, scrolling=True)
