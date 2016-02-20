from __future__ import unicode_literals

from django.db import models


# Create your models here.
class SoftwareConfiguration(models.Model):
    OS_MAC = 0
    OS_LINUX = 1
    OS_CHOICES = (
        (OS_MAC, "OS_MAC"),
        (OS_LINUX, "OS_LINUX"),
    )

    ARCH_32 = 32
    ARCH_64 = 32
    ARCH_CHOICES = (
        (ARCH_32, "32-bit"),
        (ARCH_64, "64-bit"),
    )

    name = models.CharField(max_length=500, blank=True, null=True)
    version = models.CharField(max_length=100, blank=True, null=True)
    os = models.IntegerField(choices=OS_CHOICES, default=OS_MAC)
    arch = models.IntegerField(choices=ARCH_CHOICES, default=ARCH_64)
    value = models.CharField(max_length=500, blank=True, null=True)
    tag = models.CharField(max_length=500, blank=True, null=True)
