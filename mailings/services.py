import smtplib

from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


def send_mailing(client_list, message):
    """Функция отправки письма"""
    try:
        response = send_mail(
            message.subject,
            message.body,
            EMAIL_HOST_USER,
            client_list
        )
        return response
    except smtplib.SMTPException:
        raise smtplib.SMTPException