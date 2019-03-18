from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Person


@admin.register(Person)
class PersonAdmin(UserAdmin):
    # add_form = UserCreationForm
    # form = UserChangeForm
    model = Person
    list_display = ['email', 'formal_name']
