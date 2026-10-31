from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import JobApplication


class JobApplicationModelTests(TestCase):

    def setUp(self):
        """Create a reusable job application for the tests."""
        self.application = JobApplication.objects.create(
            company_name="Microsoft",
            job_title="Junior Software Developer",
        )

    def test_job_application_is_created(self):
        """A job application should be saved in the database."""
        self.assertEqual(JobApplication.objects.count(), 1)

    def test_default_status_is_saved(self):
        """New applications should have the default status 'saved'."""
        self.assertEqual(self.application.status, "saved")

    def test_string_representation(self):
        """The application should have a readable string representation."""
        self.assertEqual(
            str(self.application),
            "Junior Software Developer at Microsoft",
        )

    def test_optional_fields_can_be_saved(self):
        """Optional job information should be stored correctly."""
        application = JobApplication.objects.create(
            company_name="Google",
            job_title="Python Developer",
            job_url="https://example.com/jobs/python-developer",
            deadline_date=date(2026, 11, 15),
            date_applied=date(2026, 10, 30),
            contact_name="Jane Smith",
            contact_email="jane@example.com",
            status="applied",
            notes="Application submitted online.",
        )

        self.assertEqual(application.company_name, "Google")
        self.assertEqual(application.status, "applied")
        self.assertEqual(application.deadline_date, date(2026, 11, 15))
        self.assertEqual(application.date_applied, date(2026, 10, 30))
        self.assertEqual(application.contact_email, "jane@example.com")

    def test_created_at_is_set_automatically(self):
        """Django should automatically set the creation timestamp."""
        self.assertIsNotNone(self.application.created_at)

    def test_invalid_status_fails_validation(self):
        """Only the defined status choices should be accepted."""
        application = JobApplication(
            company_name="Amazon",
            job_title="Backend Developer",
            status="invalid_status",
        )

        with self.assertRaises(ValidationError):
            application.full_clean()