from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import CustomUser
from branches.models import Branch, Subject
from students.models import Student
from .models import SubscriptionPlan


class SubscriptionApiTests(APITestCase):
    def setUp(self):
        self.branch = Branch.objects.create(name="Central")
        self.other_branch = Branch.objects.create(name="West")
        self.subject = Subject.objects.create(name="Physics", branch=self.branch)
        self.other_subject = Subject.objects.create(name="Biology", branch=self.branch)
        self.student = Student.objects.create(first_name="A", last_name="B", branch=self.branch)
        self.admin = CustomUser.objects.create_user(
            phone="+380000000010",
            password="pass12345",
            first_name="Ad",
            last_name="Min",
            role="ADMIN",
        )
        self.teacher = CustomUser.objects.create_user(
            phone="+380000000011",
            password="pass12345",
            first_name="Te",
            last_name="Acher",
            role="TEACHER",
        )
        self.plan = SubscriptionPlan.objects.create(
            name="Plan A",
            plan_type="individual",
            branch=self.branch,
            pricing_grid={"8": 200},
        )
        self.plan.subjects.add(self.subject)

    def _auth(self, user):
        token_response = self.client.post(
            reverse("token_obtain_pair"),
            {"phone": user.phone, "password": "pass12345"},
            format="json",
        )
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}")

    def test_plan_subject_mismatch_rejected(self):
        self._auth(self.admin)
        response = self.client.post(
            reverse("student-subscriptions-list"),
            {
                "student": self.student.id,
                "plan": self.plan.id,
                "subject": self.other_subject.id,
                "lessons_per_month": 8,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("subject", response.data)

    def test_teacher_cannot_create_branch(self):
        self._auth(self.teacher)
        response = self.client.post(
            reverse("branches-list"),
            {"name": "Forbidden", "status": "active"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
