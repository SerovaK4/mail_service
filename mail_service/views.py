from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from mail_service.models import Mailing

from  client.models import Client

# MailingDetailView, MailingCreateView, MailingUpdateView, MailingDeleteView, main


@login_required
def contacts(request):
    if request.mthod == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name}, {email}: {message}')
    context = {
        'title': "Контакты"
    }
    return render(request, 'mail_service/contacts.html', context)


class MailServiceListView(ListView):
    model = Mailing
    template_name = 'mail_service/mailing_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class MailServiceDetailView(DetailView):
    model = Mailing
    success_url = reverse_lazy('mail_service:index')


def main(request):
    clients = len(Client.objects.all().distinct("email"))
    article = Article.objects.all()

