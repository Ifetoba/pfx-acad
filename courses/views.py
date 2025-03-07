# import uuid
# from django.core.mail import send_mail
# from django.conf import settings
# from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from django.utils.timezone import now
# from django.views.generic import ListView, DetailView
# from users.models import CustomUser
# from .models import (
#     Course,
#     Lesson,
#     CourseEnrollment,
#     CourseProgress,
#     Certificate,
#     Webinar,
#     WebinarRegistration,)

# # Create your views here.
# class CourseListView(ListView):
#     model = Course
#     template_name = "courses/course_list.html"
#     context_object_name = "courses"

# class CourseDetailView(DetailView):
#     model = Course
#     template_name = "courses/course_detail.html"

#     def get_context_data(self, **kwargs) -> dict[str, any]:
#         context = super().get_context_data(**kwargs)
#         context["courses"] = Course.objects.all()
#         context["lessons"] = Lesson.objects.all()
#         return context
    
# def enroll_user_in_course(user, course_id):
#     course = Course.objects.get(id=course_id)
#     enrollment, created = CourseEnrollment.objects.get_or_create(user=user, course=course)

#     if created:
#         subject = f"Enrollment Confirmation - {course.title}"
#         message = f"Hi {user.full_name},\n\nYou have successfully enrolled in {course.title}!"
#         send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])    

# @login_required
# def enroll_course(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
#     enrollment, created = CourseEnrollment.objects.get_or_create(user=request.user, course=course) 

#     if created:
#         CourseProgress.objects.create(user=request.user, course=course)
#         message = "Successfull enrolled!"
#     else:
#         message = "Already enrolled"

#     return render(request, 
#                   "courses/enrollment_success.html", 
#                   {"course": course, "message": message}
#                   )

# @login_required
# def complete_lesson(request, course_id, lesson_id):
#     progress = get_object_or_404(CourseProgress, user=request.user, course_id=course_id)
#     lesson = get_object_or_404(Lesson, pk=lesson_id, course_id=course_id)

#     if lesson not in progress.completed_lessons.all():
#         progress.completed_lessons.add(lesson)
#         progress.update_progress()

#         if progress.progress == 100:
#             Certificate.objects.create(user=request.user, course_id=course_id, certificate_id_four=str(uuid.uuid4()))
#     return JsonResponse({
#         "progress": progress.progress,
#         "completed": list(progress.completed_lessons.values("id", "title"))
#     })

# @login_required
# def register_for_webinar(request, webinar_id):
#     webinar = get_object_or_404(Webinar, id=webinar_id)

#     if webinar.registration_deadline < now():
#         return JsonResponse({"error": "Registration closed"}, status=400)
    
#     registration, created = WebinarRegistration.objects.get_or_create(user=request.user, webinar=webinar)

#     if created:
#         return JsonResponse({"message": "Registered successfully!"})
#     return JsonResponse({"message": "Already registered."})

# import uuid
# from django.core.mail import send_mail
# from django.conf import settings
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.http import JsonResponse
# from django.utils.timezone import now
# from django.views.generic import ListView, DetailView
# from django.db.models import Prefetch
# from users.models import CustomUser
# from .models import (
#     Course,
#     Module,
#     Lesson,
#     CourseEnrollment,
#     CourseProgress,
#     Certificate,
#     Webinar,
#     WebinarRegistration,
# )

# class CourseListView(ListView):
#     model = Course
#     template_name = "courses/course_list.html"
#     context_object_name = "courses"
    
#     def get_queryset(self):
#         return Course.objects.filter(is_published=True).order_by('-created_at')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.user.is_authenticated:
#             context['enrolled_courses'] = Course.objects.filter(
#                 enrolled_students__user=self.request.user
#             )
#         return context

# class CourseDetailView(DetailView):
#     model = Course
#     template_name = "courses/course_detail.html"

#     def get_queryset(self):
#         return Course.objects.prefetch_related(
#             Prefetch('modules', queryset=Module.objects.prefetch_related('lessons'))
#         )

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         course = self.get_object()
        
#         if self.request.user.is_authenticated:
#             # Get enrollment status
#             context['is_enrolled'] = CourseEnrollment.objects.filter(
#                 user=self.request.user,
#                 course=course
#             ).exists()
            
#             # Get course progress if enrolled
#             if context['is_enrolled']:
#                 progress = CourseProgress.objects.get(
#                     user=self.request.user,
#                     course=course
#                 )
#                 context['progress'] = progress
#                 context['completed_lessons'] = progress.completed_lessons.all()
        
#         return context

# @login_required
# def module_detail(request, course_slug, module_order):
#     course = get_object_or_404(Course, slug=course_slug)
#     module = get_object_or_404(Module, course=course, order=module_order)
    
