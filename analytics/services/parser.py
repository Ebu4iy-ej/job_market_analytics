import requests
from analytics.models import Vacancy, Skill

def fetch_and_save_vacancies(text="Python", pages=2):
    """Парсит вакансии через официальный API HeadHunter."""
    url = "https://api.hh.ru/vacancies"
    
    # HH строго валидирует формат User-Agent
    headers = {
        "User-Agent": "JobMarketAnalytics/1.0 (dev@jobmarket.local)",
        "HH-User-Agent": "JobMarketAnalytics/1.0 (dev@jobmarket.local)"
    }

    count = 0
    for page in range(pages):
        params = {
            "text": text,
            "page": page,        #Страницы от 0 до pages-1
            "per_page": 20,
            "search_field": "name" # Ищем только по названию профессии
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code != 200:
                print(f"[Ошибка {response.status_code}] Ответ сервера: {response.text}")
                continue

            data = response.json()
            items = data.get("items", [])
            print(f"Страница {page}: получено {len(items)} вакансий")

            for item in items:
                salary = item.get("salary") or {}
                salary_from = salary.get("from")
                salary_to = salary.get("to")
                
                if salary_from and salary_to:
                    salary_avg = (salary_from + salary_to) / 2
                else:
                    salary_avg = salary_from or salary_to

                vacancy, created = Vacancy.objects.update_or_create(
                    url=item.get("alternate_url"),
                    defaults={
                        "title": item.get("name"),
                        "company": item.get("employer", {}).get("name", "Не указана"),
                        "salary_from": salary_from,
                        "salary_to": salary_to,
                        "salary_avg": salary_avg,
                        "currency": salary.get("currency", "RUB") or "RUB",
                        "city": item.get("area", {}).get("name"),
                        "experience": item.get("experience", {}).get("name"),
                        "is_remote": item.get("schedule", {}).get("id") == "remote",
                        "published_at": item.get("published_at"),
                    }
                )

                snippet = item.get("snippet", {})
                requirement = (snippet.get("requirement") or "").lower()
                
                tech_stack = ["Python", "Django", "SQL", "PostgreSQL", "Docker", "Git", "Redis", "Celery", "REST API", "Pandas"]
                for tech in tech_stack:
                    if tech.lower() in requirement:
                        skill_obj, _ = Skill.objects.get_or_create(name=tech)
                        vacancy.skills.add(skill_obj)

                count += 1

        except Exception as e:
            print(f"[Исключение]: {e}")

    return count