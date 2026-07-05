import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Настройка подключения к Google Sheets
@st.cache_resource(ttl=600)
def get_sheet():
    # Данные сервисного аккаунта (вставлены напрямую в код для стабильности)
    creds_dict = {
        "type": "service_account",
        "project_id": "alien-airfoil-404006",
        "private_key_id": "20520e7376090739b8f6f7347be15ae1c9424b63",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDIRCt4MNkXGufS\nHLRqpSUMchwGcGxo9TOaYx1KP71KRq1M/nwWl7Jjq5GM6dHSvi1saxHU0HWLX6/4\nZoXErxcm8wlN29W2P2cJSqEVcd0WhgRkTP0Jexul9a9kNfo6X0Zn7C1cmk+9oJX6\nGoGKjew9+0c6WyIIdCXDj3ykfu2rlLR9BaM4t+pM56sKFEGhdta1eF/MB6NvAa9e\nKJ82Bpb14kWsp882EKTTO/VU0zvNcxktvMJYsR1DHzCL9cKmBJsZ1qhdwW+10eZJ\nnvJhLzuDEW2a4Y8Cyqrw9/hcBC9UsrD7m57jN3KxU9+NuGgUYdL2pAOVEbqk9ei4\n41oI8bL3AgMBAAECggEAA63I59c4R0xHVOmremGlQBWUJGqKFOJOokS1PYkIagxi\n7TN0xeXfsSTUmPRhb9y7F3ve1hXfcU6x/CV5/WZ2Z1Dda2PUVbNtdtMhowC2XhsN\n8P+/Dp6hBksjzGEqqX0/KfQoBl4pUXAmDfQEGPtjCxjW5dOijB0CGPxFfsoVuJ1y\nEUg+RDzubYmlQkbMgDlrC7li4bcYLVUSjImy4sQP1OXlhdgo3OTuxebDBWc0o3R7\nhXuFqZTKKDti4qd0Xu/zSXR52YaPs0Wvk8x2GyXLKD52cR0xDr1WlU5uqja1HVNF\nuO1Aj0SspserxnCY+u2qvHrujwmj8hz23I7u/AGBfQKBgQDyMmCGqGO7CYC9SkKD\n0yW5hlLKK/uPMLddplc/UgGcWVsmel2NSvM6bWAF3YiM8gRNQlaBiEisxwrMFm6W\nUtWMSNZMjKhhEqj9BeTnUH9LV+5aTbY216uLNIuflpoJzx09+N4Tz1PybQbcSo7C\n6yp8DXl9xeOwclKUC6h+31yWZQKBgQDTrggbgSr7V7cNk79fumNi5os/Wx0Xk3xL\nS0Zt2Pkio6U00D6U9wuKEwcN8fAnAiaGQ+803OZ22/5LkkTNXFKrmK4r4wrjwvPp\nAz7Q59a5G4Dq3KHFWoU63BUVoVXKaz19g/J+fCPSNSJ4+pKJjfS/WcRW/fCnTsoq\nJLbx7ZOwKwKBgCsQhBNNe7Y1IVwHCT6xW6LaXHwwR+GVEvWm7xqGNV0cklWMKnhG\nHGuGKS3Bz1bobZVjN0h++BUoqyXQ00cNYYU5KkmgNQxVqhCbbLEoogm+j9YkvUKR\nJKJy7GSq/abC2fs79hjlo5KWikK/SxUjhYFbT//qIOst2LsUO5iblLX1AoGANe1I\nM3mcsZuPDu5s+r5JQ5DoOKPFrZPtPmFW9/UmwyRdmi7TQrANSIfAbFUOkWGC3wG/\nlwAP1ogFKMuCq66xgPXMqXGV/KBV8y7YefAWS+It3aeHrvd4qZ4X4QLREFhxueA7\nju2hUpQmzBtJ6bE4gOcllePrwzPXXRUtZkTYMzECgYEAjGX8zFdTSRTrYq5OrcTI\nHl9AG4G4YqX10lnp4rSmT6EjmgoO/zegLe+4p3VtZmVEPBQ7UNosiTZibt9Ulfhu\njSwq7K0WK7p5irLira/XvZ/t5fsrbDHj5agtsctsSz9lw7hTxYbLM8GAiEH8LfGG\neRg+ZLOywdD4UPL8niSRa/c=\n-----END PRIVATE KEY-----",
        "client_email": "my-grafik-app@alien-airfoil-404006.iam.gserviceaccount.com",
        "client_id": "114155465166172575794",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/my-grafik-app%40alien-airfoil-404006.iam.gserviceaccount.com"
    }
    
    creds = Credentials.from_service_account_info(creds_dict)
    scoped_creds = creds.with_scopes([
        "https://www.googleapis.com/auth/spreadsheets", 
        "https://www.googleapis.com/auth/drive"
    ])
    client = gspread.authorize(scoped_creds)
    # Открываем таблицу по ID из Secrets
    return client.open_by_key(st.secrets["SHEET_ID"]).get_worksheet(0)

def load_data():
    sheet = get_sheet()
    data = sheet.get_all_records()
    return {str(row.get('key', '')): str(row.get('name', '')) for row in data}

def save_data(db):
    sheet = get_sheet()
    rows = [[k, v] for k, v in db.items()]
    sheet.clear()
    sheet.append_row(['key', 'name'])
    if rows:
        sheet.append_rows(rows)

# Интерфейс Streamlit
st.title("График дежурства")

db = load_data()
name_input = st.text_input("Введите имя:", key="name_in")

if st.button("Записаться на 10:00"):
    if name_input.strip():
        db['cell_10_00'] = name_input.strip()
        save_data(db)
        st.success("Сохранено!")
        st.rerun() # Обновляем страницу для отображения данных
    else:
        st.warning("Введите имя!")

st.write("Текущие данные:", db)
