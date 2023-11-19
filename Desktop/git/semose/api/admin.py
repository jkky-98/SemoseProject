from django.contrib import admin
from .models import Place, LogEntry


# Register your models here.
admin.site.register(Place)
admin.site.register(LogEntry)