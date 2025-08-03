import json
from typing import Any
from typing import Dict

import structlog
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Task
from .models import TaskTypeEnum

logger = structlog.get_logger(__name__)
User = get_user_model()


class SumTaskSerializer(serializers.Serializer):
    num1 = serializers.IntegerField()
    num2 = serializers.IntegerField()


class CountdownTaskSerializer(serializers.Serializer):
    seconds = serializers.IntegerField(
        min_value=0,
        help_text="Number of seconds for the countdown. Must be a positive integer.",
    )


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    task_type_display = serializers.CharField(
        source="get_task_type_display",
        read_only=True,
    )
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model = Task
        fields = (
            "id",
            "user",
            "task_type",
            "task_type_display",
            "input_data",
            "status",
            "status_display",
            "result",
            "created_at",
        )
        read_only_fields = (
            "user",
            "status",
            "result",
            "created_at",
        )

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        task_serializer_map = {
            TaskTypeEnum.SUM: SumTaskSerializer,
            TaskTypeEnum.COUNTDOWN: CountdownTaskSerializer,
        }

        # Validate input data based on task type
        task_type = data.get("task_type")
        input_data = data.get("input_data", "{}")  # noqa: P103

        try:
            input_data = json.loads(input_data)
        except json.decoder.JSONDecodeError:
            raise serializers.ValidationError("Input data must be a valid JSON object")

        task_serializer = task_serializer_map[task_type]
        task_data = task_serializer(data=input_data)
        if not task_data.is_valid():
            raise serializers.ValidationError(task_data.errors)

        return data
