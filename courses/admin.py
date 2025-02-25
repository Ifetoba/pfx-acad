from django.contrib import admin
from .models import (
    Course,
    Lesson,
    CourseEnrollment,
    CourseProgress,
    Certificate,
    Webinar,
    WebinarRegistration,
    Order
)

# Register your models here.
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(CourseEnrollment)
admin.site.register(CourseProgress)
admin.site.register(Certificate)
admin.site.register(Webinar)
admin.site.register(WebinarRegistration)
admin.site.register(Order)