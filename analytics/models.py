from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    """Навыки и технологии, извлекаемые из вакансий (Python, SQL, Docker и т.д.)"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Название навыка")

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    """Собранный датасет вакансий"""
    LEVEL_CHOICES = [
        ('junior', 'Junior'),
        ('middle', 'Middle'),
        ('senior', 'Senior'),
        ('all', 'All / Not specified'),
    ]

    title = models.CharField(max_length=255, verbose_name="Название должности")
    company = models.CharField(max_length=255, verbose_name="Компания")
    salary_from = models.IntegerField(null=True, blank=True, verbose_name="ЗП от")
    salary_to = models.IntegerField(null=True, blank=True, verbose_name="ЗП до")
    salary_avg = models.FloatField(null=True, blank=True, verbose_name="Средняя ЗП")
    currency = models.CharField(max_length=10, default="RUB", verbose_name="Валюта")

    experience = models.CharField(max_length=50, null=True, blank=True, verbose_name="Опыт работы")
    experience_level = models.CharField(
        max_length=10, choices=LEVEL_CHOICES, default='all', verbose_name="Грейд"
    )
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name="Город")
    is_remote = models.BooleanField(default=False, verbose_name="Удаленка")

    url = models.URLField(unique=True, verbose_name="Ссылка на вакансию")
    skills = models.ManyToManyField(Skill, blank=True, related_name="vacancies", verbose_name="Навыки")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата публикации")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата сбора")

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} в {self.company}"


class DailyAnalytics(models.Model):
    date = models.DateField(auto_now_add=True)
    top_skills = models.JSONField()
    vacancies_count = models.IntegerField()


class UserProfile(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    target_role = models.CharField(max_length=100, default='Python Developer')
    created_at = models.DateTimeField(auto_now_add=True)