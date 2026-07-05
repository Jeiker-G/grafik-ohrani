import streamlit as st
import gspread
import textwrap
from google.oauth2.service_account import Credentials

@st.cache_resource(ttl=600)
def get_sheet():
    # Нарезаем строку на куски по 64 символа и собираем обратно с переносами
    raw_key = st.secrets["private_key"]
    # Убираем заголовки, чтобы нарезать только тело
    body = raw_key.replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", "")
    formatted_key = "-----BEGIN PRIVATE KEY-----\n" + "\n".join(textwrap.wrap(body, 64)) + "\n-----END PRIVATE KEY-----"
    
    creds_dict = {
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": formatted_key,
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"]
    }
    
    creds = Credentials.from_service_account_info(creds_dict)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    client = gspread.authorize(creds.with_scopes(scope))
    return client.open_by_key(st.secrets["SHEET_ID"]).get_worksheet(0)
    
