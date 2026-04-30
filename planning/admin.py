from django.contrib import admin
from .models import CalendarEntry, Participation, Notification

admin.site.register(CalendarEntry)
admin.site.register(Participation)
admin.site.register(Notification)
