from __future__ import unicode_literals

from django.db import models


# Create your models here.
class SoftwareConfiguration(models.Model):
    OS_DARWIN = 0
    OS_LINUX = 1
    OS_CHOICES = (
        (OS_DARWIN, "OS_DARWIN"),
        (OS_LINUX, "OS_LINUX"),
    )

    ARCH_32 = 32
    ARCH_64 = 64
    ARCH_BOTH = 16
    ARCH_CHOICES = (
        (ARCH_32, "32-bit"),
        (ARCH_64, "64-bit"),
        (ARCH_BOTH, "both"),
    )

    name = models.CharField(max_length=500, blank=True, null=True)
    version = models.CharField(max_length=100, blank=True, null=True)
    os = models.IntegerField(choices=OS_CHOICES, default=OS_DARWIN)
    arch = models.IntegerField(choices=ARCH_CHOICES, default=ARCH_64)
    command = models.CharField(max_length=500, blank=True, null=True)
    url = models.URLField(max_length=500, blank=True, null=True)
    tag = models.CharField(max_length=500, blank=True, null=True)
