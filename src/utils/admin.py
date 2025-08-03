from django.conf import settings
from django.contrib import admin
from django.db.models import Model
from django.db.models import QuerySet
from django.http import HttpRequest


class CannotDeleteModelAdminMixin:
    def has_delete_permission(
        self,
        request: HttpRequest,
        obj: Model | None = None,
    ) -> bool:
        return False


class CannotAddModelAdminMixin:
    def has_add_permission(
        self,
        request: HttpRequest,
        obj: Model | None = None,
    ) -> bool:
        return False


class CannotEditModelAdminMixin:
    def has_change_permission(
        self,
        request: HttpRequest,
        obj: Model | None = None,
    ) -> bool:
        return False


class ReadonlyModelAdminMixin(
    CannotDeleteModelAdminMixin,
    CannotAddModelAdminMixin,
    CannotEditModelAdminMixin,
):
    pass


class IsActiveFilter(admin.SimpleListFilter):
    title = "Активный?"
    parameter_name = "is_active"
    map_filter = {
        "Yes": True,
        "No": False,
    }

    def lookups(self, request: HttpRequest, model_admin: admin.ModelAdmin):
        return (
            ("Yes", "Да"),
            ("No", "Нет"),
        )

    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet:
        value = self.value()
        filtered = self.map_filter.get(value)
        base_qs = queryset
        if filtered is not None:
            base_qs = base_qs.filter(is_active=filtered)
        return base_qs


class CannotDeleteModelAdminDebugMixin:
    def has_delete_permission(
        self,
        request: HttpRequest,
        obj: Model | None = None,
    ) -> bool:
        return settings.DEBUG


class CannotAddModelAdminDebugMixin:
    def has_add_permission(
        self,
        request: HttpRequest,
        obj: Model | None = None,
    ) -> bool:
        return settings.DEBUG


class CannotEditModelAdminDebugMixin:
    def has_change_permission(
        self,
        request: HttpRequest,
        obj: Model | None = None,
    ) -> bool:
        return settings.DEBUG


class ReadonlyModelAdminDebugMixin(
    CannotDeleteModelAdminDebugMixin,
    CannotAddModelAdminDebugMixin,
    CannotEditModelAdminDebugMixin,
):
    pass
