import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Собираем ключ по частям, чтобы обойти ограничение длины в Secrets/Интерфейсе
key_part1 = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC/7fZGnjRucUko"
key_part2 = "\nHoptFkIBvmYPzbwyztmGSdu6r9wCksUNd+7jqS5W2HN/HX2FXzcG8C2JqwFu750Z"
key_part3 = "\nbQ70BObRoikNEhk1B9MHoyiWk/gvceY/k9Z4dhBLxqEtIo2DeDTN0v4i01eB685/"
key_part4 = "\nxCfKf9Xko87voxx7ABeXgPDSduzNidHyXZG7GeVF0Gou2RUf2v5wD8M8/+/rKe/O"
key_part5 = "\nb4/rGeeDNfmNuxxTXazgSUWltpNvWO8McTGmuiNcZiGsObeXLCiWFOpP6wKDxJS0"
key_part6 = "\nxqt3uuhFmGrc8Sk/Sl8bSafWGdRoQJ88u7ih4nMUfFmvle9/Azb/0CX94+ioG6H5"
key_part7 = "\nTIs80JlBAgMBAAECggEAJRoeOqaIojT6HGxS/CWKWwXweuudjwDXohMTC/LFCCZR"
key_part8 = "\nO3pMzuu8joNHSHJt+mNeotO5KdzJ6SUe7HRdqKRt7mZ3oxQ1lT/O9rH+vaUbHCjb"
key_part9 = "\nhrzQf/bqzYs3Sx9b1edd5c/82sSaLP5lq+NCge3Wbl2QOlkAv3JUHTCK3VSqEE1X"
key_part10 = "\nNUK2Yx0s93DXSq6skHm/kFjoTFrfR+lj8+PKgzGHa7in9J3RWr46PMSKiP07vlTN"
key_part11 = "\nqMJkHVv9eS6uFtJKc3CGFDsL3JI0iVrD/eAysPVbqkwMn5b5k7IoBQ2VEGUQN1I/"
key_part12 = "\ngAVgVGxDTYFyjqOUFNsPxosuebzBmWVIQwelrqNJ8QKBgQDv8xqiKSzHoU81k2Dx"
key_part13 = "\n4CNJleXhSdP0pTqbYz0g55/3Rmvr+nFlegBsmGm4YMVEVBtzJtQ8grPR7DFBH6Uq"
key_part14 = "\naW82ED7rgxMeSwNdOn2u5nNmscSjeF/b68LFilyj9t6unwZEahMdfUcr4JIup90H"
key_part15 = "\niJ+0ZxH6S1WlEKl263321gAJHQKBgQDMxI/zeTOyT9Jm3wqhzRP9eTjXwqbd0OdZ"
key_part16 = "\nzuw6IfexcyoKuH5F0jME7vfA4xDGwnsYPu0Zrf6fabJldZjzeJB7XkS6C00b5nyb"
key_part17 = "\njIxYOO8mP+oHNpXDrycZERsLOkzv/N3+OtjvAVqaCQAhsWA5Xezsgiw3cHRfT++9"
key_part18 = "\nfIBs88H7dQKBgQCxbBV2cHGvDuSt3dLiJnSRNahsBBYYoJAMU73gdcR/p++m5mEw"
key_part19 = "\nwpxLsAsEDXHvyy0c4UovkAl8oGPvHoIXMSzNUgfkRuA9FwRezCAg0j/kYG/g2+It"
key_part20 = "\nkE9Nl7hWePVBM08ECVcnB/o3RG9y1iaGKozEbS4K3+dtDTvxNcHHYYdXNQKBgBgv"
key_part21 = "\nu4UZstaEASkvfTUBYTQWZnVtw4H90+XSwCpZqsUmAjhD9H5Qxr/1bgQ1jdy8Sgfi"
key_part22 = "\nHuVinOm9dVnwmwFfI0m/J8UF4rTB88P3xPgCuZS+BemWM/hqLucSEyyvVTkfmCUY"
key_part23 = "\nfVFlewpHhMEfKiMAd7Qc+lPRzbvt3GK08EHtOC4KlAoGBAKhNcXyIpn8NgnIHIQ3z"
key_part24 = "\n5F69gI0fRX+blojyIpH7eT1MYsPprdnp3I99zVlWYz6jh3jWybuIm8/jRCUgYxNh"
key_part25 = "\nFQYXw+mNL9fH50ypQE3ynm1XRY8fBsMe4ZP8DVrB9f11//W21bR/VddurZHYKo5e"
key_part26 = "\nKcb2RRe4beponiFbMMhMmybA\n-----END PRIVATE KEY-----"

FULL_KEY = key_part1 + key_part2 + key_part3 + key_part4 + key_part5 + key_part6 + key_part7 + key_part8 + key_part9 + key_part10 + key_part11 + key_part12 + key_part13 + key_part14 + key_part15 + key_part16 + key_part17 + key_part18 + key_part19 + key_part20 + key_part21 + key_part22 + key_part23 + key_part24 + key_part25 + key_part26

@st.cache_resource(ttl=600)
def get_sheet():
    creds_dict = {
        "type": st.secrets["type"],
        "project_id": st.secrets["project_id"],
        "private_key_id": st.secrets["private_key_id"],
        "private_key": FULL_KEY,
        "client_email": st.secrets["client_email"],
        "client_id": st.secrets["client_id"],
        "auth_uri": st.secrets["auth_uri"],
        "token_uri": st.secrets["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["client_x509_cert_url"]
    }
    creds = Credentials.from_service_account_info(creds_dict)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    return gspread.authorize(creds.with_scopes(scope)).open_by_key(st.secrets["SHEET_ID"]).get_worksheet(0)

st.title("График дежурства")
try:
    sheet = get_sheet()
    st.write("Подключение успешно!")
except Exception as e:
    st.error(f"Ошибка: {e}")
    
