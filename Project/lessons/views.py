from django.shortcuts import render
from django.views.generic import ListView
from .models import Lesson

class LessonListView(ListView):
    model = Lesson
    template_name = 'Project/lessons.html'
    context_object_name = 'lessons'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        lesson_type = self.request.GET.get('lesson_type')
        if lesson_type in ['individual', 'group']:
            queryset = queryset.filter(lesson_type=lesson_type)
        return queryset
