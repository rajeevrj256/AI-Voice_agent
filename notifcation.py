import smtplib
import datetime
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()

# SMTP Setup (Use App Password for Gmail)

def send_appointment_notification(response_data, recipient_email):
    """Sends an email notification after an appointment booking."""
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
    
    # Current timestamp
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Extract details from response
    appointment_date = response_data.get("date", "N/A")
    appointment_time = response_data.get("time", "N/A")
    purpose = response_data.get("purpose", "N/A")

    email_subject = f"📅 Appointment Confirmation: {purpose}"

    email_body = f"""
    Hello,

    Your appointment has been successfully booked.

    📅 Date: {appointment_date}
    ⏰ Time: {appointment_time}
    🎯 Purpose: {purpose}
    📩 Notification Sent At: {current_time}

    If you need any modifications or further assistance, feel free to reach out.

    Best Regards,  
    BotMast
    """

    # Create email message
    msg = EmailMessage()
    msg.set_content(email_body)
    msg["Subject"] = email_subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email if recipient_email != "N/A" else SENDER_EMAIL  # Send to sender if no recipient

    try:
        # Send Email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"✅ Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# Example LLM Response
# llm_response = {
#     "date": "21-02-2025",
#     "time": "5:00 PM",
#     "purpose": "Appointment for Dan",
#     "email": "rjrajeev5918@gmail.com"  # Replace with actual email
# }

# # Send Email Notification
# send_appointment_notification(llm_response, llm_response["email"])
