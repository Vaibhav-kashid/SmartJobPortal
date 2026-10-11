from django.urls import path
from .views import (
    create_job,
    job_list,
    job_details,
    apply_job,
    my_applications,
    recruiter_jobs,
    job_applicants,
    update_application_status,
    candidate_dashboard,
    recruiter_dashboard
)

urlpatterns = [
    path('create/', create_job, name='create_job'),
    path('my-applications/', my_applications, name='my_applications'),
    path('my-jobs/', recruiter_jobs, name='recruiter_jobs'),

    path('candidate-dashboard/', candidate_dashboard, name='candidate_dashboard'),
    path('recruiter-dashboard/', recruiter_dashboard, name='recruiter_dashboard'),

    path('<int:id>/apply/', apply_job, name='apply_job'),
    path('<int:id>/applicants/', job_applicants, name='job_applicants'),
    path('application/<int:application_id>/status/', update_application_status, name='update_application_status'),
    path('<int:id>/', job_details, name='job_details'),
    path('', job_list, name='job_list'),
]