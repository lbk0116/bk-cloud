# -*- coding: utf-8 -*-
from django.db import models

class order(models.Model):
    id = models.AutoField(primary_key=True)
    itsm_id = models.CharField(max_length=50)

class Vm(models.Model):
    vm = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    power_state = models.CharField(max_length=50)
    cpu_count = models.IntegerField()
    memory_size_mib = models.IntegerField()

class Device(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    mgt_ip = models.CharField(max_length=50)

class Pool(models.Model):
    name = models.CharField(max_length=50, unique=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)


class Vip(models.Model):
    vip = models.CharField(max_length=50)
    vport = models.IntegerField()
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, null=True, blank=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # update_time = models.DateTimeField(auto_now=True, null=True, blank=True)


class RequirementVip(models.Model):
    vip = models.CharField(max_length=50)
    vport = models.IntegerField()
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, null=True, blank=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    create_by_order_id = models.ForeignKey(order, on_delete=models.CASCADE, null=True, related_name='create_order')
    update_by_order_id = models.ForeignKey(order, on_delete=models.CASCADE, null=True, related_name='update_order')
    delete_by_order_id = models.ForeignKey(order, on_delete=models.CASCADE, null=True, related_name='delete_order')

    class Meta:
        unique_together = ('vip', 'vport')

class Members(models.Model):
    name = models.CharField(max_length=50, unique=True)
    ip = models.CharField(max_length=50)
    port = models.IntegerField()
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

