from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class job(models.Model):
    recruter = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    required_skills = models.TextField()
    salary = models.CharField(max_length=50)
    crested_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


class jobApplication(models.Model):
    STATUS_CHOICE = [
        ('Pending', 'Pending'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
        ('Selected', 'Selected'),
]

    candidate = models.ForeignKey(
        'account.Candidate',
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        job,
        on_delete=models.CASCADE
    )

    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICE,
        default='Pending'
    )

    def __str__(self):
        return f"{self.candidate.user.username} - {self.job.title}"

    


