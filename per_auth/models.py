from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from Unipin.settings import PROFILE_IMAGES_PATH


class PersonManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self._create_user(email, password, **extra_fields)


class Person(AbstractUser):
    email = models.EmailField(u'ایمیل', unique=True)
    username = models.CharField(_('username'), max_length=150, blank=True)

    # is_active = models.BooleanField(_('active'), default=True, help_text=_(
    #     'Designates whether this user should be treated as active. '
    #     'Unselect this instead of deleting accounts.'
    # ),
    #                                 )
    # date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = PersonManager()

    formal_name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, default='')
    url_name = models.CharField(max_length=30, null=True, blank=True)
    profile_image = models.ImageField(upload_to=PROFILE_IMAGES_PATH, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email + ' <' + self.formal_name + '>'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

        # @property
        # def is_staff(self):
        #     "Is the user a member of staff?"
        #     # Simplest possible answer: All admins are staff
        #     return self.is_admin

        # real_type = models.ForeignKey(ContentType)

        # is_formal = models.BooleanField(default=False)

        # national_id = models.CharField(max_length=100, null=True, blank=True)
        # sharif_mail_address = models.EmailField(null=True, blank=True)
        # interested_tags = models.ManyToManyField(Tag, blank=True)
        # follows = models.ManyToManyField(SuperConductor, through='Follow', related_name='followers')


# ------------------------------------------------------------------------


def get_user_display(user):
    return user.formal_name
