import smtplib
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from mailings.models import Mailing, Log
from mailings.services import send_mailing


class Command(BaseCommand):
    help = 'Handles sending scheduled mailings'

    def handle(self, *args, **options):
        now = datetime.now()
        # Предполагается, что поле `time` это datetime
        # Предполагается, что рассылки только на этот день запускаются в указанное `time`
        today_midnight = datetime(now.year, now.month, now.day)
        tomorrow_midnight = today_midnight + timedelta(days=1)
        mailing_list = Mailing.objects.filter(date__gte=today_midnight,
                                              date__lt=tomorrow_midnight,
                                              time__lte=now,
                                              status='created')
        if not mailing_list.exists():
            print("No mailings to process.")
            return

        for mailing in mailing_list:
            mailing.status = 'started'
            mailing.save()

            clients = mailing.client.all()
            try:
                response = send_mailing(clients, mailing.message)
                status = bool(response)

                # Определение новой даты выпуска
                if mailing.periodicity == 'day':
                    new_date = now + timedelta(days=1)
                elif mailing.periodicity == 'week':
                    new_date = now + timedelta(weeks=1)
                elif mailing.periodicity == 'month':
                    new_date = now.replace(day=28) + timedelta(days=4)
                    new_date -= timedelta(days=new_date.day - 1)

                # Управление транзакциями для координации сохранения объектов
                with transaction.atomic():
                    Log.objects.create(time=now, status=status, server_response=str(response), mailing=mailing, user=mailing.user)
                    mailing.date = new_date
                    mailing.status = 'created'
                    mailing.save()

            except smtplib.SMTPException as e:
                # Логирование исключения
                Log.objects.create(time=now, status=False, server_response=str(e), mailing=mailing, user=mailing.user)
                mailing.status = 'created'
                mailing.save()
                print(f"Failed to send mailing: {e}")

        print("All mailings processed.")
