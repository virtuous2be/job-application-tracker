from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

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



class JobApplicationAPITests(APITestCase):

    def setUp(self):
        """Create a reusable job application for API tests."""
        self.application = JobApplication.objects.create(
            company_name="Microsoft",
            job_title="Junior Software Developer",
        )

        self.list_url = "/api/applications/"
        self.detail_url = f"/api/applications/{self.application.id}/"

    def test_list_applications(self):
        """The API should return all job applications."""
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_application(self):
        """The API should allow users to create a job application."""
        data = {
            "company_name": "Google",
            "job_title": "Python Developer",
            "status": "saved",
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JobApplication.objects.count(), 2)
        self.assertEqual(response.data["company_name"], "Google")

    def test_retrieve_application(self):
        """The API should return one specific job application."""
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["company_name"], "Microsoft")

    def test_update_application(self):
        """The API should allow updating selected application fields."""
        data = {
            "status": "interview",
        }

        response = self.client.patch(
            self.detail_url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.application.refresh_from_db()
        self.assertEqual(self.application.status, "interview")

    def test_delete_application(self):
        """The API should allow deleting a job application."""
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(JobApplication.objects.count(), 0)
