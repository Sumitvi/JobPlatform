from django.urls import path
from . import views

urlpatterns = [
    # General and Auth URLs
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),

    # Recruiter URLs
    path('recruiter/dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('jobs/create/', views.create_job, name='create_job'),
    path('jobs/manage/', views.manage_jobs, name='manage_jobs'),
    path('jobs/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('jobs/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('jobs/<int:job_id>/applications/', views.view_applications, name='view_applications'),
    path('applications/<int:app_id>/status/', views.application_status, name='application_status'),

    # Job Seeker URLs
    path('jobs/', views.jobs_list, name='jobs_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('applications/track/', views.applications_track, name='applications_track'),
    path('jobs/<int:job_id>/save/', views.save_job, name='save_job'),
    path('saved-jobs/', views.saved_jobs, name='saved_jobs'),

    path('search/jobs/', views.search_jobs, name='search_jobs')

]
