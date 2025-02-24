from django.db import models
from django.conf import settings
from django.utils.text import slugify 
from django.utils.timezone import now
from enum import Enum
import uuid

USER = settings.AUTH_USER_MODEL

class CourseLevel(Enum):
    BEGINNER = 'Beginner'
    INTERMEDIATE = 'Intermediate'
    ADVANCED = 'Advanced'

    @classmethod
    def choices(cls):
         return [(level.name , level.value) for level in cls]

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=CourseLevel.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_course_free = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0) # Track course popularity
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.is_free = self.price == 0.00
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=250)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    content = models.TextField() # Lesson details or summary
    order = models.SmallIntegerField(default=1)
    video_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.title} -{self.course.title}"  
    
class CourseEnrollment(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrolled_students")
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.00) # Progress in %

    class Meta:
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user.email} enrolled in {self.course.title}"


class CourseProgress(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.00) # % Completion
    completed_lessons = models.ManyToManyField(Lesson, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def update_progress(self):
        total_lessons = self.course.lessons.count()
        if total_lessons > 0:
            completed_count = self.completed_lessons.count()
            self.progress = (completed_count / total_lessons) * 100
            if self.progress == 100:
                self.completed_at = now()
        self.save()

    def __str__(self):
        return f"{self.user.email} - {self.course.title} ({self.progress}%)"
    
class Certificate(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_id_one = models.UUIDField(default=uuid.uuid1, unique=True, editable=False)
    certificate_id_four = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self):
        return f"Certificate {self.certificate_id_four} - {self.user.email} ({self.course.title})"        
    
class Webinar(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(USER, on_delete=models.CASCADE, limit_choices_to={"role" : "instructor"})
    date = models.DateTimeField()
    registration_deadline = models.DateTimeField()
    webinar_link = models.URLField()
    is_live = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class WebinarRegistration(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE, related_name="registrations")
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "webinar")

    def __str__(self):
        return f"{self.user.email} registered for {self.webinar.title}"

class Order(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    stripe_payment_intent = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.email} ({'Paid' if self.is_paid else 'Pending'})"
    