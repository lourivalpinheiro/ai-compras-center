import streamlit as st 

class Pages:
    def __init__(self, name: str, icon: str, page_layout: str = "centered"):
        if page_layout == "centered":
            st.set_page_config(page_title=name, page_icon=icon, layout="centered")
        elif page_layout == "wide":
            st.set_page_config(page_title=name, page_icon=icon, layout="wide")
        else:
            raise ValueError("Invalid page layout. Use 'centered' or 'wide'.")

        self.name = name
        self.icon = icon
        self.page_layout = page_layout