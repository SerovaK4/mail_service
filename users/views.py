from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import RegisterForm, UserProfileForm
from users.models import User

class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        #Генерируем уникальный токен для верификации
        user = form.save(commit=False)
        # Деактивируем пользователя, пока он не подтвердит почту
        user.is_active = False
        #Устанавливаем ненужный пароль
        #user.set_unusable_password()
        user.save()

        #Отправляем письмо с токеном для верификации
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(self.request)
        mail_subject = 'Активация аккаунта'
        message = render_to_string(
            'users/verification_email.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            }
        )
        print(user.email)
        send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [user.email])
        return redirect('users:login')


class EmailVerificationView(TemplateView):
    template_name = 'users/email_verify_yes.html'

    def get(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                #user.set_password()
                user.save()
                return self.render_to_response({})
            else:
                return redirect('users:verify_no')
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return redirect('users:verify_no')

class ActivationSuccess(TemplateView):
    template_name = 'users/email_verify_yes.html'


class ActivationFailed(TemplateView):
    template_name = 'users/email_verify_no.html'


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
