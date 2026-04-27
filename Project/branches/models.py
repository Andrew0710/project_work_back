from django.db import models
from django.core.exceptions import ValidationError

class Branch(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def delete(self, *args, **kwargs):
        # Забороняємо видалення філії, якщо є студенти або розкладені уроки
        has_active_students = self.students.filter(status='active').exists()
        has_active_lessons = self.lessons.exclude(status='CANCELLED').exists()
        
        if has_active_students or has_active_lessons:
            raise ValidationError("Не можна видалити філію з активними студентами або уроками. Переведіть її у статус 'archived'.")
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name


class Subject(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='subjects')

    class Meta:
        unique_together = ('name', 'branch') # Назва предмету унікальна в межах філії

    def __str__(self):
        return f"{self.name} ({self.branch.name})"