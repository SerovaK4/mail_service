import smtplib
from datetime import datetime

import pytz as pytz
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Article
from config import settings
from mail_service.forms import MailingForms
from mail_service.models import Mailing, Log

from client.models import Client


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name}, {email}: {message}')
    context = {
        'title': "Контакты"
    }
    return render(request, 'mail_service/contact.html', context)


class MailServiceListView(ListView):
    model = Mailing
    template_name = 'mail_service/mail_service_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user.id)


class MailServiceDetailView(DetailView):
    model = Mailing
    template_name = 'mail_service/mail_service_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if settings.CACHE_ENABLED:
            key = f'log_list_{self.object.pk}'
            log_list = cache.get(key)
            if log_list is None:
                log_list = self.object.log_set.all()
                cache.set(key, log_list)
        else:
            log_list = self.object.log_set.all()
        context_data['logs'] = log_list

        return context_data


def main(request):
    clients = len(Client.objects.all().distinct("email"))
    article = Article.objects.all()
    mailing = len(Mailing.objects.all())
    mailing_active = len(Mailing.objects.filter(status=2))
    context = {
        'title': "Главная",
        'article': article[:3],
        'mailing': mailing,
        'mailing_active': mailing_active,
        'clients': clients
    }

    return render(request, 'mail_service/main.html', context)


class MailServiceCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForms
    success_url = reverse_lazy('mail_service:list')

    def form_valid(self, form):
        if form.is_valid():
            new_mail = form.save()
            new_mail.slug = slugify(new_mail.title)
            new_mail.save()

        return super().form_valid(form)


    def form_valid(self, form):
        tz = pytz.timezone('Europe/Moscow')
        clients = [client.email for client in Client.objects.filter(user=self.request.user)]
        new_mailing = form.save()
        if new_mailing.mailing_time <= datetime.now(tz):
            mail_subject = new_mailing.massage.email_body if new_mailing.massage is not None else 'Рассылка'
            message = new_mailing.massage.email_theme if new_mailing.massage is not None else 'Вам назначена рассылка'
            try:
                send_mail(mail_subject, message, settings.EMAIL_HOST_USER, clients)
                log = Log.objects.create(attempt_date=datetime.now(tz), status='Успешно', server_response='200',
                                         mailing=new_mailing)
                log.save()
            except smtplib.SMTPDataError as err:
                log = Log.objects.create(attempt_date=datetime.now(tz), status='Ошибка', server_response=err,
                                         mailing=new_mailing)
                log.save()
            except smtplib.SMTPException as err:
                log = Log.objects.create(attempt_date=datetime.now(tz), status='Ошибка', server_response=err,
                                         mailing=new_mailing)
                log.save()
            except Exception as err:
                log = Log.objects.create(date_attempt=datetime.now(tz), status='Ошибка', server_response=err,
                                         mailing=new_mailing)
                log.save()
            new_mailing.status = 3

            new_mailing.save()

        return super().form_valid(form)


class MailServiceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForms
    permission_required = 'mail_service.change_mailing'
    success_url = reverse_lazy('mail_service:list')


class MailServiceDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mail_service:list')
