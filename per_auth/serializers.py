from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import PasswordResetSerializer
from rest_framework import serializers

from Unipin import settings
from . import models


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = ('email', 'formal_name', 'profile_image', 'url_name', 'description',)


class CustomizedRegisterSerializer(RegisterSerializer):
    formal_name = serializers.CharField(max_length=50)

    # phone_number = serializers.RegexField(r'^09[0-9]+{9}$')
    # birth_date = serializers.DateField()

    # def save(self, request):
    #     user = super(CustomizedRegisterSerializer, self).save(request)
    #     # user.first_name = self.cleaned_data['first_name']
    #     # user.last_name = self.cleaned_data['last_name']
    #     # phone_number = self.cleaned_data['phone_number']
    #     # birth_date = self.cleaned_data['birth_date']
    #     profile = Person(user=user, phone_number=phone_number, birth_date=birth_date)
    #     profile.save()
    #     return user


class CustomizedPasswordResetSerializer(PasswordResetSerializer):
    class Meta:
        abstract = True

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'FROM_EMAIL'),
            'request': request,
            'subject_template_name': 'Auth/forgot_password_subject.txt',
            'email_template_name': 'Auth/forgot_password_email.html',
            'extra_email_context': None,
        }
        self.reset_form.save(**opts)
