from django.db import models

# Create your models here.


# Create your models here.


class Profession(models.Model):
    """Профессия"""

    name = models.CharField(
        verbose_name="Название провессии",
        max_length=800,
    )

    class Meta:
        verbose_name = "Профессия"
        verbose_name_plural = "Профессии"


class Cloth(models.Model):
    """Класс для спец. одежды"""

    name = models.CharField(
        verbose_name="Наименование специальной одежды",
        max_length=255,
    )

    count = models.CharField(
        verbose_name="Норма выдачи на год",
        max_length=255,
    )

    profession = models.ForeignKey(
        Profession,
        on_delete=models.CASCADE,
        verbose_name="Профессия",
        related_name="cloth",
    )

    class Meta:
        verbose_name = "Спец. одежда"
        verbose_name_plural = "Спец. одежда"
