import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

@st.cache_resource(ttl=600)
def get_sheet():
    # Читаем конфигурацию из Secrets
    creds_dict = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(creds_dict)
    
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    scoped_creds = creds.with_scopes(scope)
    client = gspread.authorize(scoped_creds)
    
    return client.open_by_key(st.secrets["config"]["SHEET_ID"]).get_worksheet(0)

st.title("График дежурства")

# Чтение данных
sheet = get_sheet()
data = sheet.get_all_records()
db = {str(row.get('key', '')): str(row.get('name', '')) for row in data}

# Интерфейс
name_input = st.text_input("Введите имя:")
if st.button("Записаться на 10:00"):
    if name_input.strip():
        db['cell_10_00'] = name_input.strip()
        
        # Сохранение
        sheet.clear()
        sheet.append_row(['key', 'name'])
        sheet.append_rows([[k, v] for k, v in db.items()])
        st.success("Сохранено!")
        st.rerun()

st.write("Текущие данные:", db)
    
