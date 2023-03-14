"""
smth
"""
from django.db import models

# Create your models here.
class List(models.Model):
    """
    Clase que contendra los items de casa usuario
    """
    # user = models.ForeignKey()
    pass

class Item(models.Model):
    """
    item model
    """
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE, null=True)
