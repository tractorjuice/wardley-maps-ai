import streamlit as st
import requests
from io import BytesIO
from PIL import Image

# Define the URL for the Wardley Maps API
API_URL = 'https://api.onlinewardleymaps.com/v1/maps/fetch'

# Define the Streamlit app
def app():
    # Add a title and a form to the app
    st.title("Load Wardley Map from Online Wardley Maps API")
    map_id = st.text_input("Enter the ID of the Wardley Map:")

    # If the form is submitted, retrieve the map using the API
    if st.button("Load Map"):
        # Construct the API URL with the provided map ID
        url = f"{API_URL}?id={map_id}"
        
        # Send a request to the API to retrieve the map
        response = requests.get(url)
        
        # If the request was successful, display the map
        if response.status_code == 200:
            # Convert the response content to an image
            img = Image.open(BytesIO(response.content))
            
            # Display the image in the Streamlit app
            st.image(img, caption="Wardley Map")
            
        # If the request failed, display an error message
        else:
            st.error("Failed to load map. Please check the map ID and try again.")
            
# Run the Streamlit app
if __name__ == "__main__":
    app()
