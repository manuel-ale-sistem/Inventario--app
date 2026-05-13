import base64
import streamlit as st

def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
        }}
        .overlay {{
            background-color: rgba(0,0,0,0.65);
            padding: 20px;
            border-radius: 15px;
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )