from django.db import models
from django.conf import settings
from branches.models import Branch, Subject
from students.models import Student
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255)
    PLAN_CHOICES = [
        ('group', 'Групові заняття'),
        ('individual', 'Індивідуальні заняття'),
    ]
    plan_type = models.CharField(max_length=255, choices=PLAN_CHOICES)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='plans')
    def __str__(self):
        return f"{self.name} — {self.branch.name} ({self.get_plan_type_display()})"

class StudentSubscription(models.Model):
    start_date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subscriptions')
    subscription = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='student_subscriptions')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_subscriptions')
    def __str__(self):
        return f"{self.student} — {self.subscription.name} ({self.subject.name})"
    
