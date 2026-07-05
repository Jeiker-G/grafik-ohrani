import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Настройка страницы для предотвращения "черного экрана" при ошибках
st.set_page_config(page_title="График", layout="centered")

@st.cache_resource(ttl=600)
def get_sheet():
    # Собираем данные из secrets без всяких .replace()
    # Считаем, что в Secrets ключ вставлен как тройные кавычки """..."""
    creds_dict = {
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": st.secrets["private_key"], 
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"]
    }
    
    creds = Credentials.from_service_account_info(creds_dict)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    client = gspread.authorize(creds.with_scopes(scope))
    return client.open_by_key(st.secrets["SHEET_ID"]).get_worksheet(0)

# Интерфейс
st.title("График дежурства")

try:
    sheet = get_sheet()
    records = sheet.get_all_records()
    db = {str(row.get('key', '')): str(row.get('name', '')) for row in records}
    
    name_input = st.text_input("Введите имя:", key="name_in")
    
    if st.button("Записаться на 10:00"):
        if name_input.strip():
            db['cell_10_00'] = name_input.strip()
            # Обновляем лист
            sheet.clear()
            sheet.append_row(['key', 'name'])
            sheet.append_rows([[k, v] for k, v in db.items()])
            st.success("Сохранено!")
            st.rerun()
            
    st.write("Текущие данные:", db)

except Exception as e:
    # Выводим ошибку на экран, чтобы вместо черного экрана видеть причину
    st.error(f"Критическая ошибка: {e}")
    st.info("Проверьте формат ключа в Secrets и доступ к таблице.")
    
