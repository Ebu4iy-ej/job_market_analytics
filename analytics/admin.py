from django.contrib import admin
from .models import Skill, Vacancy, DailyAnalytics, UserProfile


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'experience_level', 'salary_avg', 'city', 'is_remote', 'created_at')
    list_filter = ('experience_level', 'is_remote', 'currency')
    search_fields = ('title', 'company')


@admin.register(DailyAnalytics)
class DailyAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'vacancies_count')
    list_filter = ('date',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'target_role', 'created_at')
    search_fields = ('telegram_id', 'target_role')