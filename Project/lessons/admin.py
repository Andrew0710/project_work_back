from django.contrib import admin
from .models import Lesson
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('subject', 'description', 'start_time', 'end_time', 'lesson_status', 'teacher')
    list_filter = ('lesson_status',)
    search_fields = ('subject', 'description')