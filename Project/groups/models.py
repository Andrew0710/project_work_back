from django.db import models
from branches.models import Branch
from students.models import Student

class Group(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(Student, related_name='groups')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='groups')

    def __str__(self):
        return self.name
