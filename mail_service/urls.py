from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from mail_service.apps import MailServiceConfig
from mail_service.views import contacts, MailServiceListView, MailServiceDetailView, MailServiceCreateView, \
    MailServiceUpdateView, MailServiceDeleteView, main


app_name = MailServiceConfig.name

urlpatterns = [
    path('', MailServiceListView.as_view(), name='list'),
    path('contact/', contacts, name='contact'),
    path('list/', MailServiceListView.as_view(), name='list'),
    path('main/', main, name='main'),
    path('view/<int:pk>', MailServiceDetailView.as_view(), name='view_mailing'),
    path('create/', MailServiceCreateView.as_view(), name='create'),
    path('edit/<int:pk>', MailServiceUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>', MailServiceDeleteView.as_view(), name='delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

