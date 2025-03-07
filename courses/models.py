from datetime import timedelta
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify 
from django.utils.timezone import now
from enum import Enum
from django.core.exceptions import ValidationError
import uuid

USER = settings.AUTH_USER_MODEL

class CourseLevel(models.TextChoices):
    BEGINNER = "beginner", "Beginner"
    INTERMEDIATE = "intermediate", "Intermediate"
    ADVANCED = "advanced", "Advanced"

class ResourceType(models.TextChoices):
    PDF = "pdf", "PDF Document"
    VIDEO = "video", "Video"
    LINK = "link", "External Link"
    FILE = "file", "Other File"

class LessonType(models.TextChoices):
    TEXT = 'text', 'Text Content'
    VIDEO = 'video', 'Video Lesson'
    INTERACTIVE = 'interactive', 'Interactive Practice'
    QUIZ = 'quiz', 'Quiz Assessment'
    TRADING_PRACTICE = 'trading_practice', 'Trading Practice'

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=CourseLevel.choices, default=CourseLevel.BEGINNER)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_course_free = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0) # Track course popularity
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='courses/thumbnails/', blank=True, null=True)
    duration = models.DurationField(null=True, blank=True)
    prerequisites = models.TextField(blank=True)
    learning_objectives = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    # instructor = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='courses')
    
    def get_absolute_url(self):
        return reverse('courses:course-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.is_course_free = self.price == 0.00
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    @property
    def total_students(self):
        return self.enrolled_students.count()

    @property
    def total_modules(self):
        return self.modules.count()

    @property
    def total_lessons(self):
        return Lesson.objects.filter(module__course=self).count()
    
class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']
        unique_together = ['course', 'order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def get_absolute_url(self):
        return reverse('courses:module-detail', kwargs={
            'course_slug': self.course.slug,
            'module_order': self.order
        })
    
    # def save(self, *args, **kwargs):
    #     return super().save(*args, **kwargs)

class Lesson(models.Model):
    # module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons")
    # title = models.CharField(max_length=250)
    # content = models.TextField()
    # order = models.PositiveIntegerField(default=1)
    # video_url = models.URLField(blank=True, null=True)
    # duration = models.DurationField(null=True, blank=True)
    # is_preview = models.BooleanField(default=False)  # For free preview lessons
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=250)
    lesson_type = models.CharField(
        max_length=20, 
        choices=LessonType.choices,
        default=LessonType.TEXT
    )
    content = models.TextField()  # Regular text content
    video_url = models.URLField(blank=True, null=True)
    trading_pair = models.CharField(max_length=20, blank=True, default='eur/usd')  # For trading practice
    chart_timeframe = models.CharField(max_length=10, blank=True, default='D')  # For trading practice
    practice_instructions = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)
    duration = models.DurationField(null=True, blank=True)
    is_preview = models.BooleanField(default=False)
    
    class Meta:
        ordering = ["order"]
        unique_together = ['module', 'order']

    def clean(self):
        if self.lesson_type == LessonType.VIDEO and not self.video_url:
            raise ValidationError({'video_url': 'Video URL is required for video lessons.'})
        if self.lesson_type == LessonType.TRADING_PRACTICE and not self.trading_pair:
            raise ValidationError({'trading_pair': 'Trading pair is required for trading practice lessons.'})
        
    def get_absolute_url(self):
        return reverse('courses:lesson-detail', kwargs={
            'course_slug': self.module.course.slug,
            'module_order': self.module.order,
            'lesson_order': self.order
        })

    def get_next_lesson(self):
        return Lesson.objects.filter(
            module=self.module,
            order__gt=self.order
        ).first()

    def get_previous_lesson(self):
        return Lesson.objects.filter(
            module=self.module,
            order__lt=self.order
        ).last()
    
    def get_content_template(self):
        """Returns the appropriate template for the lesson type"""
        return f'courses/lesson_types/{self.lesson_type}_lesson.html'

    def __str__(self):
        return f"{self.title} -{self.module.title}"  
    
class Resource(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="resources")
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=20, choices=ResourceType.choices)
    file = models.FileField(upload_to='course_resources/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.lesson.title}"
    
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
    last_accessed_lesson = models.ForeignKey(
        Lesson, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='last_accessed'
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    time_spent = models.DurationField(default=timedelta(0))

    # def update_progress(self):
    #     total_lessons = self.course.lessons.count()
    #     if total_lessons > 0:
    #         completed_count = self.completed_lessons.count()
    #         self.progress = (completed_count / total_lessons) * 100
    #         if self.progress == 100:
    #             self.completed_at = now()
    #     self.save()

    def update_progress(self):
        total_lessons = Lesson.objects.filter(module__course=self.course).count()
        if total_lessons > 0:
            completed_count = self.completed_lessons.count()
            self.progress = (completed_count / total_lessons) * 100
            if self.progress == 100 and not self.completed_at:
                self.completed_at = now()
                # Trigger certificate creation
                Certificate.objects.get_or_create(
                    user=self.user,
                    course=self.course
                )
        self.save()

    def get_module_progress(self, module):
        total_lessons = module.lessons.count()
        if total_lessons == 0:
            return 0
        completed_lessons = self.completed_lessons.filter(module=module).count()
        return (completed_lessons / total_lessons) * 100

    def get_detailed_progress(self):
        """Returns detailed progress information"""
        return {
            'overall_progress': self.progress,
            'time_spent': self.time_spent,
            'modules_progress': [
                {
                    'module': module,
                    'progress': self.get_module_progress(module),
                    'completed_lessons': self.completed_lessons.filter(module=module).count(),
                    'total_lessons': module.lessons.count()
                }
                for module in self.course.modules.all()
            ],
            'last_activity': self.last_accessed_lesson.title if self.last_accessed_lesson else None,
            'completion_rate': self.calculate_completion_rate()
        }

    def calculate_completion_rate(self):
        """Calculate the rate of completion (lessons per day)"""
        if not self.completed_lessons.exists():
            return 0
        
        first_completion = self.completed_lessons.order_by('courseprogress__completed_at').first()
        last_completion = self.completed_lessons.order_by('-courseprogress__completed_at').first()
        
        if first_completion == last_completion:
            return 1
        
        days = (last_completion.courseprogress__completed_at - first_completion.courseprogress__completed_at).days
        return self.completed_lessons.count() / (days or 1)

    def __str__(self):
        return f"{self.user.email} - {self.course.title} ({self.progress}%)"
    
class LessonProgress(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_spent = models.DurationField(default=timedelta(0))
    last_position = models.PositiveIntegerField(default=0)  # For video progress
    practice_attempts = models.PositiveIntegerField(default=0)
    practice_success = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'lesson']

    def update_time_spent(self):
        if self.completed_at:
            self.time_spent = self.completed_at - self.started_at
        self.save()

class Certificate(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_id_one = models.UUIDField(default=uuid.uuid1, unique=True, editable=False)
    certificate_id_four = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self):
        return f"Certificate {self.certificate_id_four} - {self.user.email} ({self.course.title})"    

    def get_absolute_url(self):
        return reverse('courses:certificate-detail', kwargs={
            'certificate_id': self.certificate_id_four
        })    
    
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
    
class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    passing_score = models.PositiveIntegerField(default=70)  # Percentage

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.PositiveIntegerField(default=1)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

class QuizAttempt(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    completed_at = models.DateTimeField(auto_now_add=True)
    passed = models.BooleanField(default=False)
    