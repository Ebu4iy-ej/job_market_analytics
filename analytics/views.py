from django.db.models import Count
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

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