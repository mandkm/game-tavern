from django.contrib import admin
from .models import GameCategory, Game, GameLibrary

admin.site.register(GameCategory)
admin.site.register(Game)
admin.site.register(GameLibrary)