from django.urls import path
from django.views.decorators.cache import cache_page

from mailings.apps import MailingsConfig
from mailings.views import HomeTemplateView, ClientCreateView, MessageCreateView, MailingCreateView, ClientListView, \
    MessageListView, MailingListView, ClientUpdateView, ClientDeleteView, MessageUpdateView, MessageDeleteView, \
    MailingUpdateView, MailingDeleteView, status_mailing, LogListView, LogDetailView, LogDeleteView

app_name = MailingsConfig.name


urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home_page'),

    path('add', ClientCreateView.as_view(), name='add_client'),
    path('client_list', ClientListView.as_view(), name='client_list'),
    path('edit_client/<int:pk>', ClientUpdateView.as_view(), name='edit_client'),
    path('delete_client/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),

    path('create_message', MessageCreateView.as_view(), name='create_message'),
    path('message_list', MessageListView.as_view(), name='message_list'),
    path('edit_message/<int:pk>', MessageUpdateView.as_view(), name='edit_message'),
    path('delete_message/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),

    path('create_mailing', MailingCreateView.as_view(), name='create_mailing'),
    path('mailing_list', MailingListView.as_view(), name='mailing_list'),
    path('edit_mailing/<int:pk>', MailingUpdateView.as_view(), name='edit_mailing'),
    path('delete_mailing/<int:pk>', MailingDeleteView.as_view(), name='delete_mailing'),
    path('status_mailing/<int:pk>', status_mailing, name='status_mailing'),

    path('log_list', LogListView.as_view(), name='log_list'),
    path('log_detail/<int:pk>', cache_page(60)(LogDetailView.as_view()), name='log_detail'),
    path('delete_log/<int:pk>', LogDeleteView.as_view(), name='delete_log'),
]
