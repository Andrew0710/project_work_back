from rest_framework import viewsets
from users.permissions import IsAdminOrReadOnly
from .models import Branch, Subject
from .serializers import BranchSerializer, SubjectSerializer


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all().order_by("id")
    serializer_class = BranchSerializer
    permission_classes = [IsAdminOrReadOnly]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.select_related("branch").all().order_by("id")
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminOrReadOnly]
