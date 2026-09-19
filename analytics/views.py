from django.db.models import Count, Avg, Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render

from .models import DailyAnalytics, Skill, UserProfile, Vacancy
from .serializers import (
    DailyAnalyticsSerializer,
    SkillSerializer,
    UserProfileSerializer,
    VacancySerializer,
)


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class VacancyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer


class DailyAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DailyAnalytics.objects.all()
    serializer_class = DailyAnalyticsSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class TopSkillsView(APIView):
    def get(self, request):
        level = request.query_params.get('level', None)

        vacancies_qs = Vacancy.objects.all()
        if level in ['junior', 'middle', 'senior']:
            vacancies_qs = vacancies_qs.filter(experience_level=level)

        skills = Skill.objects.filter(vacancies__in=vacancies_qs)
        top_skills = (
            skills.annotate(vacancies_count=Count('vacancies'))
            .order_by('-vacancies_count')[:10]
            .values('name', 'vacancies_count')
        )

        return Response({
            'selected_level': level or 'all',
            'total_vacancies': vacancies_qs.count(),
            'top_skills': top_skills
        })

class DashboardAnalyticsAPIView(APIView):
    """
    API эндпоинт для получения агрегированных данных с поддержкой фильтрации.
    """
    def get(self, request, *args, **kwargs):
        # 1. Получаем параметры фильтрации из URL (исправлено имя переменной)
        experience_filter = request.GET.get('experience', None)
        search_query = request.GET.get('search', None)

        # 2. Базовый QuerySet вакансий
        vacancies = Vacancy.objects.all()

        # 3. Применяем фильтры
        if experience_filter:
            vacancies = vacancies.filter(experience_level__icontains=experience_filter)
        
        if search_query:
            vacancies = vacancies.filter(title__icontains=search_query)

        # 4. Агрегируем топ-навыки по отфильтрованным вакансиям
        top_skills_qs = (
            Skill.objects.filter(vacancies__in=vacancies)
            .annotate(vacancy_count=Count('vacancies'))
            .order_by('-vacancy_count')[:10]
        )
        
        # Исправлено: skill.vacancy_count (в единственном числе)
        top_skills = [
            {"name": skill.name, "count": skill.vacancy_count}
            for skill in top_skills_qs
        ]

        # 5. Группировка по опыту
        experience_levels = (
            vacancies.values('experience_level')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        return Response({
            "top_skills": top_skills,
            "experience_levels": list(experience_levels),
            "total_vacancies": vacancies.count()
        })
    
def dashboard_page_view(request):
    #отображает html страницу дашборда с графиками Chart.js.
    return render(request, "analytics/dashboard.html")