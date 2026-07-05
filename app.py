import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. Скрываем все настройки в одном месте
def get_sheet():
    # Используем ваш JSON (вставлен как словарь)
    creds_dict = {
        "type": "service_account",
        "project_id": "grafik-bot-501520",
        "private_key_id": "46e830bb8517ee0e37273590309cdf67a105ad9a",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQC7wubfBjLIFb7k\nsn+VO6+T+RTfhRLEbKejBAG/rjAbebJRMdafOe0O/PZmrrk2HXJFCUBD4iY3OBLT\nHQ9MS9EM2RHAQo+lLyg5uAFI/ZmRIu1hlWJ7F74Vdk8nNMUCTvt6f38EdfNRUdCb\nsbtnXrzqkSc6yqbJPQxJGlnO11dRvDOJKBiUg1adQwYNtRXa11a1+J3IZpmx4kO6\nhq78IRRL07ZHirT/PJbnDqkDXlZZFWRV5q59XkdHe4IvhAYWO3jo2rb+Z5BH0+MJ\nth/vUvVL44Jh4ugnuwTcPKKw0al4wvNDTO4B8//gJPndkIHiMj3zlgh95hbMmPDD\nBrsym5XJAgMBAAECgf8FhzUhEbi3NPipRFBeOYsggnHsOsHJIQ7tlk6FOrv9oEK2\ng2A9kIHP+ezeBfMyPwHVUK/Qtrn0Fhqi2Z3d4JvJebAxMStiEC2jzS8wihvf3rW+\n0nO1VMMCLbaSjth+r1XU3WiIpMCLNSQKu6dU19iF2Hh0TXJpcNRYoZyjmrOBBw5y\nMdS46igLX+GkLPyIcxmjjwXrFMmmlnD4wIJblUJtNfuU263A2VCzZyYgHOOEiIBf\nYomlYzbC/OZay/FSCEJfOlArDNW577iwNGaX+aKrHlVQbZeqg1aOeekxzi8TLkBe\nc4VKnZxMz+aqQbp2lXleho9pT4FROjnWCwmV7o8CgYEA+R0iKrmvOvi3aAawvpbP\nC/6Aogf/9jLCIqKdKckCCkxY0fpyICeo3VU1oFw8ImctSXb9GV+nBVPtMd+tZqGi\nIqw4Hg6TLF+9FB3p3DgF9CF5Md8LxXE7I9qb/i7VB/7ouxmDhjCw/uxwTKYktXHJ\nT5q3TMAb1vukG3gf2w2aRFMCgYEAwPOawThg4D7fFAu9+lBcfQmGAIBjnEEEj+u7\nqrzDm68RklE7OwlElKYNwEUMIvkAXyQpGTkDl6pcY8jEv1jiBGuTvSpGjwzmv2q8\nYl8le2qjtdVhh0+5CBD68WVfWdXm8PZ2qENYvftpSLv7PefJz2dScvhMsCAwT2eJ\nkDlo+fMCgYBI/TI/lnwzKSCDyEIM9Z7ggscpsnJarnCXOVIXJiAE6G21yE2cAkLF\n5ut5eszbv6NTPRvXTWFgfECpNkJWKdGZmyAuHlMc00hRFpqovXlxGEWsSQ/n389W\nJ/1AsnQUjame+FDDBo01hA07SArFZvt26Xv/buI5US26Jq4evpOOpQKBgQCcq7C2\nv2555tL/1eD2RRY0OO1jrtwy3eA0dDa3lfpGiUp9QhQUBZx4DrUPr4EBTKnultAA\nOPkfxyappzWKIUO0Tx1w9cjBErqyJpq8TYGDyr0PQimk0yjs0czRAX0A1txkP9tt\nGPIPoPqGIo0IYRLOo5ig3dh3Ekvnzaw3PUZt3QKBgEUjOGSjcLPDu0dCqwOzlrFx\nx+OTpK5F2eVraE9gVPFo9sIVLKzDHt7WMqSPGnoRkGqwEGo9pQmpaF/V6ahssVCQ\nwUq/JhCIoRQXfi/VtpaJnTOIgehuXgeQDJDO8byVr60UxZ+zKefQM4oS0cOMnO41\nqYfpQyLQTZqfSmKiYW/M\n-----END PRIVATE KEY-----",
        "client_email": "my-grafik-app@grafik-bot-501520.iam.gserviceaccount.com",
        "client_id": "112388178246657528769",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/my-grafik-app%40grafik-bot-501520.iam.gserviceaccount.com"
    }
    
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open_by_key(st.secrets["SHEET_ID"]).get_worksheet(0)

# Интерфейс
st.title("График дежурства")
sheet = get_sheet()
data = sheet.get_all_records()
db = {str(row.get('key', '')): str(row.get('name', '')) for row in data}

name_input = st.text_input("Введите имя:", key="name_in")
if st.button("Записаться на 10:00"):
    db['cell_10_00'] = name_input
    sheet.clear()
    sheet.append_row(['key', 'name'])
    sheet.append_rows([[k, v] for k, v in db.items()])
    st.rerun()

st.write("Данные:", db)
