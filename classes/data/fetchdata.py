import streamlit as st
import asyncio
from streamlit_gsheets import GSheetsConnection


class DataConnection:

    @classmethod
    def get_purchase_data(cls):
        conn = st.connection("gsheets", type=GSheetsConnection)
        spread_content =  conn.read(
            spreadsheet=st.secrets['database']['spreadsheet_path']
        )
        return spread_content

    @staticmethod
    async def fetch_center_data():
        # Função bloqueante executada em thread separada
        def read_spreadsheet():
            conn = st.connection("gsheets", type=GSheetsConnection)
            return conn.read(
                spreadsheet=st.secrets['database']['spreadsheet_path']
            )

        return await asyncio.to_thread(read_spreadsheet)