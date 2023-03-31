import streamlit as st
import requests
import json

def fetch_wardley_map(map_id):
    url = f"https://api.onlinewardleymaps.com/v1/maps/fetch?id={map_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch Wardley Map.")
        return None


def main():
    st.set_page_config(page_title="Wardley Maps with AI")

    st.title("Wardley Maps with AI")

    map_id = st.text_input("Enter the ID of the Wardley Map from OnlineWardleyMaps:")

    if st.button("Load Map"):
        map_data = fetch_wardley_map(map_id)
        if map_data is not None:
            wardley_map = WardleyMap.from_dict(map_data)
            st_wardley_map = st_wm_component(wardley_map)
            st_wardley_map.json_data = json.dumps(map_data)
            st_wardley_map.render()


if __name__ == "__main__":
    main()
