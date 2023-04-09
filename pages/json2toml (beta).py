import streamlit as st
import json
import toml
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="JSON to TOML file converter",
    page_icon="✔️",
)

with st.sidebar:
    selected = option_menu(
        "Choose conversion",
        ["WM to JSON", "WM to TOML", "JSON to TOML"],
        icons=["gear"],
        # menu_icon="bookmark-fill",
        menu_icon="robot",
        default_index=0,
    )

if selected == "JSON to TOML":

    st.image("./pages/logo.gif", width=200)
    st.title("JSON to TOML file converter")
    st.write(
        """  

            """
    )

    st.write(
        """  
    Let's convert your Wardley Map in JSON to TOML

            """
    )

    st.write(
        """  

            """
    )
    json_file = st.file_uploader("UPLOAD JSON FILE")
    st.info(
        f"""
                👆 Upload your json file. Or try a [sample](https://github.com/CharlyWargnier/CSVs/blob/master/more_samples/firestore-key-sample.json?raw=true).
                
                """
    )


    if json_file is not None:
        json_text = json_file.read()

        st.write("JSON CONTENT")
        st.code(json.loads(json_text))

        toml_content = toml.dumps(json.loads(json_text))
        st.write("TOML FILE CONTENT")
        st.code(toml_content)
        toml_file_name = json_file.name.replace(".json", ".toml")
        st.download_button(
            "DOWNLOAD TOML FILE", data=toml_content, file_name=toml_file_name
        )
        
elif selected == "WM to TOML":
    st.title("WM to TOML")
    
    st.image("./pages/logo.gif", width=200)
    st.title("WM to TOML File Converter")
    st.write(
        """  
            """
    )

    st.write(
        """  
    Let's convert your Wardley Map in WM to TOML
            """
    )

    st.write(
        """  
            """
    )
    json_file = st.file_uploader("UPLOAD JSON FILE")
    st.info(
        f"""
                👆 Upload your json file. Or try a [sample](https://github.com/CharlyWargnier/CSVs/blob/master/more_samples/firestore-key-sample.json?raw=true).
                
                """
    )

    if json_file is not None:
        json_text = json_file.read()

        st.write("JSON CONTENT")
        st.code(json.loads(json_text))

        toml_content = toml.dumps(json.loads(json_text))
        st.write("TOML FILE CONTENT")
        st.code(toml_content)
        toml_file_name = json_file.name.replace(".json", ".toml")
        st.download_button(
            "DOWNLOAD TOML FILE", data=toml_content, file_name=toml_file_name
        )
        
elif selected == "Options":
    st.title("Options")
    
elif selected == "JSON to TOML":
    st.title("JSON to TOML")