#     # Check if user is enrolled
#     if not CourseEnrollment.objects.filter(user=request.user, course=course).exists():
#         messages.error(request, "You must be enrolled to access this module.")
#         return redirect('courses:course-detail', slug=course_slug)
    
#     progress = CourseProgress.objects.get(user=request.user, course=course)
    
#     context = {
#         'course': course,
#         'module': module,
#         'lessons': module.lessons.all().order_by('order'),
#         'progress': progress,
#         'completed_lessons': progress.completed_lessons.all()
#     }
#     return render(request, 'courses/module_detail.html', context)

# @login_required
# def lesson_detail(request, course_slug, module_order, lesson_order):
#     course = get_object_or_404(Course, slug=course_slug)
#     module = get_object_or_404(Module, course=course, order=module_order)
#     lesson = get_object_or_404(Lesson, module=module, order=lesson_order)
    
#     # Check if user is enrolled
#     if not CourseEnrollment.objects.filter(user=request.user, course=course).exists():
#         messages.error(request, "You must be enrolled to access this lesson.")
#         return redirect('courses:course-detail', slug=course_slug)
    
#     progress = CourseProgress.objects.get(user=request.user, course=course)
    
#     # Update last accessed lesson
#     progress.last_accessed_lesson = lesson
#     progress.save()
    
#     context = {
#         'course': course,
#         'module': module,
#         'lesson': lesson,
#         'progress': progress,
#         'completed_lessons': progress.completed_lessons.all(),
#         'next_lesson': lesson.get_next_lesson(),
#         'previous_lesson': lesson.get_previous_lesson(),
#     }
#     return render(request, 'courses/lesson_detail.html', context)

# @login_required
# def enroll_course(request, course_id):
#     course = get_object_or_404(Course, id=course_id)
    
#     # Check if course is free or payment is required
#     if not course.is_course_free:
#         # Redirect to payment process
#         return redirect('payments:process', course_id=course_id)
    
#     enrollment, created = CourseEnrollment.objects.get_or_create(
#         user=request.user, 
#         course=course
#     ) 

#     if created:
#         CourseProgress.objects.create(user=request.user, course=course)
        
#         # Send enrollment email
#         subject = f"Welcome to {course.title}"
#         message = f"""
#         Hi {request.user.get_full_name()},

#         Welcome to {course.title}! You can now access all course materials.
        
#         Get started here: {request.build_absolute_uri(course.get_absolute_url())}
        
#         Happy learning!
#         """
#         send_mail(
#             subject,
#             message,
#             settings.DEFAULT_FROM_EMAIL,
#             [request.user.email]
#         )
        
#         messages.success(request, "Successfully enrolled!")
#     else:
#         messages.info(request, "You are already enrolled in this course.")

#     return redirect('courses:course-detail', slug=course.slug)

# @login_required
# def complete_lesson(request, course_slug, module_order, lesson_order):
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Invalid request method'}, status=400)
    
#     course = get_object_or_404(Course, slug=course_slug)
#     module = get_object_or_404(Module, course=course, order=module_order)
#     lesson = get_object_or_404(Lesson, module=module, order=lesson_order)
    
#     progress = get_object_or_404(CourseProgress, 
#         user=request.user, 
#         course=course
#     )

#     if lesson not in progress.completed_lessons.all():
#         progress.completed_lessons.add(lesson)
#         progress.update_progress()

#         # Check if course is completed
#         if progress.progress == 100:
#             certificate = Certificate.objects.create(
#                 user=request.user,
#                 course=course,
#                 certificate_id_four=uuid.uuid4()
#             )
#             return JsonResponse({
#                 'progress': progress.progress,
#                 'completed': True,
#                 'certificate_url': certificate.get_absolute_url()
#             })

#     return JsonResponse({
#         'progress': progress.progress,
#         'completed': False,
#         'completed_lessons': list(progress.completed_lessons.values_list('id', flat=True))
#     })

# # Your existing webinar views...
# @login_required
# def register_for_webinar(request, webinar_id):
#     webinar = get_object_or_404(Webinar, id=webinar_id)

#     if webinar.registration_deadline < now():
#         return JsonResponse({"error": "Registration closed"}, status=400)
    
#     registration, created = WebinarRegistration.objects.get_or_create(user=request.user, webinar=webinar)

#     if created:
#         return JsonResponse({"message": "Registered successfully!"})
#     return JsonResponse({"message": "Already registered."})

import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils.timezone import now
from django.urls import reverse

from .models import (
    Course, Module, Lesson, CourseEnrollment, CourseProgress,
    Certificate, Webinar, WebinarRegistration
)

