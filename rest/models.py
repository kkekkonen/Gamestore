from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils import timezone

# Create your models here.

class ApiKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    token = models.CharField(max_length=32, editable=False, default=get_random_string(length=32), blank=False)
    created = models.DateTimeField(editable=False, default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    