from rest_framework import serializers
from .models import SubscriptionPlan, StudentSubscription


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = "__all__"


class StudentSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSubscription
        fields = "__all__"

    def validate(self, attrs):
        plan = attrs.get("plan") or getattr(self.instance, "plan", None)
        subject = attrs.get("subject") or getattr(self.instance, "subject", None)
        student = attrs.get("student") or getattr(self.instance, "student", None)

        if plan and subject and not plan.subjects.filter(id=subject.id).exists():
            raise serializers.ValidationError(
                {"subject": "Selected subject is not part of the plan."}
            )
        if plan and student and plan.branch_id != student.branch_id:
            raise serializers.ValidationError(
                {"plan": "Student and subscription plan must belong to the same branch."}
            )
        return attrs
