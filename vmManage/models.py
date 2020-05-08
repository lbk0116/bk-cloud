# -*- coding: utf-8 -*-
from django.db import models

class vm(models.Model):
    vm = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    power_state = models.CharField(max_length=50)
    cpu_count = models.IntegerField()
    memory_size_mib = models.IntegerField()

