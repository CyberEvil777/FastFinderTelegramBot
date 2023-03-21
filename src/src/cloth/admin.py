from django.contrib import admin
from django.contrib.auth.models import Group, User

from src.cloth.models import Cloth, Profession


class ClothInline(admin.TabularInline):
    model = Cloth


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    """Админка для модели Profession"""

    list_display = ("name",)

    inlines = [
        ClothInline,
    ]

    fieldsets = (
        (
            None,
            {"fields": ("name",)},
        ),
    )


admin.site.unregister(Group)
admin.site.unregister(User)
