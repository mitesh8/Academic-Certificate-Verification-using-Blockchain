import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

def send_email(to_addr, subject, body):
    # Gmail SMTP server and port
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Your Gmail account credentials
    username = 'verifiercertificate@gmail.com'
    password = 'replace with password'

    # Create message object
    message = MIMEMultipart()
    message['From'] = username
    message['To'] = to_addr
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Create SMTP connection
    smtp = smtplib.SMTP(smtp_server, smtp_port)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(username, password)

    # Send email and close connection
    smtp.sendmail(username, to_addr, message.as_string())
    smtp.quit()
