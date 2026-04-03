from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from django.contrib.auth import login
from .serializers import LoginSerializer

class LoginAPIView(APIView):
    # ДОДАНО: Дозволяємо доступ всім, навіть неавторизованим (бо це ж логін)
    permission_classes = [permissions.AllowAny] 

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user) # Авторизація через сесію
        return Response({"message": "Успішний вхід!"}, status=status.HTTP_200_OK)