class CourseListView(ListView):
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"

    def get_queryset(self):
        return Course.objects.filter(is_published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['enrolled_courses'] = Course.objects.filter(
                enrolled_students__user=self.request.user
            )
        return context

class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Check enrollment status
            context['is_enrolled'] = CourseEnrollment.objects.filter(
                user=self.request.user,
                course=self.object
            ).exists()
            
            if context['is_enrolled']:
                progress = CourseProgress.objects.get(
                    user=self.request.user,
                    course=self.object
                )
                context['progress'] = progress
                context['completed_lessons'] = progress.completed_lessons.all()
        return context

# class ModuleDetailView(LoginRequiredMixin, DetailView):
#     model = Module
#     template_name = "courses/module_detail.html"
    
#     def get_object(self):
#         return get_object_or_404(
#             Module,
#             course__slug=self.kwargs['course_slug'],
#             order=self.kwargs['module_order']
#         )

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         module = self.object
#         course = module.course
        
#         # Check enrollment
#         if not CourseEnrollment.objects.filter(
#             user=self.request.user, course=course
#         ).exists():
#             messages.error(self.request, "You must be enrolled to access this module.")
#             return redirect('courses:course-detail', slug=course.slug)
        
#         progress = CourseProgress.objects.get(user=self.request.user, course=course)
        
#         # Calculate module progress
#         total_lessons = module.lessons.count()
#         completed_lessons = progress.completed_lessons.filter(module=module).count()
#         module_progress = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
        
#         context.update({
#             'course': course,
#             'lessons': module.lessons.all().order_by('order'),
#             'progress': progress,
#             'completed_lessons': progress.completed_lessons.all(),
#             'module_progress': module_progress
#         })
#         return context

class ModuleDetailView(LoginRequiredMixin, DetailView):
    model = Module
    template_name = 'courses/module_detail.html'
    
    def get_object(self):
        return get_object_or_404(
            Module,
            course__slug=self.kwargs['course_slug'],
            order=self.kwargs['module_order']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        module = self.object
        course = module.course
        
        # Check enrollment
        if not CourseEnrollment.objects.filter(
            user=self.request.user,
            course=course
        ).exists():
            messages.error(self.request, "You must be enrolled to access this module.")
            return redirect('courses:course-detail', slug=course.slug)
        
        # Get progress
        progress = CourseProgress.objects.get(user=self.request.user, course=course)
        
        # Calculate module progress
        total_lessons = module.lessons.count()
        completed_lessons = progress.completed_lessons.filter(module=module)
        module_progress = (completed_lessons.count() / total_lessons * 100) if total_lessons > 0 else 0
        
        # Get previous and next modules
        previous_module = Module.objects.filter(
            course=course,
            order__lt=module.order
        ).last()
        
        next_module = Module.objects.filter(
            course=course,
            order__gt=module.order
        ).first()
        
        context.update({
            'course': course,
            'progress': progress,
            'completed_lessons': completed_lessons,
            'module_progress': module_progress,
            'previous_module': previous_module,
            'next_module': next_module,
        })
        return context

class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = "courses/lesson_detail.html"
    
    def get_object(self):
        return get_object_or_404(
            Lesson,
            module__course__slug=self.kwargs['course_slug'],
            module__order=self.kwargs['module_order'],
            order=self.kwargs['lesson_order']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.object
        module = lesson.module
        course = module.course
        
        # Check enrollment
        if not CourseEnrollment.objects.filter(
            user=self.request.user, course=course
        ).exists():
            messages.error(self.request, "You must be enrolled to access this lesson.")
            return redirect('courses:course-detail', slug=course.slug)
        
        progress = CourseProgress.objects.get(user=self.request.user, course=course)
        
        # Update last accessed lesson
        progress.last_accessed_lesson = lesson
        progress.save()
        
        context.update({
            'course': course,
            'module': module,
            'progress': progress,
            'completed_lessons': progress.completed_lessons.all(),
            'next_lesson': lesson.get_next_lesson(),
            'previous_lesson': lesson.get_previous_lesson(),
        })
        return context

class ProgressDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "courses/progress_dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get enrollments with progress
        enrollments = CourseEnrollment.objects.filter(user=user)
        
        # Get course progress
        progress_records = CourseProgress.objects.filter(user=user)
        
        # Categorize courses
        completed_courses = progress_records.filter(progress=100)
        in_progress_courses = progress_records.filter(progress__gt=0, progress__lt=100)
        
        # Get certificates
        certificates = Certificate.objects.filter(user=user)
        
        context.update({
            'enrollments': enrollments,
            'active_enrollments': enrollments.filter(
                course__in=in_progress_courses.values_list('course', flat=True)
            ),
            'completed_courses': completed_courses,
            'in_progress_courses': in_progress_courses,
            'certificates': certificates,
        })
        return context

class CertificateDetailView(LoginRequiredMixin, DetailView):
    model = Certificate
    template_name = "courses/certificate_view.html"
    slug_field = 'certificate_id_four'
    slug_url_kwarg = 'certificate_id'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if course is free or payment is required
    if not course.is_course_free:
        # Redirect to payment process
        return redirect('payments:process', course_id=course_id)
    
    enrollment, created = CourseEnrollment.objects.get_or_create(
        user=request.user, 
        course=course
    ) 

    if created:
        CourseProgress.objects.create(user=request.user, course=course)
        
        # Send enrollment email
        subject = f"Welcome to {course.title}"
        message = f"""
        Hi {request.user.get_full_name()},

        Welcome to {course.title}! You can now access all course materials.
        
        Get started here: {request.build_absolute_uri(course.get_absolute_url())}
        
        Happy learning!
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [request.user.email]
        )
        
        messages.success(request, "Successfully enrolled!")
    else:
        messages.info(request, "You are already enrolled in this course.")

    return redirect('courses:course-detail', slug=course.slug)

# @login_required
# def complete_lesson(request, course_slug, module_order, lesson_order):
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Invalid request method'}, status=400)
    
#     lesson = get_object_or_404(
#         Lesson,
#         module__course__slug=course_slug,
#         module__order=module_order,
#         order=lesson_order
#     )
    
#     progress = get_object_or_404(
#         CourseProgress,
#         user=request.user,
#         course=lesson.module.course
#     )

#     if lesson not in progress.completed_lessons.all():
#         progress.completed_lessons.add(lesson)
#         progress.update_progress()

#         response_data = {
#             'progress': progress.progress,
#             'completed': True,
#             'completed_lessons': list(progress.completed_lessons.values_list('id', flat=True))
#         }

#         # Check if course is completed
#         if progress.progress == 100:
#             certificate = Certificate.objects.create(
#                 user=request.user,
#                 course=lesson.module.course
#             )
#             response_data['certificate_url'] = reverse(
#                 'courses:certificate-detail',
#                 kwargs={'certificate_id': certificate.certificate_id_four}
#             )

#         return JsonResponse(response_data)
    
#     return JsonResponse({
#         'progress': progress.progress,
#         'completed': False
#     })

@login_required
def complete_lesson(request, course_slug, module_order, lesson_order):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    lesson = get_object_or_404(
        Lesson,
        module__course__slug=course_slug,
        module__order=module_order,
        order=lesson_order
    )
    
    module = lesson.module
    course = module.course
    
    progress = get_object_or_404(
        CourseProgress,
        user=request.user,
        course=course
    )

    # Mark lesson as complete
    if lesson not in progress.completed_lessons.all():
        progress.completed_lessons.add(lesson)
        progress.update_progress()

        # Check if module is completed
        module_lessons = module.lessons.count()
        completed_module_lessons = progress.completed_lessons.filter(module=module).count()
        module_completed = module_lessons == completed_module_lessons

        response_data = {
            'status': 'success',
            'lesson_id': lesson.id,
            'progress': progress.progress,
            'module_completed': module_completed,
            'completed_lessons': list(progress.completed_lessons.values_list('id', flat=True))
        }

        # Only create certificate if module is completed
        if module_completed:
            # Check if all modules are completed before creating certificate
            all_modules_completed = all(
                progress.completed_lessons.filter(module=m).count() == m.lessons.count()
                for m in course.modules.all()
            )
            
            if all_modules_completed:
                certificate, created = Certificate.objects.get_or_create(
                    user=request.user,
                    course=course
                )
                response_data['certificate_url'] = reverse(
                    'courses:certificate-detail',
                    kwargs={'certificate_id': certificate.certificate_id_four}
                )

        # Add next lesson URL if available
        next_lesson = lesson.get_next_lesson()
        if next_lesson:
            response_data['next_lesson_url'] = next_lesson.get_absolute_url()

        return JsonResponse(response_data)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Lesson already completed'
    })

def verify_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, certificate_id_four=certificate_id)
    return render(request, 'courses/verify_certificate.html', {
        'certificate': certificate
    })

@login_required
def register_for_webinar(request, webinar_id):
    webinar = get_object_or_404(Webinar, id=webinar_id)

    if webinar.registration_deadline < now():
        return JsonResponse({"error": "Registration closed"}, status=400)
    
    registration, created = WebinarRegistration.objects.get_or_create(user=request.user, webinar=webinar)

    if created:
        return JsonResponse({"message": "Registered successfully!"})
    return JsonResponse({"message": "Already registered."})