from django import template
from django.utils.timesince import timesince
from urllib.parse import urlparse, parse_qs
from ..models import CourseProgress

register = template.Library()

@register.filter
def progress_percentage(user, course):
    try:
        progress = CourseProgress.objects.get(user=user, course=course)
        return progress.progress
    except CourseProgress.DoesNotExist:
        return 0

@register.filter
def format_duration(duration):
    if not duration:
        return "No duration set"
    
    hours = duration.total_seconds() // 3600
    minutes = (duration.total_seconds() % 3600) // 60
    
    if hours > 0:
        return f"{int(hours)}h {int(minutes)}m"
    return f"{int(minutes)}m"

@register.inclusion_tag('courses/tags/progress_bar.html')
def show_progress(user, course):
    try:
        progress = CourseProgress.objects.get(user=user, course=course)
        return {
            'progress': progress.progress,
            'completed_lessons': progress.completed_lessons.count(),
            'total_lessons': course.total_lessons
        }
    except CourseProgress.DoesNotExist:
        return {
            'progress': 0,
            'completed_lessons': 0,
            'total_lessons': course.total_lessons
        }
    

# courses/templatetags/course_tags.py
@register.filter
def module_progress(module, user):
    """Calculate progress for a specific module"""
    try:
        progress = CourseProgress.objects.get(user=user, course=module.course)
        total_lessons = module.lessons.count()
        if total_lessons == 0:
            return 0
        completed_lessons = progress.completed_lessons.filter(module=module).count()
        return int((completed_lessons / total_lessons) * 100)
    except CourseProgress.DoesNotExist:
        return 0
    
@register.filter
def progress_color(progress):
    """Return Bootstrap color class based on progress percentage"""
    if progress >= 100:
        return 'success'
    elif progress >= 50:
        return 'primary'
    elif progress > 0:
        return 'warning'
    return 'secondary'

@register.filter(name='youtube_embed_url')
def youtube_embed_url(value):
    """
    Converts YouTube video URL to embed URL
    """
    if value:
        parsed_url = urlparse(value)
        if 'youtube.com' in parsed_url.netloc:
            # Get video ID from URL parameters
            video_id = parse_qs(parsed_url.query).get('v', [None])[0]
        elif 'youtu.be' in parsed_url.netloc:
            # Get video ID from URL path
            video_id = parsed_url.path[1:]
        else:
            return value

        if video_id:
            return f'https://www.youtube.com/embed/{video_id}'
    return value