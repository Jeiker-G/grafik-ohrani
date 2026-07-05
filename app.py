import streamlit as st
import gspread
import base64
import json
from google.oauth2.service_account import Credentials

# Твой ключ в формате Base64
ENCODED_KEY = "ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgInByb2plY3RfaWQiOiAiZ3JhZmlrLWJvdC01MDE1MjAiLAogICJwcml2YXRlX2tleV9pZCI6ICI0NmU4MzBiYjg1MTdlZTBlMzcyNzM1OTAzMDljZGY2N2ExMDVhZDlhIiwKICAicHJpdmF0ZV9rZXkiOiAiLS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tXG5NSUlFdXdJQkFEQU5CZ2txaGtpRzl3MEJBUUVGQUFTQ0JLVXdnZ1NoQWdFQUFvSUJBUUM3d3ViZkJqTElGYjdrXG5zbitWTzYrVCtSVGZoUkxFYktlakJBRy9yakFiZWJKUk1kYWZPZTBPL1BabXJyazJIWEpGQ1VCRDRpWTNPQkxUXG5IUTlNUzlFTTJSSEFRbytsTHlnNXVBRkkvWm1SSXUxaGxXSjdGNzRWZGs4bk5NVUNUdnQ2ZjM4RWRmTlJVZENiXG5zYnRuWHJ6cWtTYzZ5cWJKUFF4Skdsbk8xMWRSdkRPSktCaVVnMWFkUXdZTnRSWGExMWExK0ozSVpwbXg0a082XG5ocTc4SVJSTDA3WkhpclQvUEpibkRxa0RYbFpaRldSVjVxNTlYa2RIZTRJdmhBWVdPM2pvMnJiK1o1QkgwK01KXG50aC92VXZWTDQ0Smg0dWdudXdUY1BLS3cwYWw0d3ZORFRPNEI4Ly9nSlBuZGtJSGlNajN6bGdoOTVoYk1tUEREXG5CcnN5bTVYSkFnTUJBQUVDZ2Y4Rmh6VWhFYmkzTlBpcFJGQmVPWXNnZ25Ic09zSEpJUTd0bGs2Rk9ydjlvRUsyXG5nMkE5a0lIUCtlemVCZk15UHdIVlVLL1F0cm4wRmhxaTJaM2Q0SnZKZWJBeE1TdGlFQzJqelM4d2lodmYzclcrXG4wbk8xVk1NQ0xiYVNqdGgrcjFYVTNXaUlwTUNMTlNRS3U2ZFUxOWlGMkhoMFRYSnBjTlJZb1p5am1yT0JCdzV5XG5NZFM0NmlnTFgrR2tMUHlJY3htamp3WHJGTW1tbG5ENHdJSmJsVUp0TmZ1VTI2M0EyVkN6WnlZZ0hPT0VpSUJmXG5Zb21sWXpiQy9PWmF5L0ZTQ0VKZk9sQXJETlc1Nzdpd05HYVgrYUtySGxWUWJaZXFnMWFPZWVreHppOFRMa0JlXG5jNFZLblp4TXorYXFRYnAybFhsZWhvOXBUNEZST2puV0N3bVY3bzhDZ1lFQStSMGlLcm12T3ZpM2FBYXd2cGJQXG5DLzZBb2dmLzlqTENJcUtkS2NrQ0NreFkwZnB5SUNlbzNWVTFvRnc4SW1jdFNYYjlHVituQlZQdE1kK3RacUdpXG5JcXc0SGc2VExGKzlGQjNwM0RnRjlDRjVNZDhMeFhFN0k5cWIvaTdWQi83b3V4bURoakN3L3V4d1RLWWt0WEhKXG5UNXEzVE1BYjF2dWtHM2dmMncyYVJGTUNnWUVBd1BPYXdUaGc0RDdmRkF1OStsQmNmUW1HQUlCam5FRUVqK3U3XG5xcnpEbTY4UmtsRTdPd2xFbEtZTndFVU1JdmtBWHlRcEdUa0RsNnBjWThqRXYxamlCR3VUdlNwR2p3em12MnE4XG5ZbDhsZTJxanRkVmhoMCs1Q0JENjhXVmZXZFhtOFBaMnFFTll2ZnRwU0x2N1BlZkp6MmRTY3ZoTXNDQXdUMmVKXG5rRGxvK2ZNQ2dZQkkvVEkvbG53ektTQ0R5RUlNOVo3Z2dzY3Bzbkphcm5DWE9WSVhKaUFFNkcyMXlFMmNBa0xGXG41dXQ1ZXN6YnY2TlRQUnZYVFdGZ2ZFQ3BOa0pXS2RHWm15QXVIbE1jMDBoUkZwcW92WGx4R0VXc1NRL24zODlXXG5KLzFBc25RVWphbWUrRkREQm8wMWhBMDdTQXJGWnZ0MjZYdi9idUk1VVMyNkpxNGV2cE9PcFFLQmdRQ2NxN0MyXG52MjU1NXRMLzFlRDJSUlkwT08xanJ0d3kzZUEwZERhM2xmcEdpVXA5UWhRVUJaeDREclVQcjRFQlRLbnVsdEFBXG5PUGtmeHlhcHB6V0tJVU8wVHgxdzljakJFcnF5SnBxOFRZR0R5cjBQUWltazB5anMwY3pSQVgwQTF0eGtQOXR0XG5HUElQb1BxR0lvMElZUkxPbzVpZzNkaDNFa3ZuemF3M1BVWnQzUUtCZ0VVak9HU2pjTFBEdTBkQ3F3T3psckZ4XG54K09UcEs1RjJlVnJhRTlnVlBGbzlzSVZMS3pESHQ3V01xU1BHbm9Sa0dxd0VHbzlwUW1wYUYvVjZhaHNzVkNRXG53VXEvSmhDSW9SUVhmaS9WdHBhSm5UT0lnZWh1WGdlUURKRE84YnlWcjYwVXhaK3pLZWZRTTRvUzBjT01uTzQxXG5xWWZwUXlMUVRacWZTbUtpWVcvTVxuLS0tLS1FTkQgUFJJVkFURSBLRVktLS0tLVxuIiwKICAiY2xpZW50X2VtYWlsIjogIm15LWdyYWZpay1hcHBAZ3JhZmlrLWJvdC01MDE1MjAuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLAogICJjbGllbnRfaWQiOiAiMTEyMzg4MTc4MjQ2NjU3NTI4NzY5IiwKICAiYXV0aF91cmkiOiAiaHR0cHM6Ly9hY2NvdW50cy5nb29nbGUuY29tL28vb2F1dGgyL2F1dGgiLAogICJ0b2tlbl91cmkiOiAiaHR0cHM6Ly9vYXV0aDIuZ29vZ2xlYXBpcy5jb20vdG9rZW4iLAogICJhdXRoX3Byb3ZpZGVyX3g1MDlfY2VydF91cmwiOiAiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vYXV0aDIvdjEvY2VydHMiLAogICJjbGllbnRfeDUwOV9jZXJ0X3VybCI6ICJodHRwczovL3d3dy5nb29nbGVhcGlzLmNvbS9yb2JvdC92MS9tZXRhZGF0YS94NTA5L215LWdyYWZpay1hcHAlNDBncmFmaWstYm90LTUwMTUyMC5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsCiAgInVuaXZlcnNlX2RvbWFpbiI6ICJnb29nbGVhcGlzLmNvbSIKfQoK"

@st.cache_resource(ttl=600)
def get_sheet():
    creds_json = base64.b64decode(ENCODED_KEY).decode('utf-8')
    creds_dict = json.loads(creds_json)
    
    creds = Credentials.from_service_account_info(creds_dict)
    scoped_creds = creds.with_scopes([
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ])
    client = gspread.authorize(scoped_creds)
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

st.title("График дежурства")
db = load_data()
name_input = st.text_input("Введите имя:", key="name_in")

if st.button("Записаться на 10:00"):
    if name_input.strip():
        db['cell_10_00'] = name_input.strip()
        save_data(db)
        st.success("Сохранено!")
        st.rerun()
    else:
        st.warning("Введите имя!")

st.write("Текущие данные:", db)
