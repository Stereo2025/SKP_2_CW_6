import smtplib
from datetime import datetime, timedelta
from calendar import monthrange
from mailings.models import Mailing, Log
from mailings.services import send_mailing


def start_mailing():
    """Функция проверки и начала рассылок."""
    now = datetime.now()
    # Объедините дату и время в datetime для корректного сравнения
    current_datetime = datetime.combine(now.date(), now.time())
    mailing_list = Mailing.objects.filter(datetime__lte=current_datetime, status='created')

    for mailing in mailing_list:
        user = mailing.user
        mailing.status = 'started'
        mailing.save()

        clients = mailing.client.all()
        message = mailing.message
        response = None
        try:
            response = send_mailing(clients, message)
            mailing.status = 'completed'
        except smtplib.SMTPException as e:
            response = False
            log_message = str(e)
            mailing.status = 'failed'

        if mailing.periodisity:
            if mailing.periodisity == 'day':
                mailing.date += timedelta(days=1)
            elif mailing.periodisity == 'week':
                mailing.date += timedelta(weeks=1)
            elif mailing.periodisity == 'month':
                days_in_month = monthrange(now.year, now.month)[1]
                mailing.date += timedelta(days=days_in_month)

        log = Log.objects.create(
            time=now,
            status=response,
            server_response=log_message if not response else '',
            mailing=mailing,
            user=user
        )
        log.save()
        mailing.save()

