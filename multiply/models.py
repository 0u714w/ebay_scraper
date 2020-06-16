from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class GenericFile(models.Model):
    title = models.CharField(max_length=140)
    csv_active = models.BooleanField(default=False)
    csv_sold = models.BooleanField(default=False)

