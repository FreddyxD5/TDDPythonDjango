"""
smth
"""
from django.db import models

# Create your models here.
class Item(models.Model):
    """
    item model
    """
    text = models.TextField(default='')
