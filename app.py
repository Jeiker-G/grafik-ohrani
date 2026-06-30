import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")
DATA_FILE = "schedule_v46.csv"

def load_db():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        return {str(row['key']): str(row['name']) for _, row in df.iterrows()}
    return {}

def save_db(db):
    df = pd.DataFrame([{"key": k, "name": v} for k, v in db.items()])
    df.to_csv(DATA_FILE, index=False)

@st.dialog("Запись на дежурство")
def edit_cell(key):
    db = load_db()
    new_name = st.text_input("Имя:", value=db.get(key, ""))
    if st.button("Записаться"):
        if new_name.strip():
            db[key] = new_name.strip()
            save_db(db)
            st.rerun()

# CSS для красоты
st.markdown("""
    <style>
    .time-box { background: #E3F2FD; border-radius: 8px; padding: 8px; text-align: center; font-weight: 700; border: 1px solid #90CAF9; color: #1565C0; margin-top: 10px; font-size: 0.9rem; }
    .stButton > button { width: 100%; height: 40px !important; }
    /* Стройка оранжевая */
    .st-emotion-cache-1r6slp { background-color: #FF9800 !important; color: white !important; border: none !important; }
    </style>
""", unsafe_allow_html=True)

st.title("График дежурства")
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
            
            # Индекс 4 в списке стройки — это 07:30-17:30
            if is_stroyka and i == 4:
                st.button("Стройка", key=f"st_{d_idx}_{i}")
            else:
                for post in [1, 2]:
                    key = f"{d_idx}_{i}_{post}"
                    val = db.get(key)
                    if st.button(val if val else "Свободно", key=key, type="primary" if val else "secondary"):
                        edit_cell(key)
                      
