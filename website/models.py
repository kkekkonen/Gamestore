from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

class RightsSupport(models.Model):

    class Meta:

        managed = False  # No database table creation or deletion operations \
                         # will be performed for this model.

        permissions = (
            ('developer_rights', 'developers can add games'),
            ('admin_rights', 'admins cannot do anything yet'),
            ('no_rights', ' '),
        )

class Game(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField(blank=False)
    description = models.CharField(max_length=255)
    price = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Purchase(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(editable=False, default=timezone.now)

class Score(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()

class GameState(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gamestate = models.TextField()
