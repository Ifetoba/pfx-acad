from django.contrib import admin
from .models import (
    Course,
    Lesson,
    CourseEnrollment,
    CourseProgress,
    Certificate,
    Webinar,
    WebinarRegistration,
    Order, 
    Resource,
    Module,
)

# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)
admin.site.register(CourseEnrollment)
admin.site.register(CourseProgress)
admin.site.register(Certificate)
admin.site.register(Webinar)
admin.site.register(WebinarRegistration)
admin.site.register(Order)
admin.site.register(Module)
admin.site.register(Resource)