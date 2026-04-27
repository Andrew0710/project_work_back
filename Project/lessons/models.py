from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from branches.models import Subject, Branch
from students.models import Student
from groups.models import Group

class Lesson(models.Model):
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='lessons')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name='lessons')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='lessons')

    # Якщо урок індивідуальний - заповнюється student, якщо груповий - group
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name='individual_lessons')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, related_name='group_lessons')

    def clean(self):
        super().clean()

        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("Час закінчення має бути пізніше за час початку.")

        # Перевірка: має бути вказана або група, або студент (але не обидва)
        if self.student and self.group:
            raise ValidationError("Урок не може бути одночасно індивідуальним і груповим.")
        if not self.student and not self.group:
            raise ValidationError("Необхідно вказати студента (для індив. уроку) або групу.")

        if hasattr(self, 'teacher') and self.teacher and self.teacher.role != 'TEACHER':
            raise ValidationError({"teacher": "Цей користувач не є вчителем."})

        # --- Логіка перевірки конфліктів (накладок) ---
        if self.date and self.start_time and self.end_time:
            overlapping_lessons = Lesson.objects.filter(
                date=self.date,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            ).exclude(pk=self.pk).exclude(status='CANCELLED')

            # 1. Перевірка накладок для вчителя
            if overlapping_lessons.filter(teacher=self.teacher).exists():
                raise ValidationError({"teacher": "У вчителя вже є урок на цей час."})

            # 2. Перевірка накладок для студентів
            if self.student: # Для індивідуального уроку
                # Перевіряємо чи є у цього студента індивідуальні уроки або групові уроки на цей час
                student_conflict = overlapping_lessons.filter(
                    models.Q(student=self.student) | models.Q(group__students=self.student)
                ).exists()
                if student_conflict:
                    raise ValidationError({"student": "У студента вже є інший урок на цей час."})
            
            if self.group and self.group.pk: # Для групового уроку
                # Отримуємо студентів групи і перевіряємо, чи немає в них накладок
                group_students = self.group.students.all()
                group_conflict = overlapping_lessons.filter(
                    models.Q(student__in=group_students) | models.Q(group__students__in=group_students)
                ).distinct().exists()
                if group_conflict:
                    raise ValidationError({"group": "Один або більше студентів з цієї групи мають інший урок у цей час."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject.name} - {self.date} {self.start_time.strftime('%H:%M')}"


class Attendance(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    is_present = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('lesson', 'student') # Один запис на студента для уроку

    def clean(self):
        super().clean()
        if hasattr(self, 'lesson') and self.lesson and hasattr(self, 'student') and self.student:
            # Не можна відмітити для скасованого уроку
            if self.lesson.status == 'CANCELLED':
                raise ValidationError("Не можна відмічати відвідуваність для скасованого уроку.")
            
            # Перевіряємо, чи є студент учасником цього уроку
            is_participant = False
            if self.lesson.student == self.student:
                is_participant = True
            elif self.lesson.group and self.lesson.group.students.filter(id=self.student.id).exists():
                is_participant = True
            
            if not is_participant:
                raise ValidationError("Цього студента немає в списках на цей урок.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        status = "Присутній" if self.is_present else "Відсутній"
        return f"{self.student} - {self.lesson.date} ({status})"