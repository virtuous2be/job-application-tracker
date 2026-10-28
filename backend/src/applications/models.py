from django.db import models

# Create your models here.

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ("saved", "Saved"),
        ("applied", "Applied"),
        ("interview", "Interview"),
        ("offer", "Offer"),
        ("rejected", "Rejected"),
    ]

    # Required job information
    company_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)

    # Optional job information
    job_url = models.URLField(blank=True)
    deadline_date = models.DateField(null=True, blank=True)
    date_applied = models.DateField(null=True, blank=True)
    contact_name = models.CharField(max_length=200, blank=True)
    contact_email = models.EmailField(blank=True)

    # Application tracking
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="saved",
    )

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"
