from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class GenericFile(models.Model):
    file = models.FileField()
    title = models.CharField(max_length=140)
    csv = models.BooleanField(default=False)

    
