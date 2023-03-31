import streamlit as st
import requests

# Define the Streamlit app
def app():

    # Set the page title and layout
    st.set_page_config(page_title="Wardley Maps Viewer")
    st.title("Wardley Maps Viewer")

    # Define the form to enter the map ID
    map_id = st.text_input("Enter the ID of the Wardley Map")

    # Load the map data when the user submits the form
    if st.button("Load Map"):
        # Fetch the map data from the API
        url = f"https://api.onlinewardleymaps.com/v1/maps/fetch?id={map_id}"
        response = requests.get(url)

        # Check if the map was found
        if response.status_code == 200:
            map_data = response.json()

            # Display the map
            st.write(map_data)
        else:
            st.error("Map not found. Please enter a valid ID.")

if __name__ == "__main__":
    app()
