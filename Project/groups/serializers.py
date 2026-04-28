from rest_framework import serializers
from .models import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

    def validate(self, attrs):
        branch = attrs.get("branch") or getattr(self.instance, "branch", None)
        students = attrs.get("students")
        if branch and students is not None:
            invalid = [s.id for s in students if s.branch_id != branch.id]
            if invalid:
                raise serializers.ValidationError(
                    {"students": "All students in a group must belong to the same branch."}
                )
        return attrs
