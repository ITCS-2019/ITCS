from django.db import models
from django.contrib import admin

import os
from django.conf import settings

def only_filename(instance, filename):
    fullname = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(fullname):
        os.remove(fullname)
    return filename

class RegulationDoc(models.Model):
	date_activation = models.DateTimeField(blank=True)
	number = models.CharField(blank=True, max_length=100)
	title = models.CharField(blank=True, max_length=150)
	status = models.CharField(blank=True, max_length=100)
	text = models.TextField(blank=True)
	pdf_file = models.FileField(blank=True, upload_to=only_filename)
	user = models.CharField(blank=True, max_length=100)
	prev_version = models.CharField(blank=True, max_length=100)
	organisation = models.CharField(blank=True, max_length=150)
	regulation_organization_link = models.CharField(blank=True, max_length=150)

class RegulationDocAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'date_activation', 'user', 'status',)
    search_fields = ('number',)


admin.site.register(RegulationDoc, RegulationDocAdmin)