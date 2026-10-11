from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm
from .models import Profile, Candidate, recruter


# Register User
def register(request):

    if request.method == 'POST':

        form = RegistrationForm(request.POST)

        if form.is_valid():

            # Create User
            user = form.save(commit=False)

            # Encrypt password
            user.set_password(
                form.cleaned_data['password']
            )

            user.save()

            # Get selected role
            role = form.cleaned_data['role']

            # Create Profile
            Profile.objects.create(
                user=user,
                role=role
            )

            # Create Candidate Profile
            if role == 'candidate':

                Candidate.objects.create(
                    user=user,
                    phone='',
                    skills='',
                    education=''
                )

            # Create Recruiter Profile
            elif role == 'recruiter':

                recruter.objects.create(
                    user=user,
                    company_name='',
                    phone=''
                )

            # Registration successful
            return redirect('login')

        else:
            print("Registration Error:")
            print(form.errors)

    else:
        form = RegistrationForm()

    return render(
        request,
        'account/register.html',
        {'form': form}
    )


# Login User
def user_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        else:

            return render(
                request,
                'account/login.html',
                {
                    'error': 'Invalid Username or Password'
                }
            )

    return render(
        request,
        'account/login.html'
    )


# Logout User
def user_logout(request):

    logout(request)

    return redirect('login')


# Home Page
# Home Page
@login_required
def home(request):

    user_role = None

    if request.user.is_authenticated:

        profile = Profile.objects.filter(
            user=request.user
        ).first()

        if profile:
            user_role = profile.role

    return render(
        request,
        'account/home.html',
        {
            'user_role': user_role
        }
    )