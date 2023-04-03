import streamlit as st

st.set_page_config(
    page_title="Wardley Mapping with AI",
)

st.write("# Welcome to Wardley Mapping with AI")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    **Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [Twitter thread](https://twitter.com/mcraddock/status/1641537955507347476)
    ![alt text](prompt-engineering-wardley.png "Tweet")
"""
)
