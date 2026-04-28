from datetime import date, time
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import CustomUser
from branches.models import Branch, Subject
from students.models import Student
from .models import Lesson


class LessonApiTests(APITestCase):
    def setUp(self):
        self.branch = Branch.objects.create(name="Main")
        self.subject = Subject.objects.create(name="Math", branch=self.branch)
        self.teacher = CustomUser.objects.create_user(
            phone="+380000000001",
            password="pass12345",
            first_name="Teach",
            last_name="Er",
            role="TEACHER",
        )
        self.student = Student.objects.create(
            first_name="Stud",
            last_name="Ent",
            branch=self.branch,
        )

    def _auth(self, user, password="pass12345"):
        token_response = self.client.post(
            reverse("token_obtain_pair"),
            {"phone": user.phone, "password": password},
            format="json",
        )
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}")

    def test_teacher_conflict_detection(self):
        self._auth(self.teacher)
        Lesson.objects.create(
            date=date(2026, 4, 28),
            start_time=time(10, 0),
            end_time=time(11, 0),
            teacher=self.teacher,
            subject=self.subject,
            branch=self.branch,
            student=self.student,
        )

        response = self.client.post(
            reverse("lessons-list"),
            {
                "date": "2026-04-28",
                "start_time": "10:30:00",
                "end_time": "11:30:00",
                "teacher": self.teacher.id,
                "subject": self.subject.id,
                "branch": self.branch.id,
                "student": self.student.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("teacher", response.data)

    def test_teacher_can_create_lesson(self):
        self._auth(self.teacher)
        response = self.client.post(
            reverse("lessons-list"),
            {
                "date": "2026-05-01",
                "start_time": "12:00:00",
                "end_time": "13:00:00",
                "teacher": self.teacher.id,
                "subject": self.subject.id,
                "branch": self.branch.id,
                "student": self.student.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
