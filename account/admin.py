from django.contrib import admin
from .models import Candidate, recruter, Profile
# Register your models here.

admin.site.register(Candidate)
admin.site.register(recruter)
admin.site.register(Profile)