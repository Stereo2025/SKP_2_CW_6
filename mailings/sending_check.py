import smtplib
from datetime import datetime, timedelta
from calendar import monthrange
from mailings.models import Mailing, Log
from mailings.services import send_mailing


def start_mailing():
    """Функция проверки и начала рассылок."""
    now = datetime.now()
    current_datetime = datetime.combine(now.date(), now.time())
    lower_bound_time = current_datetime - timedelta(seconds=30)
    upper_bound_time = current_datetime + timedelta(seconds=30)
    mailing_list = Mailing.objects.filter(date__lte=now.date(),
                                          time__gte=lower_bound_time.time(),
                                          time__lte=upper_bound_time.time(),
                                          status__in=['created', 'started'])
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

# def start_mailing():
#     """Функция проверки и начала рассылок."""
#     now = datetime.now()
#     current_datetime = datetime.combine(now.date(), now.time())
#     lower_bound_time = current_datetime - timedelta(seconds=30)
#     upper_bound_time = current_datetime + timedelta(seconds=30)
#
#     mailing_list = Mailing.objects.filter(date__lte=now.date(),
#                                           time__gte=lower_bound_time.time(),
#                                           time__lte=upper_bound_time.time(),
#                                           status='created')
#     for mailing in mailing_list:
#         user = mailing.user
#         mailing.status = 'pending'
#         mailing.save()
#
#         clients = mailing.client.all()
#         message = mailing.message
#         response = None
#         try:
#             response = send_mailing(clients, message)
#             mailing.status = 'completed'
#         except smtplib.SMTPException as e:
#             response = False
#             log_message = str(e)
#             mailing.status = 'failed'
#
#         mailing.save()
#
#         if mailing.periodicity:
#             update_mailing_date(mailing, now)
#
#         log = Log.objects.create(
#             time=now,
#             status=response,
#             server_response=log_message if not response else '',
#             mailing=mailing,
#             user=user
#         )
#         log.save()
#
#
# def update_mailing_date(mailing, now):
#     """Функция обновляет дату следующей рассылки в зависимости от периодичности."""
#     if mailing.periodicity == 'day':
#         mailing.date += timedelta(days=1)
#     elif mailing.periodicity == 'week':
#         mailing.date += timedelta(weeks=1)
#     elif mailing.periodicity == 'month':
#         days_in_month = monthrange(now.year, now.month)[1]
#         mailing.date += timedelta(days=days_in_month)
#     mailing.save()
