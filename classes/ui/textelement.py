import streamlit as st 

class TextElement:
    @classmethod
    def write_text(cls, text:str):
        st.write(text)
    
    @classmethod
    def set_title(cls, title:str):
        st.title(title)
    
    @classmethod
    def set_caption(cls, caption:str):
        st.caption(caption)