from rest_framework import serializers
from .models import Lesson, Attendance


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

    def validate(self, attrs):
        teacher = attrs.get("teacher") or getattr(self.instance, "teacher", None)
        branch = attrs.get("branch") or getattr(self.instance, "branch", None)
        subject = attrs.get("subject") or getattr(self.instance, "subject", None)
        student = attrs.get("student") if "student" in attrs else getattr(self.instance, "student", None)
        group = attrs.get("group") if "group" in attrs else getattr(self.instance, "group", None)

        if teacher and teacher.role != "TEACHER":
            raise serializers.ValidationError({"teacher": "Selected user must have TEACHER role."})
        if subject and branch and subject.branch_id != branch.id:
            raise serializers.ValidationError({"subject": "Subject and lesson branch must match."})
        if student and branch and student.branch_id != branch.id:
            raise serializers.ValidationError({"student": "Student and lesson branch must match."})
        if group and branch and group.branch_id != branch.id:
            raise serializers.ValidationError({"group": "Group and lesson branch must match."})
        return attrs


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"
