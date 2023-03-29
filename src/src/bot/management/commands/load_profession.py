from django.core.management import BaseCommand
from django.utils import timezone

from src.bot.core.parse_city import parse_cloth


class Command(BaseCommand):
    """Команда для запуска пулинга телеграм бота."""

    help = "Запуск парсинга exel файла"  # noqa

    def handle(self, *args, **options):
        """Запуск парсинга."""
        self.stdout.write("Начало загрузки csv файла:\n")
        start = timezone.now()
        parse_cloth()
        self.stdout.write(
            "Конец успешной загрузки: "
            f"{(timezone.now() - start).seconds / 60:.2f} мин"
        )
