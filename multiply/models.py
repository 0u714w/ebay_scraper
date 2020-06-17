from django.db import models
from django.utils import timezone


class GenericFile(models.Model):
    title = models.CharField(max_length=140)
    csv_active = models.BooleanField(default=False)
    csv_sold = models.BooleanField(default=False)
    created_date = models.DateTimeField('date created', default=timezone.now)

