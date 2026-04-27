from django.contrib import admin
from .models import Lesson, Attendance

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('subject', 'date', 'start_time', 'end_time', 'status', 'teacher')
    list_filter = ('status', 'date')
    search_fields = ('subject__name',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'student', 'is_present')
    list_filter = ('is_present',)