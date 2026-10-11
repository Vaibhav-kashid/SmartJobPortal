from django.contrib import admin
from .models import job, jobApplication

# Register your models here.

admin.site.register(job)
admin.site.register(jobApplication)