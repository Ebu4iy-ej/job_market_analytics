from celery import shared_task
from django.core.management import call_command


@shared_task
def run_scheduled_job_parser():
    """Фоновая задача для автоматического парсинга вакансий по расписанию."""
    print("--- Запуск фонового парсинга вакансий (Celery Task) ---")
    try:
        # Вызываем нашу custom management-команду parse_jobs
        call_command('parse_jobs', query='Python', pages=2)
        print("--- Фоновый парсинг успешно завершен ---")
        return "Parsing completed successfully"
    except Exception as e:
        print(f"--- Ошибка во время фонового парсинга: {e} ---")
        raise e