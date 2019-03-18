from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from rest_auth.registration.views import RegisterView
from rest_auth.views import PasswordResetView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from per_auth.models import Person
from per_auth.serializers import CustomizedPasswordResetSerializer, CustomizedRegisterSerializer, PersonSerializer
from per_auth.tokens import account_activation_token


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'url_name'


class Signup(CreateView):
    model = Person
    # form_class = SignupForm
    # fields = ('first_name', 'last_name', 'username', 'email', 'birth_date', 'phone_number', 'address', 'password')
    template_name = 'Auth/signup.html'

    def post(self, request, *args, **kwargs):
        return super(Signup, self).post(self, request, *args, **kwargs)

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.is_active = False
        profile.save()
        current_site = get_current_site(self.request)
        subject = 'Activate Your MySite Account'
        message = render_to_string('account_activation_email.html', {
            'user': profile,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(profile.pk)).decode(),
            'token': account_activation_token.make_token(profile),
        })
        profile.email_user(subject, message)
        return super(Signup, self).form_valid(form)

        # def get_success_url(self):
        #     return '/per_auth/welcome/'


class SignedUpPage(TemplateView):
    template_name = 'Auth/signed-up.html'


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('Core:home')
    else:
        return render(request, 'Auth/account_activation_invalid.html')


class CustomizedRegisterView(RegisterView):
    serializer_class = CustomizedRegisterSerializer


class Signup(CreateView):
    model = Person
    # form_class = SignupForm
    # fields = ('first_name', 'last_name', 'username', 'email', 'birth_date', 'phone_number', 'address', 'password')
    template_name = 'Auth/signup.html'

    def post(self, request, *args, **kwargs):
        return super(Signup, self).post(self, request, *args, **kwargs)

    def form_valid(self, form):
        profile = form.save(commit=False)
        # profile.is_active = False
        profile.save()
        current_site = get_current_site(self.request)
        subject = 'Activate Your Pyro Account'
        message = render_to_string('Auth/account_activation_email.html', {
            'user': profile,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(profile.pk)).decode(),
            'token': account_activation_token.make_token(profile),
        })
        profile.email_user(subject, message)
        return super(Signup, self).form_valid(form)

    def get_success_url(self):
        return '/per_auth/welcome/'


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('Core:home')
    else:
        return render(request, 'Auth/account_activation_invalid.html')


class CustomizedPasswordResetView(PasswordResetView):
    serializer_class = CustomizedPasswordResetSerializer
