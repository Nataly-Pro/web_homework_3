from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, UpdateView
from users.forms import RegisterForm, ResetForm
from users.models import User
from django.utils.crypto import get_random_string


class UserLoginView(LoginView):
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        self.object = form.save()
        self.object.verify_code = get_random_string(12)
        self.object.save()
        url = f'http://127.0.0.1:8000/users/email/verify/{self.object.verify_code}'
        send_mail(
                subject='Регистрация',
                message=f'Для успешной регистрации перейдите по ссылке: {url}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.object.email],
                fail_silently=False,
            )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:verify_message')


def verification(request, verify_code):
    try:
        user = User.objects.filter(verify_code=verify_code).first()
        user.is_active = True
        user.save()
        return redirect('users:success_verify')
    except (AttributeError, ValidationError):
        return redirect('users:invalid_verify')


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        new_password = get_random_string(12)
        send_mail(
            subject='Восстановление пароля',
            message=f'Для входа используйте новый пароль: {new_password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        user.set_password(new_password)
        user.save()
        return redirect('users:login')
    else:
        form = ResetForm
        context = {
            'form': form
        }
        return render(request, 'users/reset_password.html', context)


