from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.http import HttpResponseForbidden
from .models import User, RecruiterProfile, JobSeekerProfile, JobPosting, Application, SavedJob
from .forms import UserRegistrationForm, UserLoginForm, RecruiterProfileForm, JobSeekerProfileForm, JobPostingForm, ApplicationForm
from django.db.models import Q



# Helper checks
def is_recruiter(user):
    return user.is_authenticated and user.user_type == 'recruiter'

def is_seeker(user):
    return user.is_authenticated and user.user_type == 'seeker'

# Home page with general job search/listing
def home(request):
    jobs = JobPosting.objects.filter(is_active=True).order_by('-date_posted')
    return render(request, 'jobs/home.html', {'jobs': jobs})


def search_jobs(request):
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')

    jobs = JobPosting.objects.filter(is_active=True)

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(company_name__icontains=query)
        )

    if location:
        jobs = jobs.filter(location__icontains=location)

    jobs = jobs.order_by('-date_posted')

    return render(request, 'jobs/home.html', {'jobs': jobs})

# User registration view
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                user_type=form.cleaned_data['user_type']
            )
            # Create corresponding profile
            if user.user_type == 'recruiter':
                RecruiterProfile.objects.create(user=user)
            else:
                JobSeekerProfile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'jobs/register.html', {'form': form})

# User login view
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = UserLoginForm()
    return render(request, 'jobs/login.html', {'form': form})

# Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

# Profile view and edit
@login_required
def profile(request):
    user = request.user
    if user.user_type == 'recruiter':
        profile = get_object_or_404(RecruiterProfile, user=user)
        ProfileForm = RecruiterProfileForm
    else:
        profile = get_object_or_404(JobSeekerProfile, user=user)
        ProfileForm = JobSeekerProfileForm

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'jobs/profile.html', {'form': form})

# Recruiter dashboard
@login_required
@user_passes_test(is_recruiter)
def recruiter_dashboard(request):
    recruiter = get_object_or_404(RecruiterProfile, user=request.user)
    jobs = JobPosting.objects.filter(recruiter=recruiter)
    applications = Application.objects.filter(job__in=jobs).order_by('-application_date')[:10]
    context = {
        'jobs': jobs,
        'applications': applications,
    }
    return render(request, 'jobs/recruiter_dashboard.html', context)

# Create job posting
@login_required
@user_passes_test(is_recruiter)
def create_job(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = get_object_or_404(RecruiterProfile, user=request.user)
            job.save()
            return redirect('recruiter_dashboard')
    else:
        form = JobPostingForm()
    return render(request, 'jobs/create_job.html', {'form': form})

# Manage jobs list
@login_required
@user_passes_test(is_recruiter)
def manage_jobs(request):
    recruiter = get_object_or_404(RecruiterProfile, user=request.user)
    jobs = JobPosting.objects.filter(recruiter=recruiter)
    return render(request, 'jobs/manage_jobs.html', {'jobs': jobs})

# Edit job posting
@login_required
@user_passes_test(is_recruiter)
def edit_job(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id, recruiter__user=request.user)
    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('manage_jobs')
    else:
        form = JobPostingForm(instance=job)
    return render(request, 'jobs/edit_job.html', {'form': form, 'job': job})

# Delete job posting
@login_required
@user_passes_test(is_recruiter)
def delete_job(request, job_id):
    if request.method == 'POST':
        job = get_object_or_404(JobPosting, id=job_id, recruiter__user=request.user)
        job.delete()
        return redirect('manage_jobs')
    return HttpResponseForbidden()

# View applications for a specific job
@login_required
@user_passes_test(is_recruiter)
def view_applications(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id, recruiter__user=request.user)
    applications = Application.objects.filter(job=job).order_by('-application_date')
    return render(request, 'jobs/view_applications.html', {'job': job, 'applications': applications})

# Update application status
@login_required
@user_passes_test(is_recruiter)
def application_status(request, app_id):
    if request.method == 'POST':
        application = get_object_or_404(Application, id=app_id, job__recruiter__user=request.user)
        status = request.POST.get('status')
        if status in dict(Application.STATUS_CHOICES).keys():
            application.status = status
            application.save()
        return redirect('view_applications', job_id=application.job.id)
    return HttpResponseForbidden()

# List all available jobs (public)
def jobs_list(request):
    jobs = JobPosting.objects.filter(is_active=True).order_by('-date_posted')
    return render(request, 'jobs/jobs_list.html', {'jobs': jobs})

# Job details page (public)
def job_detail(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id, is_active=True)
    return render(request, 'jobs/job_detail.html', {'job': job})

# Job application page
@login_required
@user_passes_test(is_seeker)
def apply_job(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id, is_active=True)
    seeker_profile = get_object_or_404(JobSeekerProfile, user=request.user)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.seeker = seeker_profile
            application.save()
            return redirect('applications_track')
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})

# Track all job applications by the seeker
@login_required
@user_passes_test(is_seeker)
def applications_track(request):
    seeker_profile = get_object_or_404(JobSeekerProfile, user=request.user)
    applications = Application.objects.filter(seeker=seeker_profile).order_by('-application_date')
    return render(request, 'jobs/applications_track.html', {'applications': applications})

# Save a job (for seekers)
@login_required
@user_passes_test(is_seeker)
def save_job(request, job_id):
    if request.method == 'POST':
        job = get_object_or_404(JobPosting, id=job_id, is_active=True)
        seeker_profile = get_object_or_404(JobSeekerProfile, user=request.user)
        SavedJob.objects.get_or_create(job=job, seeker=seeker_profile)
        return redirect('saved_jobs')
    return HttpResponseForbidden()

# View saved jobs
@login_required
@user_passes_test(is_seeker)
def saved_jobs(request):
    seeker_profile = get_object_or_404(JobSeekerProfile, user=request.user)
    saved_jobs = SavedJob.objects.filter(seeker=seeker_profile).select_related('job').order_by('-date_saved')
    return render(request, 'jobs/saved_jobs.html', {'saved_jobs': saved_jobs})
