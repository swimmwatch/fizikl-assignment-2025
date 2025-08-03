from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User
from utils.admin import CannotAddModelAdminMixin
from utils.admin import CannotDeleteModelAdminDebugMixin


@admin.register(User)
class UserAdmin(
    CannotAddModelAdminMixin,
    CannotDeleteModelAdminDebugMixin,
    UserAdmin,
):
    pass
