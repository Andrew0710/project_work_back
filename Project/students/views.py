from rest_framework import viewsets
from users.permissions import IsAdminOrReadOnly
from .models import Student
from .serializers import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related("branch").all().order_by("id")
    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrReadOnly]
