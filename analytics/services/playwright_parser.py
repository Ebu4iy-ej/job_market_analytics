import asyncio
from playwright.async_api import async_playwright
from asgiref.sync import sync_to_async
from analytics.models import Vacancy, Skill


def detect_level(title: str) -> str:
    title_lower = title.lower()
    if 'junior' in title_lower or 'стажер' in title_lower or 'intern' in title_lower:
        return 'junior'
    elif 'senior' in title_lower or 'lead' in title_lower or 'ведущий' in title_lower:
        return 'senior'
    elif 'middle' in title_lower:
        return 'middle'
    return 'all'


@sync_to_async
def save_vacancy_to_db(title, company, url_link, full_text):
    level = detect_level(title)

    vacancy, _ = Vacancy.objects.update_or_create(
        url=url_link,
        defaults={
            "title": title,
            "company": company,
            "currency": "RUB",
            "experience_level": level,
        }
    )
    
    tech_stack = [
        "Python", "Django", "FastAPI", "Flask", "SQL", "PostgreSQL", 
        "Docker", "Git", "Redis", "Celery", "REST API", "Linux", 
        "Kubernetes", "MongoDB", "Asyncio", "RabbitMQ"
    ]
    
    for tech in tech_stack:
        if tech.lower() in full_text.lower():
            skill_obj, _ = Skill.objects.get_or_create(name=tech)
            vacancy.skills.add(skill_obj)


async def run_parser(search_query="Python", pages=2):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        for page_num in range(pages):
            search_url = f"https://hh.ru/search/vacancy?text={search_query}&page={page_num}"
            print(f"--- Загрузка страницы поисковой выдачи {page_num + 1} ---")
            
            try:
                await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_selector("a[data-qa='serp-item__title']", timeout=10000)
            except Exception as e:
                print(f"Ошибка при загрузке страницы выдачи {page_num + 1}: {e}")
                continue

            title_elements = await page.query_selector_all("a[data-qa='serp-item__title']")
            print(f"Найдено вакансий на странице: {len(title_elements)}")

            vacancies_to_process = []
            for elem in title_elements:
                title = await elem.inner_text()
                href = await elem.get_attribute("href")
                if href:
                    clean_url = href.split("?")[0]
                    vacancies_to_process.append((title, clean_url))

            for title, clean_url in vacancies_to_process:
                try:
                    print(f"Обработка вакансии: {title[:30]}...")
                    await page.goto(clean_url, wait_until="domcontentloaded", timeout=15000)
                    
                    body_element = await page.query_selector("body")
                    full_text = await body_element.inner_text() if body_element else ""

                    company_elem = await page.query_selector("a[data-qa='vacancy-company-name']")
                    company_name = await company_elem.inner_text() if company_elem else "Не указано"

                    await save_vacancy_to_db(title, company_name, clean_url, full_text)

                    await asyncio.sleep(1.5)

                except Exception as e:
                    print(f"Не удалось спарсить вакансию {clean_url}: {e}")
                    continue

        await browser.close()


def start_parsing(query="Python", pages=2):
    asyncio.run(run_parser(search_query=query, pages=pages))