from django.views.generic import ListView
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from users.permissions import IsAdminOrTeacher
from .models import Lesson, Attendance
from .serializers import LessonSerializer, AttendanceSerializer

class LessonListView(ListView):
    model = Lesson
    template_name = 'Project/lessons.html'
    context_object_name = 'lessons'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset()


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.select_related(
        "teacher", "subject", "branch", "student", "group"
    ).all().order_by("date", "start_time")
    serializer_class = LessonSerializer
    permission_classes = [IsAdminOrTeacher]

    def perform_create(self, serializer):
        try:
            serializer.save()
        except DjangoValidationError as exc:
            raise ValidationError(exc.message_dict if hasattr(exc, "message_dict") else exc.messages)

    def perform_update(self, serializer):
        try:
            serializer.save()
        except DjangoValidationError as exc:
            raise ValidationError(exc.message_dict if hasattr(exc, "message_dict") else exc.messages)


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related("lesson", "student").all().order_by("id")
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminOrTeacher]

    def perform_create(self, serializer):
        try:
            serializer.save()
        except DjangoValidationError as exc:
            raise ValidationError(exc.message_dict if hasattr(exc, "message_dict") else exc.messages)
