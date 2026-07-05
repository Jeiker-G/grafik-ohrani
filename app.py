import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# 1. Настройка подключения (берет данные из Secrets)
@st.cache_resource
def get_sheet():
    creds_dict = st.secrets["gcp_service_account"]
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open_by_key(st.secrets["SHEET_ID"]).sheet1

# 2. Функция загрузки данных
def load_data():
    sheet = get_sheet()
    data = sheet.get_all_records()
    # Возвращаем словарь, где key — это ключ, а name — имя
    return {str(row['key']): str(row['name']) for row in data}

# 3. Функция сохранения данных
def save_data(db):
    sheet = get_sheet()
    rows = [[k, v] for k, v in db.items()]
    sheet.clear()
    sheet.append_row(['key', 'name'])
    if rows:
        sheet.append_rows(rows)

# --- ИНТЕРФЕЙС ---
st.title("График дежурства")

# Загружаем текущие данные
db = load_data()

# Пример ввода и кнопки
name_input = st.text_input("Введите имя:", key="name_in")

if st.button("Записаться на 10:00"):
    # Сюда записываем ключ и значение
    db['cell_10_00'] = name_input.strip()
    # Сохраняем весь словарь обратно в таблицу
    save_data(db)
    st.success("Сохранено в Google Таблицу!")
    st.rerun()

st.write("Текущие данные:", db)
st.title("График дежурства")

# Получаем актуальные данные из Google Sheets
db = load_data()

# Пример того, как ты рисуешь кнопку (используй свой стиль)
# Допустим, у тебя есть пост "10:00" с ключом "cell_10_00"
name_input = st.text_input("Введите имя:", key="name_in")

if st.button("Записаться на 10:00"):
    save_data("cell_10_00", name_input)
    st.success("Сохранено в Google Таблицу!")
    st.rerun() # Перезагрузка, чтобы сразу увидеть результат

st.write("Текущие данные в таблице:", db)
            db[key] = new_name.strip()
            
        save_db(db)
        st.rerun()

# CSS для красоты
st.markdown("""
    <style>
    .time-box { background: #E3F2FD; border-radius: 8px; padding: 8px; text-align: center; font-weight: 700; border: 1px solid #90CAF9; color: #1565C0; margin-top: 10px; font-size: 0.9rem; }
    .stButton > button { width: 100%; height: 40px !important; }
    </style>
""", unsafe_allow_html=True)

st.title("График дежурства")

# Основной цикл
db = load_db()

def get_slots(is_stroyka):
    if is_stroyka:
        return ["00:00-02:00", "02:00-04:00", "04:00-06:00", "06:00-07:30", "07:30-17:30", "17:30-20:00", "20:00-22:00", "22:00-00:00"]
    else:
        return ["00:00-02:00", "02:00-04:00", "04:00-06:00", "06:00-08:00", "08:00-10:00", "10:00-12:00", 
                "12:00-14:00", "14:00-16:00", "16:00-18:00", "18:00-20:00", "20:00-22:00", "22:00-00:00"]

cols = st.columns(7)
days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

for d_idx, day in enumerate(days):
    with cols[d_idx]:
        st.markdown(f"### {day}")
        is_stroyka = 1 <= d_idx <= 5
        slots = get_slots(is_stroyka)
        
        for i, slot in enumerate(slots):
            st.markdown(f"<div class='time-box'>{slot}</div>", unsafe_allow_html=True)
            
            if is_stroyka and i == 4:
                st.button("Стройка", key=f"stroyka_{d_idx}_{i}")
            else:
                for post in [1, 2]:
                    key = f"cell_{d_idx}_{i}_{post}"
                    val = db.get(key)
                    
                    is_occupied = val is not None and val != "nan" and str(val).strip() != ""
                    btn_text = str(val) if is_occupied else "Свободно"
                    
                    if st.button(btn_text, key=key, type="primary" if is_occupied else "secondary"):
                        edit_cell(key)
