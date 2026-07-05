import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Настройка подключения
@st.cache_resource
def get_sheet():
    # Берет данные из Secrets
    creds_dict = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(creds_dict)
    scoped_creds = creds.with_scopes([
        "https://www.googleapis.com/auth/spreadsheets", 
        "https://www.googleapis.com/auth/drive"
    ])
    client = gspread.authorize(scoped_creds)
    # Открываем таблицу по ID и берем ПЕРВЫЙ лист
    return client.open_by_key(st.secrets["SHEET_ID"]).get_worksheet(0)

def load_data():
    sheet = get_sheet()
    data = sheet.get_all_records()
    # Если данные пустые, вернем словарь с дефолтными значениями
    return {str(row.get('key', '')): str(row.get('name', '')) for row in data}

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
