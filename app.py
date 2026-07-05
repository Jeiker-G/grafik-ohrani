import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Настройка страницы
st.set_page_config(page_title="График дежурства", page_icon="📅")

@st.cache_resource(ttl=600)
def get_sheet():
    """
    Авторизация в Google Sheets через сервисный аккаунт.
    Данные берутся из Streamlit Secrets (настройки приложения).
    """
    # Собираем словарь учетных данных из Secrets
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
        "client_x509_cert_url": st.secrets["client_x509_cert_url"],
        "universe_domain": st.secrets.get("universe_domain", "googleapis.com")
    }
    
    # Создаем объект учетных данных
    creds = Credentials.from_service_account_info(creds_dict)
    
    # Авторизуемся в Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    client = gspread.authorize(creds.with_scopes(scope))
    
    # Открываем таблицу по ID и берем первый лист
    return client.open_by_key(st.secrets["SHEET_ID"]).get_worksheet(0)

# --- Интерфейс приложения ---
st.title("📅 График дежурства")

try:
    sheet = get_sheet()
    
    # Получаем данные из таблицы
    # Ожидается, что в таблице есть столбцы 'key' и 'name'
    data = sheet.get_all_records()
    db = {str(row.get('key', '')): str(row.get('name', '')) for row in data}

    st.subheader("Записаться на смену")
    name_input = st.text_input("Введите ваше имя:", key="name_in")
    
    if st.button("Записаться на 10:00"):
        if name_input.strip():
            # Обновляем данные в словаре
            db['cell_10_00'] = name_input.strip()
            
            # Перезаписываем лист таблицы
            sheet.clear()
            sheet.append_row(['key', 'name'])
            rows_to_append = [[k, v] for k, v in db.items()]
            sheet.append_rows(rows_to_append)
            
            st.success("Успешно сохранено!")
            st.rerun() # Перезагружаем страницу для обновления данных
        else:
            st.warning("Пожалуйста, введите имя.")

    st.divider()
    st.write("### Текущее расписание:")
    st.table(db)

except Exception as e:
    st.error(f"Произошла ошибка при подключении к таблице: {e}")
    st.info("Убедитесь, что вы предоставили доступ к Google Таблице почте сервисного аккаунта.")
    
