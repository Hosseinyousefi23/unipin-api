from allauth.account.views import confirm_email
from django.conf.urls import url
from rest_auth.registration.views import VerifyEmailView
from rest_auth.views import LoginView, LogoutView, PasswordResetConfirmView, PasswordChangeView
from rest_framework.routers import DefaultRouter

from per_auth import views
from per_auth.views import CustomizedPasswordResetView, CustomizedRegisterView, PersonViewSet

# app_name = 'per_auth'

router = DefaultRouter()
router.register(r'person', PersonViewSet, base_name='person')
urlpatterns = router.urls + [
    url(r'^login/?$', LoginView.as_view(), name='login'),
    url(r'^register/?$', CustomizedRegisterView.as_view(), name='register'),
    url(r'^logout/?$', LogoutView.as_view(), name='logout'),
    url(r'^verify-email/$', VerifyEmailView.as_view(), name='rest_verify_email'),
    url(r'^account-confirm-email/(?P<key>[-:\w]+)/$', confirm_email,
        name='account_confirm_email'),
    url(r'^activate/?$', views.activate, name='activate'),
    url(r'^password/forgot/?$', CustomizedPasswordResetView.as_view(), name='forgot_password'),
    url(r'^password/reset/?$', PasswordResetConfirmView.as_view(), name='reset_password'),
    url(r'^password/change/?$', PasswordChangeView.as_view(), name='change_password'),
    # url(r'^activate/?(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.activate, name='activate'),
]
