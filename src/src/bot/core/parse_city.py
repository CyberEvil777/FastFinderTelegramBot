import csv
from itertools import islice

from django.conf import settings
from django.db import transaction

from src.cloth.models import Cloth, Profession


def parse_cloth():
    """Фильтруем парсим и добавляем данные в бд"""
    professions = Profession.objects.all().values_list("name", flat=True)
    with open(settings.PATH_CLOTH, newline="") as csvfile:
        cloth_csv = csv.DictReader(csvfile)
        batch_size = 100
        clean_data = [
            row
            for row in cloth_csv
            if not row.get("Наименование профессии (должности") in professions
        ]

        profession_only = [
            row.get("Наименование профессии (должности") for row in clean_data
        ]

        unique_profession = set(profession_only)

        professions_generator = (
            Profession(
                name=row,
            )
            for row in unique_profession
        )

        with transaction.atomic():
            while True:
                batch = list(islice(professions_generator, batch_size))
                if not batch:
                    break
                Profession.objects.bulk_create(batch, batch_size)

        cloth_generator = (
            Cloth(
                name=row.get(
                    "Наименование специальной одежды, специальной обуви и других средств индивидуальной защиты"
                ),
                count=row.get("Норма выдачи на год (штуки, пары, комплекты)"),
                profession=Profession.objects.filter(
                    name=row.get("Наименование профессии (должности")
                ).first(),
            )
            for row in clean_data
        )

        with transaction.atomic():
            while True:
                batch = list(islice(cloth_generator, batch_size))
                if not batch:
                    break
                Cloth.objects.bulk_create(batch, batch_size)
