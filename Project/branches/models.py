from django.db import models
from django.conf import settings

class Branch(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='branches')
    def __str__(self):
        return f"{self.name} ({self.city})"

class Subject(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return f"{self.name} - {self.branch.name}"