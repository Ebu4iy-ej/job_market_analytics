# IT Job Market Analytics Platform

Платформа для сбора и интерактивной аналитики рынка IT-вакансий. Проект автоматически парсит данные с HeadHunter, агрегирует ключевые навыки, уровень опыта и вилки зарплат, предоставляя удобный дашборд с фильтрацией в реальном времени.

## Основной функционал

- **Парсинг вакансий (Playwright & Chromium):** Асинхронный сбор вакансий с HeadHunter с извлечением стека технологий, опыта, компании и вилки зарплаты.
- **Интерактивный дашборд (Chart.js & Bootstrap 5):**
  - Столбчатая диаграмма топовых ключевых навыков.
  - Круговая диаграмма распределения вакансий по уровню опыта (Junior, Middle, Senior).
  - Карточки с метриками (общее количество вакансий, средняя зарплата).
- **Динамическая фильтрация:** Поиск по должности и фильтрация по опыту работы без перезагрузки страницы (асинхронные запросы via Fetch API).
- **Список вакансий с пагинацией:** Табличный вывод со ссылками на первоисточник и разбиением по страницам (Django REST Framework Pagination).
- **Фоновые задачи (Celery & Redis):** Возможность периодического автообновления базы вакансий.

## Технологический стек

- **Backend:** Python 3.12+, Django 5+, Django REST Framework (DRF)
- **Scraping / Automation:** Crawlee, Playwright, Chromium
- **Frontend:** HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, Chart.js
- **Database:** PostgreSQL / SQLite
- **Async & Scheduling:** Celery, Redis, django-celery-beat

## Структура проекта

```text
job_market_analytics/
├── analytics/
│   ├── templates/analytics/
│   │   └── dashboard.html    # Фронтенд дашборда (Chart.js & Bootstrap)
│   ├── models.py             # Модели Vacancy, Skill, DailyAnalytics
│   ├── serializers.py        # Сериализаторы DRF
│   ├── views.py              # API views & Dashboard views
│   └── urls.py               # Роутинг API и дашборда
├── config/                   # Настройки Django, Celery и DRF
├── scraper/                  # Модуль парсинга данных с HH.ru
└── manage.py
```

## Установка и запуск

1. **Клонируйте репозиторий:**
   ```bash
   git clone [https://github.com/your-username/job_market_analytics.git](https://github.com/your-username/job_market_analytics.git)
   cd job_market_analytics
   ```

2. **Создайте и активируйте виртуальное окружение:**
   ```bash
   python -m venv venv
   ```
   
   * Для Windows:
     ```bash
     venv\Scripts\activate
     ```
   * Для Linux/macOS:
     ```bash
     source venv/bin/activate
     ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

4. **Примените миграции:**
   ```bash
   python manage.py migrate
   ```

5. **Запустите сервер разработки:**
   ```bash
   python manage.py runserver
   ```

6. **Откройте в браузере:** `http://127.0.0.1:8000/dashboard/`