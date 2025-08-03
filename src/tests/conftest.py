"""
Celery test configurations to mock task execution in tests.
"""

from unittest.mock import patch

import pytest
from django.db import connections


@pytest.fixture(autouse=True)
def _celery_eager():
    """Configure Celery to execute tasks eagerly during tests."""
    from django.conf import settings

    # Store original settings
    original_always_eager = getattr(settings, "CELERY_TASK_ALWAYS_EAGER", False)
    original_eager_propagates = getattr(settings, "CELERY_TASK_EAGER_PROPAGATES", False)

    # Configure settings for testing
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True

    yield

    # Restore original settings
    settings.CELERY_TASK_ALWAYS_EAGER = original_always_eager
    settings.CELERY_TASK_EAGER_PROPAGATES = original_eager_propagates


@pytest.fixture(autouse=True)
def _db_cleanup(django_db_setup, django_db_blocker):
    """Reset database after each test to ensure no data persists between tests."""
    yield
    # Clean up all tables after each test
    with django_db_blocker.unblock():
        for connection in connections.all():
            with connection.cursor() as cursor:
                tables = connection.introspection.table_names()
                for table in tables:
                    if table not in ["django_migrations", "django_content_type"]:
                        cursor.execute(f'TRUNCATE TABLE "{table}" CASCADE;')


@pytest.fixture
def mock_celery_tasks():
    """Mock all Celery tasks to avoid actual execution."""
    with patch("tasks.tasks.sum_two_numbers.delay") as mock_sum, patch("tasks.tasks.countdown.delay") as mock_countdown:
        yield {"sum_two_numbers": mock_sum, "countdown": mock_countdown}
