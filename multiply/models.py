from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class GenericFile(models.Model):
    title = models.CharField(max_length=140)
    csv = models.BooleanField(default=False)
    file = models.FileField(upload_to="files/")

