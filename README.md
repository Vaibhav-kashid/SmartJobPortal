# SmartJobPortal

A Django web application where recruiters post jobs and candidates browse and apply for them.

## Features
- User registration and login with Candidate and Recruiter roles
- Recruiters can create job postings and view the applicants for each job
- Candidates can browse jobs, view job details and apply
- "My Applications" page with application status
- Separate dashboards for candidates and recruiters

## Tech Stack
Python, Django, HTML, CSS, SQLite

## Run Locally
```bash
git clone https://github.com/Vaibhav-kashid/SmartJobPortal.git
cd SmartJobPortal
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Then open http://127.0.0.1:8000/

## Project Structure
- `account/` - registration, login, user profiles and roles
- `jobs/` - job postings, applications, dashboards
- `matching/` - job matching (in progress)

## Author
Vaibhav Kashid