import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

@st.cache_resource(ttl=600)
def get_sheet():
    creds_dict = st.secrets["gcp_service_account"].to_dict()
    # Удаляем попытку замены, так как TOML должен передать ключ целиком
    creds = Credentials.from_service_account_info(creds_dict)
    
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    client = gspread.authorize(creds.with_scopes(scope))
    
    return client.open_by_key(st.secrets["config"]["SHEET_ID"]).get_worksheet(0)

# ... остальной интерфейс (инпут и кнопка) остается прежним ...
st.title("График дежурства")
try:
    sheet = get_sheet()
    db = {str(row.get('key', '')): str(row.get('name', '')) for row in sheet.get_all_records()}
    name_input = st.text_input("Введите имя:", key="name_in")
    if st.button("Записаться на 10:00"):
        if name_input.strip():
            db['cell_10_00'] = name_input.strip()
            sheet.clear()
            sheet.append_row(['key', 'name'])
            sheet.append_rows([[k, v] for k, v in db.items()])
            st.success("Сохранено!")
            st.rerun()
    st.write("Текущие данные:", db)
except Exception as e:
    st.error(f"Ошибка: {e}")
        
