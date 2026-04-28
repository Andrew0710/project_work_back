from django.db import models
from django.core.exceptions import ValidationError
from branches.models import Branch, Subject
from students.models import Student

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('individual', 'Individual'),
        ('group', 'Group'),
    ]
    name = models.CharField(max_length=255)
    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='subscription_plans')
    subjects = models.ManyToManyField(Subject, related_name='subscription_plans')
    pricing_grid = models.JSONField(help_text='Формат: {"8": 200, "12": 180} (кількість уроків -> ціна за урок)')

    def __str__(self):
        return f"{self.name} ({self.branch.name})"

class StudentSubscription(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='student_subscriptions')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    lessons_per_month = models.PositiveIntegerField()

    class Meta:
        unique_together = ("student", "subject")

    def clean(self):
        super().clean()
        if self.plan_id and self.subject_id:
            # Перевіряємо, чи дозволений цей предмет для даного плану
            if not self.plan.subjects.filter(id=self.subject.id).exists():
                raise ValidationError({"subject": "Цей предмет не входить у вибраний план підписки."})
        if self.plan_id and self.student_id and self.plan.branch_id != self.student.branch_id:
            raise ValidationError({"plan": "План і студент мають належати до однієї філії."})

    def __str__(self):
        return f"{self.student} - {self.plan.name} ({self.subject.name})"
