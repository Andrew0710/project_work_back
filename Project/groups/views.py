from rest_framework import viewsets
from users.permissions import IsAdminOrReadOnly
from .models import Group
from .serializers import GroupSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.select_related("branch").prefetch_related("students").all().order_by("id")
    serializer_class = GroupSerializer
    permission_classes = [IsAdminOrReadOnly]
