from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    skills = models.TextField()
    education = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resume/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class recruter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)


    def __str__(self):
        return self.company_name


class Profile(models.Model):

    ROLE_CHOICE = [
        ('candidate', 'Candidate'),
        ('recruiter', 'Recruiter'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICE)

    def __str__(self):
        return self.user.username