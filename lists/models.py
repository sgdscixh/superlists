"""models for list app"""
from django.db import models


class List(models.Model):
    """list model"""


# Create your models here.
class Item(models.Model):
    """item model"""

    text = models.TextField(default="")
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
