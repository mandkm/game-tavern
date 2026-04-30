from django.db import models
from django.conf import settings
from games.models import GameCategory
from locations.models import Location
from food.models import Food

class CalendarEntry(models.Model):
    STATUS_CHOICES = [
        ('open', 'Offen'),
        ('evaluated', 'Bewertet'),
        ('confirmed', 'Bestätigt'),
        ('cancelled', 'Abgesagt'),
    ]
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='entries')
    game_category = models.ForeignKey(
        GameCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='entries')
    food = models.ForeignKey(
        Food, on_delete=models.SET_NULL, null=True, blank=True, related_name='entries')
    
    def __str__(self):
        return f"Entry {self.date} ({self.status})"
    
class Participation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participations')
    calendar_entry = models.ForeignKey(
        CalendarEntry, on_delete=models.CASCADE, related_name='participations')
    available = models.BooleanField(default=True)
    alternative_date = models.DateTimeField(null=True, blank=True)
    can_host = models.BooleanField(default=False)
    food = models.ForeignKey(
        Food, on_delete=models.SET_NULL, null=True, blank=True, related_name='participations')
    game_category = models.ManyToManyField(
        GameCategory, blank=False, related_name='participations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'calendar_entry')

    def __str__(self):
        return f"{self.user} - {self.calendar_entry}"
    
class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    calendar_entry = models.ForeignKey(
        CalendarEntry, on_delete=models.CASCADE, related_name="notifications"
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Notification for {self.user} - read: {self.read_at is not None}"    
