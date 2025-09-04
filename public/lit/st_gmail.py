# GMail Clean
# ===========

from itertools import count
import streamlit as st
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 1) OAuth2 scope to read your mail
# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SCOPES = ['https://mail.google.com/']

CLIENT_SECRET = "client_secret.json"

# Select ``start_date`` and ``end_date``.

min_date = datetime.date(1997, 1, 1)

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start date", max_value="today", min_value=min_date, value=datetime.date(2006, 12, 1))
with col2:    
    end_date = st.date_input("End date", max_value="today", min_value=min_date, value=datetime.date(2006, 12, 31))

# Calculate time interval between start_date and end_date

if start_date and end_date:
    
    # If ``end_date`` is less than ``start_date`` then swap dates.
    if end_date < start_date:
        start_date, end_date = end_date, start_date
    
    time_interval = end_date - start_date
    st.write(f"Time interval: {time_interval.days} days")

# Google Cloud authentication

def authenticate():
    # If you have a token.json from a previous run, it’ll be used.
    creds = None
    try:
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    except FileNotFoundError:
        pass

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save for next time
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

# Counts messages matching the Gmail search
# after ``start_date`` and before ``end_date``.
# Dates are in ``YYYY/MM/DD`` format.
#
# ::

def count_messages_in_interval(service, start_date, end_date, user_id='me'):
    query = f'after:{start_date} before:{end_date}'
    message_ids = []
    request = service.users().messages().list(userId=user_id, q=query)
    while request is not None:
        response = request.execute()
        messages = response.get('messages', [])
        message_ids.extend([msg['id'] for msg in messages])
        # Fetch next page, if any
        request = service.users().messages().list_next(request, response)
    return message_ids


def delete_messages(service, message_ids):
    # Gmail API allows deleting up to 1000 emails at once (batch delete)
    batch_size = 1000
    st.write(f"Deleting {len(message_ids)} emails.")
    for i in range(0, len(message_ids), batch_size):
        ids = message_ids[i:i+batch_size]

        # Delete batch of emails
        service.users().messages().batchDelete(
            userId='me',
            body={'ids': ids}
        ).execute()
        st.info(f"Deleted {len(ids)} emails.")

# main

svc = authenticate()

message_ids = []

if "message_ids" in st.session_state:
    message_ids = st.session_state.message_ids

if st.button("Count", use_container_width=True):
    message_ids = count_messages_in_interval(svc, start_date, end_date)
    st.session_state.message_ids = message_ids
    st.info(f'You have {len(message_ids)} messages between the dates specified.')

if st.sidebar.button("Delete", type="primary", disabled=len(message_ids)==0):
    delete_messages(svc, message_ids)
    st.success("Deletion process completed.")