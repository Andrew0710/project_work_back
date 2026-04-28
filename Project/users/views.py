from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .services import process_login
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from .serializers import UserSerializer, PhoneTokenObtainPairSerializer
from .permissions import IsAdminOrReadOnly

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'Project/loginPage.html')

    def post(self, request):
        phone = request.POST.get('phone')
        password = request.POST.get('password')
    
        success, error_message = process_login(request, phone, password)
        if success:
            return redirect('home')
        
        messages.error(request, error_message)
        return redirect('loginPage')


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]


class PhoneTokenObtainPairView(TokenObtainPairView):
    serializer_class = PhoneTokenObtainPairSerializer