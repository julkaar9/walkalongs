from django.contrib import admin
from .custom_models import Occupation, Person

# Register your models here.

admin.site.register(Occupation)
admin.site.register(Person)
