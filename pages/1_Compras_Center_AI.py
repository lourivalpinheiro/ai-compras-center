import streamlit as st
from classes.ui.header import HeaderMenu
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI


memory = ConversationBufferMemory()
api_key = st.secrets["ai"]["OPEN_AI_KEY"]

def carrega_modelo():
    chat = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)
    st.session_state['chat'] = chat

def chat_page():
    HeaderMenu().hide_menu()
    st.header("🤖 COMPRAS CENTER AI", divider=True)
    if st.button("Inicializar IA", use_container_width=True):
            carrega_modelo()
    

    chat_model = st.session_state.get('chat')
    memoria = st.session_state.get('memoria', memory)

    for mensagem in memoria.buffer_as_messages:
        chat = st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)

    input_usuario = st.chat_input("Fale com o Compras IA...")
    if input_usuario:
        # memoria.chat_memory.add_user_message(input_usuario)
        chat = st.chat_message('human')
        chat.markdown(input_usuario)
        chat = st.chat_message('ai')
        resposta = chat.write_stream(chat_model.stream(input_usuario))
        memoria.chat_memory.add_ai_message(resposta)
        st.session_state['memoria'] = memoria


        


def main():
    chat_page()

if __name__ == '__main__':
    main()
