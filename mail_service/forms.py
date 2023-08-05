from django import forms

from mail_service.models import Mailing


class MailingForms(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'