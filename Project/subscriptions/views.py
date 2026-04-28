from rest_framework import viewsets
from users.permissions import IsAdminOrReadOnly
from .models import SubscriptionPlan, StudentSubscription
from .serializers import SubscriptionPlanSerializer, StudentSubscriptionSerializer


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.select_related("branch").prefetch_related("subjects").all().order_by("id")
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAdminOrReadOnly]


class StudentSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = StudentSubscription.objects.select_related("student", "plan", "subject").all().order_by("id")
    serializer_class = StudentSubscriptionSerializer
    permission_classes = [IsAdminOrReadOnly]
