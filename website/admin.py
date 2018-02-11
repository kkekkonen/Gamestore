from django.contrib import admin
from website.models import Game, Purchase, Score, GameState, Category

admin.site.register(Game)
admin.site.register(Purchase)
admin.site.register(Score)
admin.site.register(GameState)
admin.site.register(Category)