import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Настройка подключения
@st.cache_resource
def get_sheet():
    # Берет данные из Secrets, которые мы сейчас настроим
    creds_dict = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(creds_dict)
    scoped_creds = creds.with_scopes([
        "https://spreadsheets.google.com/feeds", 
        "https://www.googleapis.com/auth/drive"
    ])
    client = gspread.authorize(scoped_creds)
    return client.open_by_key(st.secrets["SHEET_ID"]).sheet1

def load_data():
    sheet = get_sheet()
    data = sheet.get_all_records()
    return {str(row['key']): str(row['name']) for row in data}

def save_data(db):
    sheet = get_sheet()
    rows = [[k, v] for k, v in db.items()]
    sheet.clear()
    sheet.append_row(['key', 'name'])
    if rows:
        sheet.append_rows(rows)

# Интерфейс
st.title("График дежурства")

db = load_data()
name_input = st.text_input("Введите имя:", key="name_in")

if st.button("Записаться на 10:00"):
    if name_input.strip():
        db['cell_10_00'] = name_input.strip()
        save_data(db)
        st.success("Сохранено в Google Таблицу!")
        st.rerun()
    else:
        st.warning("Сначала введите имя!")

st.write("Текущие данные:", db)
