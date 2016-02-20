from django.contrib import admin


# Register your models here.
from backend.models import SoftwareConfiguration


class SoftwareConfigurationAdmin(admin.ModelAdmin):
    list_display = ["id", "arch", "os", "tag", "value", "name", "version"]
    list_filter = ["arch", "os", "tag", "value", "name", "version"]

admin.site.register(SoftwareConfiguration, SoftwareConfigurationAdmin)
