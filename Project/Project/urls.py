"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from users.views import LoginView
from lessons.views import LessonListView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from branches.views import BranchViewSet, SubjectViewSet
from groups.views import GroupViewSet
from students.views import StudentViewSet
from lessons.views import LessonViewSet, AttendanceViewSet
from subscriptions.views import SubscriptionPlanViewSet, StudentSubscriptionViewSet
from users.views import UserViewSet, PhoneTokenObtainPairView

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("branches", BranchViewSet, basename="branches")
router.register("subjects", SubjectViewSet, basename="subjects")
router.register("students", StudentViewSet, basename="students")
router.register("groups", GroupViewSet, basename="groups")
router.register("lessons", LessonViewSet, basename="lessons")
router.register("attendances", AttendanceViewSet, basename="attendances")
router.register("subscription-plans", SubscriptionPlanViewSet, basename="subscription-plans")
router.register("student-subscriptions", StudentSubscriptionViewSet, basename="student-subscriptions")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", LoginView.as_view(), name='loginPage'),
    path("lessons/", LessonListView.as_view(), name='lesson-list'),
    path("", TemplateView.as_view(template_name='Project/home.html'), name='home'),
    path("api/", include(router.urls)),
    path("api/auth/token/", PhoneTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
