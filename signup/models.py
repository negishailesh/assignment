# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User


class CityDetails(models.Model):
    user = models.ForeignKey(User)
    location = models.CharField(max_length = 200)
    state = models.CharField(max_length = 100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6,blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True) 


