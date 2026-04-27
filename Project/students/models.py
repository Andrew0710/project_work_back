from django.db import models
from branches.models import Branch

class Student(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    parent_info = models.TextField(blank=True, null=True, help_text="Ім'я, телефон, email, ким доводиться")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='students')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"