import streamlit as st
import re
from mailer_service import Mailer
from config import GmailConfig, YOUR_DOMAIN_NAME

mailer = Mailer(
    your_email=GmailConfig.EMAIL,
    your_password=GmailConfig.PASSWORD,
    host=GmailConfig.HOST,
    port=GmailConfig.PORT
)

st.header("Contact Us")

with st.form(key="Email_form"):
    options = ["Freelance", "Teach", "Report an issue", "Other"]
    topic = st.selectbox("What topic do you want to discuss?", options)

    user_email = st.text_input("Enter your email")
    user_message = st.text_area("Enter your message")

    button = st.form_submit_button("Submit")

    if button and not re.match(r"[^@]+@[^@]+\.[^@]+", user_email):
        st.warning("Please enter a valid email address")

    elif button and re.match(r"[^@]+@[^@]+\.[^@]+", user_email):
        mailer.send_email(
            receiver=GmailConfig.EMAIL,
            subject=f"New email from {user_email} via {YOUR_DOMAIN_NAME}. Topic: {topic}",
            body=user_message
        )

        if mailer.status:
            st.success("Email sent successfully")
            mailer.flush_last_email_metadata()
        else:
            st.error(f"Email wasn't sent. Reason: {mailer.reason}")
            mailer.flush_last_email_metadata()
