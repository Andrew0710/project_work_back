from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from branches.models import Branch
from students.models import Student

class Group(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='groups')
    students = models.ManyToManyField(Student, related_name='student_groups')

    class Meta:
        unique_together = ("name", "branch")

    def __str__(self):
        return f"{self.name} ({self.branch.name})"

# Сигнал для перевірки, що студенти належать до тієї ж філії, що і група
@receiver(m2m_changed, sender=Group.students.through)
def validate_group_students_branch(sender, instance, action, pk_set, **kwargs):
    if action == "pre_add":
        invalid_students = Student.objects.filter(pk__in=pk_set).exclude(branch=instance.branch)
        if invalid_students.exists():
            raise ValidationError("Не можна додати до групи студентів з іншої філії.")
