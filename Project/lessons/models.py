from django.db import models
from django.conf import settings
from branches.models import Subject
from groups.models import Group



class LessonManager(models.Manager):
    def check_conflicts(self, teacher, students, date , start_time,end_time,exclude_lesson = None):
        conflicts = []
        teacher_conflicts = self.filter(teacher=teacher, date=date).exclude(id=exclude_lesson.id if exclude_lesson else None)
        for lesson in teacher_conflicts:
            if (start_time < lesson.end_time and end_time > lesson.start_time):
                conflicts.append(f"Teacher {teacher} has a conflict with lesson {lesson}.")

        for student in students:
            student_conflicts = self.filter(student__user=student.user, date=date).exclude(id=exclude_lesson.id if exclude_lesson else None)
            for lesson in student_conflicts:
                if (start_time < lesson.end_time and end_time > lesson.start_time):
                    conflicts.append(f"Student {student} has a conflict with lesson {lesson}.")

        return conflicts


class Lesson(models.Model):
    LESSON_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('group', 'Group'),
    ]
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE_CHOICES, default='individual')
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    lesson_status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='scheduled')
    

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lessons')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lessons', limit_choices_to={'role': 'teacher'})
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, null=True, blank=True, related_name='individual_lessons')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, related_name='lessons')

    objects = LessonManager()

    def __str__(self):
        return f"{self.subject} - {self.date}"
    











    # @property
    # def participants(self):
    #     if self.lesson_type == 'individual' and self.student:
    #         return [self.student]
    #     elif self.lesson_type == 'group' and self.group:
    #         return list(self.group.members.all())
    #     return []

    # def clean(self):
    #     from django.core.exceptions import ValidationError
    #     if self.lesson_type == 'individual':
    #         if not self.student:
    #             raise ValidationError("Individual lessons must have a student assigned.")
    #         if self.group:
    #             raise ValidationError("Individual lessons cannot have a group assigned.")
    #     elif self.lesson_type == 'group':
    #         if not self.group:
    #             raise ValidationError("Group lessons must have a group assigned.")
    #         if self.student:
    #             raise ValidationError("Group lessons cannot have a student assigned.")

    # def save(self, *args, **kwargs):
    #     self.clean()
    #     # Check conflicts before saving
    #     participants = self.participants
    #     conflict = self.objects.check_conflicts(self.teacher, participants, self.date, self.start_time, self.end_time, exclude_lesson=self if self.pk else None)
    #     if conflict:
    #         from django.core.exceptions import ValidationError
    #         raise ValidationError(conflict)
    #     super().save(*args, **kwargs)