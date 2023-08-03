from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from mail_service.apps import MailServiceConfig
from mail_service.views import contacts, MailServiceListView, MailServiceDetailView, MailingCreateView, \
    MailingUpdateView, MailingDeleteView, main


app_name = MailServiceConfig.name

urlpatterns = [
    path('', MailServiceListView.as_view(), name='list'),
    path('contact/', contacts, name='contact'),
    path('main/', main, name='main'),
    path('view/<int:pk>', MailServiceDetailView.as_view(), name='view_mailing'),
    path('create/', MailingCreateView.as_view(), name='create'),
    path('edit/<int:pk>', MailingUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>', MailingDeleteView.as_view(), name='delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)