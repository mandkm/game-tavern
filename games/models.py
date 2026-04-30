from django.db import models
from django.conf import settings

class GameCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Game(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        GameCategory, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='games'
    )

    def __str__(self):
        return self.name

class GameLibrary(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='library'
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='owners'
    )

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user} owns {self.game}"
    