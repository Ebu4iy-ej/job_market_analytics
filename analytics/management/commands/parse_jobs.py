from django.core.management.base import BaseCommand
from analytics.services.playwright_parser import start_parsing

class Command(BaseCommand):
    help = "Запускает парсинг вакансий с hh.ru"

    def add_arguments(self, parser):
        parser.add_argument("--query", type=str, default="Python", help="Поисковый запрос")
        parser.add_argument("--pages", type=int, default=3, help="Количество страниц")

    def handle(self, *args, **options):
        query = options["query"]
        pages = options["pages"]
        self.stdout.write(f"Запуск парсинга для '{query}' ({pages} стр.)...")
        start_parsing(query=query, pages=pages)
        self.stdout.write(self.style.SUCCESS("Парсинг успешно завершен!"))