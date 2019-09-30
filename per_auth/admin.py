from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from .models import Person


@admin.register(Person)
class PersonAdmin(ModelAdmin):
    # add_form = UserCreationForm
    # form = UserChangeForm
    model = Person
    list_display = ['email', 'formal_name']
    exclude = ()
