from __future__ import unicode_literals

from django.db import models

# Create your models here.
class SavedFoodVision(models.Model):
    type = models.CharField(max_length=150)
