from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import jobForm, ApplicationForm
from .models import job, jobApplication

from account.models import Profile, Candidate


# Create Job
@login_required
def create_job(request):

    profile = Profile.objects.filter(
        user=request.user
    ).first()

    if profile is None or profile.role != 'recruiter':
        return redirect('home')

    if request.method == 'POST':

        form = jobForm(request.POST)

        if form.is_valid():

            job_obj = form.save(commit=False)

            job_obj.recruter = request.user

            job_obj.save()

            return redirect('home')

    else:
        form = jobForm()

    return render(
        request,
        'jobs/create_job.html',
        {
            'form': form
        }
    )


# Job List
# Job List - Search + Location Filter
def job_list(request):

    search = request.GET.get('search', '').strip()
    location = request.GET.get('location', '').strip()

    jobs = job.objects.all().order_by('-crested_at')

    # Search by title or company
    if search:
        jobs = jobs.filter(
            title__icontains=search
        ) | jobs.filter(
            company_name__icontains=search
        )

    # Filter by location
    if location:
        jobs = jobs.filter(
            location__icontains=location
        )

    return render(
        request,
        'jobs/job_list.html',
        {
            'jobs': jobs,
            'search': search,
            'location': location
        }
    )


# Job Details
def job_details(request, id):

    job_obj = get_object_or_404(
        job,
        id=id
    )

    already_applied = False
    user_role = None

    if request.user.is_authenticated:

        profile = Profile.objects.filter(
            user=request.user
        ).first()

        if profile:

            user_role = profile.role

        if user_role == 'candidate':

            candidate = Candidate.objects.filter(
                user=request.user
            ).first()

            if candidate:

                already_applied = jobApplication.objects.filter(
                    candidate=candidate,
                    job=job_obj
                ).exists()

    return render(
        request,
        'jobs/job_details.html',
        {
            'job': job_obj,
            'already_applied': already_applied,
            'user_role': user_role
        }
    )


# Apply Job
@login_required
def apply_job(request, id):

    profile = Profile.objects.filter(
        user=request.user
    ).first()

    if profile is None or profile.role != 'candidate':

        return redirect(
            'job_details',
            id=id
        )

    job_obj = get_object_or_404(
        job,
        id=id
    )

    candidate = Candidate.objects.filter(
        user=request.user
    ).first()

    if candidate is None:

        candidate = Candidate.objects.create(
            user=request.user,
            phone='',
            skills='',
            education=''
        )

    already_applied = jobApplication.objects.filter(
        candidate=candidate,
        job=job_obj
    ).exists()

    if already_applied:

        return redirect(
            'job_details',
            id=job_obj.id
        )

    if request.method == 'POST':

        form = ApplicationForm(
            request.POST,
            request.FILES,
            instance=candidate
        )

        if form.is_valid():

            form.save()

            jobApplication.objects.create(
                candidate=candidate,
                job=job_obj
            )

            return redirect(
                'my_applications'
            )

    else:

        form = ApplicationForm(
            instance=candidate
        )

    return render(
        request,
        'jobs/apply_job.html',
        {
            'form': form,
            'job': job_obj
        }
    )


# Candidate My Applications
@login_required
def my_applications(request):

    profile = Profile.objects.filter(
        user=request.user
    ).first()

    if profile is None or profile.role != 'candidate':

        return redirect('home')

    candidate = Candidate.objects.filter(
        user=request.user
    ).first()

    if candidate is None:

        applications = []

    else:

        applications = jobApplication.objects.filter(
            candidate=candidate
        ).select_related(
            'job'
        ).order_by(
            '-applied_at'
        )

    return render(
        request,
        'jobs/my_applications.html',
        {
            'applications': applications
        }
    )


# Recruiter My Posted Jobs
@login_required
def recruiter_jobs(request):

    profile = Profile.objects.filter(
        user=request.user
    ).first()

    if profile is None or profile.role != 'recruiter':

        return redirect('home')

    jobs = job.objects.filter(
        recruter=request.user
    ).order_by(
        '-crested_at'
    )

    return render(
        request,
        'jobs/recruiter_jobs.html',
        {
            'jobs': jobs
        }
    )


# Job Applicants
@login_required
def job_applicants(request, id):

    profile = Profile.objects.filter(
        user=request.user
    ).first()

    if profile is None or profile.role != 'recruiter':

        return redirect('home')

    job_obj = get_object_or_404(
        job,
        id=id
    )

    if job_obj.recruter != request.user:

        return redirect('home')

    applications = jobApplication.objects.filter(
        job=job_obj
    ).select_related(
        'candidate',
        'candidate__user'
    )

    return render(
        request,
        'jobs/job_applicants.html',
        {
            'job': job_obj,
            'applications': applications
        }
    )


# Update Application Status
@login_required
def update_application_status(request, application_id):

    profile = Profile.objects.filter(
        user=request.user
    ).first()

    if profile is None or profile.role != 'recruiter':

        return redirect('home')

    application = get_object_or_404(
        jobApplication,
        id=application_id
    )

    if application.job.recruter != request.user:

        return redirect('home')

    if request.method == 'POST':

        status = request.POST.get('status')

        if status in [
            'Pending',
            'Shortlisted',
            'Rejected',
            'Selected'
        ]:

            application.status = status

            application.save()

    return redirect(
        'job_applicants',
        id=application.job.id
    )


# Candidate Dashboard
@login_required
def candidate_dashboard(request):
    profile = Profile.objects.filter(user=request.user).first()

    if profile is None or profile.role != 'candidate':
        return redirect('home')

    candidate = Candidate.objects.filter(user=request.user).first()

    total_applications = 0
    pending = 0
    shortlisted = 0
    selected = 0
    rejected = 0
    recent_applications = []

    if candidate:
        applications = jobApplication.objects.filter(
            candidate=candidate
        )

        total_applications = applications.count()
        pending = applications.filter(status='Pending').count()
        shortlisted = applications.filter(status='Shortlisted').count()
        selected = applications.filter(status='Selected').count()
        rejected = applications.filter(status='Rejected').count()

        recent_applications = applications.select_related(
            'job'
        ).order_by('-applied_at')[:5]

    return render(
        request,
        'jobs/candidate_dashboard.html',
        {
            'total_applications': total_applications,
            'pending': pending,
            'shortlisted': shortlisted,
            'selected': selected,
            'rejected': rejected,
            'recent_applications': recent_applications
        }
    )

@login_required
def recruiter_dashboard(request):
    profile = Profile.objects.filter(user=request.user).first()

    if profile is None or profile.role != 'recruiter':
        return redirect('home')

    jobs = job.objects.filter(recruter=request.user)

    applications = jobApplication.objects.filter(
        job__in=jobs
    )

    total_jobs = jobs.count()
    total_applicants = applications.count()
    pending = applications.filter(status='Pending').count()
    shortlisted = applications.filter(status='Shortlisted').count()
    selected = applications.filter(status='Selected').count()
    rejected = applications.filter(status='Rejected').count()

    recent_applications = applications.select_related(
        'candidate',
        'candidate__user',
        'job'
    ).order_by('-applied_at')[:5]

    return render(
        request,
        'jobs/recruiter_dashboard.html',
        {
            'total_jobs': total_jobs,
            'total_applicants': total_applicants,
            'pending': pending,
            'shortlisted': shortlisted,
            'selected': selected,
            'rejected': rejected,
            'recent_applications': recent_applications
        }
    )