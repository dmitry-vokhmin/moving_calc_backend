import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_ADDRESS, EMAIL_PASSWORD


def send_email(user_email, one_time_password, user_name):
    sender_email = EMAIL_ADDRESS
    receiver_email = user_email
    password = EMAIL_PASSWORD

    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset"
    message["From"] = sender_email
    message["To"] = receiver_email

    html = f"""\
    <html>
        <body>
            <p style="color: #0915CC; font-size: 16px; font-family: Inter;">Calculator</p>
            <hr style="height:2px; color:rgba(181, 184, 199, 0.2);border-width:0;background-color:rgba(181, 184, 199, 0.2)">
            <h1 style="color: #0915CC; font-size: 24px; font-family: Arial; font-weight: bold; margin-top: 54px;">
            Password Reset
            </h1>
            <p style="color: #757C9F;font-size: 15px;font-family: Arial;">Hello, {user_name}</p>
            <p style="color: #757C9F;font-size: 15px;font-family: Arial;">Forgotten your password? No worries, here’s a 
            one-time password to access your account:</p>
            <div style="border: 1px solid #0915CC;border-radius: 10px;box-sizing: border-box;padding: 14px 15px;
            width: 144px;height: 48px;text-align: center;font-family: Inter;color: #070808;font-size: 16px;">
            {one_time_password}</div>
            <p style="color: #757C9F;font-size: 15px;font-family: Arial;">Enter the one-time above in the app 
            password (copy and paste works well too). We’ll then ask you to create a new password so that only you 
            will know your login details.</p>
            <p style="color: #757C9F;font-size: 15px;font-family: Arial;">If you did not equest a new password,
             please let us know immediately by replying to this email.</p>
            <p style="color: #757C9F;font-size: 15px;font-family: Arial;margin-top: 40px;"> — The Calculator team</p>
            <hr style="height:2px; color:rgba(181, 184, 199, 0.2);border-width:0;
            background-color:rgba(181, 184, 199, 0.2);margin-top: 40px;margin-bottom: 23px;">
            <p style="color: #757C9F;font-size: 10px;font-family: Arial;">
            Calculator, 8502 Preston Rd. Inglewood, Maine 98380</p>
        </body>
    </html>
    """

    html_text = MIMEText(html, "html")
    message.attach(html_text)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
