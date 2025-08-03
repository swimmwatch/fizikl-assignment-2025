from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpRequest

UserModel = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(
        self,
        request: HttpRequest,
        email: str | None = None,
        password: str | None = None,
        **kwargs,
    ):
        if not email or not password:
            return None

        user = UserModel.objects.filter(Q(email__iexact=email) | Q(email__iexact=email)).first()
        if not user:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
