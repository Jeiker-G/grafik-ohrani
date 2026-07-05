import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import textwrap

@st.cache_resource(ttl=600)
def get_sheet():
    # Собираем ключ обратно
    full_body = st.secrets["pk1"] + st.secrets["pk2"] + st.secrets["pk3"] + st.secrets["pk4"]
    
    # Формируем PEM формат (разбиваем по 64 символа)
    formatted_body = "\n".join(textwrap.wrap(full_body, 64))
    pem_key = f"-----BEGIN PRIVATE KEY-----\n{formatted_body}\n-----END PRIVATE KEY-----"
    
    creds_dict = {
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": pem_key, 
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"]
    }
    
    creds = Credentials.from_service_account_info(creds_dict)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    return gspread.authorize(creds.with_scopes(scope)).open_by_key(st.secrets["SHEET_ID"]).get_worksheet(0)
    
