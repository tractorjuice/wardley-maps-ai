import streamlit as st
import requests

API_ENDPOINT = "https://api.onlinewardleymaps.com/v1/maps/fetch?id="

# Define the Streamlit app
def app():
    # Set app title
    st.set_page_config(page_title="Wardley Map Viewer", page_icon=":map:")

    # Create a form for entering the Wardley map ID
    map_id = st.text_input("Enter the ID of the Wardley map:")

    # Load the map if an ID is entered
    if map_id:
        # Build the API endpoint URL
        url = f"{API_ENDPOINT}{map_id}"

        # Make a GET request to the API
        response = requests.get(url)

        # Check if the response was successful
        if response.status_code == 200:
            # Display the map
            st.components.v1.html(response.content, width=800, height=600)
        else:
            # Display an error message
            st.error("Failed to load map. Please check the map ID and try again.")

# Run the Streamlit app
if __name__ == "__main__":
    app()
