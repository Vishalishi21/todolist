
from django.contrib import admin
from home.models import UserProfile , Task


# Register your models here.
admin.site.register(Task)
admin.site.register(UserProfile)
