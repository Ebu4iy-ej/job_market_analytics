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
    API эндпоинт для получения агрегированных данных для дашборда и графиков.
    """
    def get(self, request, *args, **kwargs):
        top_skills_qs = (
            Skill.objects.annotate(vacancy_count=Count('vacancies'))
            .order_by('-vacancy_count')[:10]
        )
        top_skills = [
            {"name": skill.name, "count": skill.vacancy_count}
            for skill in top_skills_qs
        ]

        experience_levels = (
            Vacancy.objects.values('experience_level')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        salary_by_skill = []
        for skill in top_skills_qs[:8]:
            avg_salary = Vacancy.objects.filter(
                skills=skill,
                currency='RUR'
            ).filter(
                Q(salary_from__isnull=False) | Q(salary_to__isnull=False)
            ).aggregate(
                avg_from=Avg('salary_from'),
                avg_to=Avg('salary_to')
            )
            
            avg_from = avg_salary['avg_from'] or 0
            avg_to = avg_salary['avg_to'] or 0
            
            if avg_from and avg_to:
                calculated_avg = (avg_from + avg_to) / 2
            else:
                calculated_avg = avg_from or avg_to

            if calculated_avg > 0:
                salary_by_skill.append({
                    "skill": skill.name,
                    "avg_salary": round(calculated_avg)
                })

        return Response({
            "top_skills": top_skills,
            "experience_levels": list(experience_levels),
            "salary_by_skill": salary_by_skill,
            "total_vacancies": Vacancy.objects.count()
        })
def dashboard_page_view(request):
    #отображает html страницу дашборда с графиками Chart.js.
    return render(request, "analytics/dashboard.html")