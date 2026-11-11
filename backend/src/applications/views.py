from django.shortcuts import render

from rest_framework import viewsets

from .models import JobApplication
from .serializers import JobApplicationSerializer


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all().order_by("-created_at")
    serializer_class = JobApplicationSerializer