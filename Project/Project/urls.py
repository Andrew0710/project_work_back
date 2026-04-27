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

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", LoginView.as_view(), name='loginPage'),
    path("lessons/", LessonListView.as_view(), name='lesson-list'),
    path("", TemplateView.as_view(template_name='Project/home.html'), name='home'),
]
