import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Настройка страницы
st.set_page_config(page_title="График дежурства", page_icon="📅")

@st.cache_resource(ttl=600)
def get_sheet():
    # Загружаем JSON напрямую из файла
    creds = Credentials.from_service_account_file(
        "service_account.json", 
        scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    )
    client = gspread.authorize(creds)
    # SHEET_ID берем из Secrets, это безопасно и удобно
    return client.open_by_key(st.secrets["SHEET_ID"]).get_worksheet(0)

# Интерфейс
st.title("📅 График дежурства")

try:
    sheet = get_sheet()
    records = sheet.get_all_records()
    db = {str(row.get('key', '')): str(row.get('name', '')) for row in records}
    
    name_input = st.text_input("Введите имя:", key="name_in")
    
    if st.button("Записаться на 10:00"):
        if name_input.strip():
            db['cell_10_00'] = name_input.strip()
            # Обновление таблицы
            sheet.clear()
            sheet.append_row(['key', 'name'])
            sheet.append_rows([[k, v] for k, v in db.items()])
            st.success("Успешно записано!")
            st.rerun()
            
    st.write("Текущие данные:", db)

except Exception as e:
    st.error(f"Ошибка при работе с таблицей: {e}")
    
