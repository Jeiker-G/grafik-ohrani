import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import textwrap

# --- 1. Настройка параметров подключения ---
# Используем разбитый ключ для обхода лимитов Secrets
# Если вы используете разбитый ключ (pk1-pk4), убедитесь что они в Secrets
def get_creds():
    # Собираем ключ из переменных secrets
    full_body = st.secrets["pk1"] + st.secrets["pk2"] + st.secrets["pk3"] + st.secrets["pk4"]
    formatted_body = "\n".join(textwrap.wrap(full_body, 64))
    pem_key = f"-----BEGIN PRIVATE KEY-----\n{formatted_body}\n-----END PRIVATE KEY-----"
    
    return {
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

@st.cache_resource(ttl=600)
def get_sheet():
    creds = Credentials.from_service_account_info(get_creds())
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    client = gspread.authorize(creds.with_scopes(scope))
    return client.open_by_key(st.secrets["SHEET_ID"]).get_worksheet(0)

# --- 2. Логика интерфейса ---
st.set_page_config(page_title="График дежурства", page_icon="📅")
st.title("📅 График дежурства")

try:
    sheet = get_sheet()
    data = sheet.get_all_records()
    
    # Преобразуем список словарей в удобный словарь для работы
    # Ожидаем в таблице заголовки "key" и "name"
    db = {str(row.get('key', '')): str(row.get('name', '')) for row in data}
    
    st.subheader("Регистрация")
    name_input = st.text_input("Введите ваше имя:", key="name_in")
    
    if st.button("Записаться на 10:00"):
        if name_input.strip():
            db['cell_10_00'] = name_input.strip()
            
            # Перезапись данных в таблицу
            sheet.clear()
            sheet.append_row(['key', 'name'])
            sheet.append_rows([[k, v] for k, v in db.items()])
            
            st.success("Запись обновлена!")
            st.rerun()
        else:
            st.warning("Введите имя!")

    st.divider()
    st.write("### Текущие записи:")
    st.table(db)

except Exception as e:
    st.error(f"Ошибка работы с таблицей: {e}")
    
