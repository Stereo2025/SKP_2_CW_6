import random

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView

from blogs.models import Blog
from mailings.forms import ClientForm, MessageForm, MailingForm
from mailings.models import Client, Message, Mailing, Log


class HomeTemplateView(TemplateView):
    template_name = 'mailing/index.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        user = self.request.user
        if user.is_authenticated:
            context_data['clients_count'] = Client.objects.filter(user=user).count()
            context_data['mailing_count'] = Mailing.objects.filter(user=user).count()
            context_data['active_mailing'] = Mailing.objects.filter(user=user, status='created').count()
        else:
            context_data['clients_count'] = 0
            context_data['mailing_count'] = 0
            context_data['active_mailing'] = 0

        blogs = list(Blog.objects.all()[:10])
        context_data['random_blog_list'] = random.sample(blogs, min(len(blogs), 3)) if blogs else []

        return context_data


class ClientListView(LoginRequiredMixin, ListView):
    """Контроллер страницы клиентов"""
    model = Client
    template_name = 'mailing/client_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:home_page')
    template_name = 'mailing/client_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClientAccessMixin(UserPassesTestMixin):
    def test_func(self):
        client = self.get_object()
        return client.user == self.request.user


class ClientUpdateView(LoginRequiredMixin, ClientAccessMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')
    template_name = 'mailing/client_form.html'


class ClientDeleteView(LoginRequiredMixin, ClientAccessMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:client_list')
    template_name = 'mailing/client_confirm_delete.html'


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailing/message_list.html'

    def get_queryset(self):
        # return self.model.objects.filter(user=self.request.user).only('title', 'timestamp')
        return super().get_queryset().filter(user=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')
    template_name = 'mailing/message_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MessageUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().user


class MessageUpdateView(LoginRequiredMixin, MessageUserPassesTestMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')
    template_name = 'mailing/message_form.html'


class MessageDeleteView(LoginRequiredMixin, MessageUserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailings:home_page')
    template_name = 'mailing/message_confirm_delete.html'


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:home_page')
    template_name = 'mailing/mailing_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MailingUserPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().user


class MailingUpdateView(LoginRequiredMixin, MailingUserPermissionMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailings:mailing_list')
    template_name = 'mailing/mailing_form.html'


class MailingDeleteView(LoginRequiredMixin, MailingUserPermissionMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailings:mailing_list')
    template_name = 'mailing/mailing_confirm_delete.html'


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm('mailing.view_mailing'):
            return queryset
        return queryset.filter(user=self.request.user)


def status_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if request.user == mailing.user or request.user.has_perm('mailing.set_status'):
        new_status = 'completed' if mailing.status == 'created' else 'created'
        mailing.status = new_status
        mailing.save(update_fields=['status'])
    else:
        raise Http404("You don't have permission to change the status.")
    return redirect('mailings:mailing_list')


class LogListView(LoginRequiredMixin, ListView):
    """Контроллер страницы логов"""
    model = Log
    template_name = 'mailing/log_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class UserLogAccessMixin(UserPassesTestMixin):
    def test_func(self):
        log = self.get_object()
        return self.request.user == log.user


class LogDetailView(LoginRequiredMixin, UserLogAccessMixin, DetailView):
    model = Log


class LogDeleteView(LoginRequiredMixin, UserLogAccessMixin, DeleteView):
    model = Log
    success_url = reverse_lazy('mailing:log_list')
