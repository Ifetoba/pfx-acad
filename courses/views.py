from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import (
    Course,
    CourseLevel,
    CourseEnrolment,
    CourseProgress,
    Certificate,)
# Create your views here.
