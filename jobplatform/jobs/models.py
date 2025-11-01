from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('recruiter', 'Recruiter'),
        ('seeker', 'Job Seeker'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    groups = models.ManyToManyField(
        Group,
        related_name='job_users',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
        related_query_name='job_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='job_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
        related_query_name='job_user',
    )




class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    company_description = models.TextField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.company_name

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    headline = models.CharField(max_length=255)
    resume_file = models.FileField(upload_to='resumes/')
    skills = models.TextField()

    def __str__(self):
        return self.full_name

# class JobPosting(models.Model):
#     recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     location = models.CharField(max_length=255)
#     salary = models.DecimalField(max_digits=10, decimal_places=2)
#     date_posted = models.DateField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.title


class JobPosting(models.Model):
    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, blank=True, null=True)  # Optional, fallback to RecruiterProfile company_name
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    job_type = models.CharField(max_length=50, default='Full-time')  # Add this field
    date_posted = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.company_name and self.recruiter:
            self.company_name = self.recruiter.company_name
        super().save(*args, **kwargs)


class Application(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    seeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE)
    application_date = models.DateField(auto_now_add=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('interview', 'Interview'),
        ('reviewed', 'Reviewed'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    cover_letter_text = models.TextField()

    def __str__(self):
        return f"Application by {self.seeker} for {self.job}"

class SavedJob(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    seeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE)
    date_saved = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.seeker} saved {self.job}"

