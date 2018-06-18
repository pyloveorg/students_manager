from flask_mail import Message
from app import mail


def send_email(to, subject, template):
    """ Send email to recipients. """

    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=None
    )
    mail.send(msg)

