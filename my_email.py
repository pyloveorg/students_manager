from flask_mail import Message
from main import app, mail


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=None
    )
    mail.send(msg)