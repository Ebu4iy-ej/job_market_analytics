from rest_framework import serializers
from .models import Skill, Vacancy, DailyAnalytics, UserProfile

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']


class VacancySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Vacancy
        fields = [
            'id', 'title', 'company', 'salary_from', 'salary_to', 
            'salary_avg', 'currency', 'experience', 'city', 
            'is_remote', 'url', 'skills', 'published_at', 'created_at'
        ]


class DailyAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyAnalytics
        fields = ['id', 'date', 'total_vacancies', 'median_salary', 'avg_salary', 'top_skills']


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'subscription', 'telegram_id']