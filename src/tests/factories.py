"""
Factory classes for creating test data.
"""

from typing import Any
from typing import Dict
from typing import Optional

import factory
from factory.django import DjangoModelFactory
from faker import Faker

from tasks.models import Task
from tasks.models import TaskStatusEnum
from tasks.models import TaskTypeEnum
from users.models import User

fake = Faker()


class UserFactory(DjangoModelFactory):
    """Factory for creating User instances for tests."""

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True

    @factory.post_generation
    def password(self, create: bool, extracted: Optional[str], **kwargs) -> None:
        password = extracted if extracted else "testpassword123"
        self.set_password(password)
        if create:
            self.save()


class TaskFactory(DjangoModelFactory):
    """Factory for creating Task instances for tests."""

    class Meta:
        model = Task

    user = factory.SubFactory(UserFactory)
    task_type = factory.Iterator([choice[0] for choice in TaskTypeEnum.choices])
    status = factory.Iterator([choice[0] for choice in TaskStatusEnum.choices])

    @factory.lazy_attribute
    def input_data(self) -> Dict[str, Any]:
        """Generate appropriate input data based on task_type."""
        if self.task_type == TaskTypeEnum.SUM:
            return {"num1": fake.pyint(1, 100), "num2": fake.pyint(1, 100)}
        elif self.task_type == TaskTypeEnum.COUNTDOWN:
            return {"seconds": fake.pyint(1, 60)}
        return {}

    @factory.lazy_attribute
    def result(self) -> Optional[Dict[str, Any]]:
        """Generate appropriate result data based on task_type and status."""
        if self.status in [TaskStatusEnum.COMPLETED]:
            if self.task_type == TaskTypeEnum.SUM:
                return {"result": self.input_data["num1"] + self.input_data["num2"]}
            elif self.task_type == TaskTypeEnum.COUNTDOWN:
                return {"message": f"Countdown of {self.input_data['seconds']} seconds completed"}
        elif self.status == TaskStatusEnum.ERROR:
            return {"error": "An error occurred during task execution"}
        return None
