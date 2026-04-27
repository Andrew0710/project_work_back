from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

User = get_user_model()

def validate_login_data(phone, password):
    """ Business logic for validating login"""
    if not phone or not password:
        return False, "Всі поля обов'язкові"
    return True, ""

def process_login(request, phone, password):
    """
    Coordinates validation and authentication.
    Returns (True, None) on success.
    Returns (False, error_message) on failure.
    """
    is_valid, error_msg = validate_login_data(phone, password)
    if not is_valid:
        return False, error_msg # всі поля обов'язкові
    
    user = authenticate(request, phone=phone, password=password)
    if user and user.is_active:
        login(request, user)
        return True, None
        
    return False, "Неправильний номер або пароль"
