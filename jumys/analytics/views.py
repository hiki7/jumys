import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from django.db import models
from users.models import CustomUser
from seekers.models import Ability, Application
from vacancies.models import Vacancy
from companies.models import Company
from .models import UserActivity
from django.db.models.functions import TruncDate

def ensure_chart_dir():
    chart_dir = os.path.join(settings.MEDIA_ROOT, 'analytics_charts')
    os.makedirs(chart_dir, exist_ok=True)
    return chart_dir

def user_role_distribution(request):
    # Count users by role
    data = CustomUser.objects.values('role').annotate(count=Count('id'))
    roles = [d['role'] for d in data]
    counts = [d['count'] for d in data]

    # Plot bar chart
    plt.figure(figsize=(6,4))
    plt.bar(roles, counts, color='skyblue')
    plt.title('User Role Distribution')
    plt.xlabel('Role')
    plt.ylabel('Count')
    chart_dir = ensure_chart_dir()
    chart_path = os.path.join(chart_dir, 'user_role_distribution.png')
    plt.savefig(chart_path)
    plt.close()

    return render(request, 'analytics/user_role_distribution.html', {
        'chart_url': f"{settings.MEDIA_URL}analytics_charts/user_role_distribution.png"
    })

def user_login_activity(request):
    # Show login counts by day for the last 30 days
    now = timezone.now()
    start_date = now - timedelta(days=30)
    activities = UserActivity.objects.filter(login_time__gte=start_date)

    # Group by date
    daily_counts = (
        activities
        .annotate(date=models.functions.TruncDate('login_time'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    dates = [x['date'].strftime('%Y-%m-%d') for x in daily_counts]
    counts = [x['count'] for x in daily_counts]

    plt.figure(figsize=(10,5))
    plt.plot(dates, counts, marker='o', color='green')
    plt.title('User Logins in the Last 30 Days')
    plt.xlabel('Date')
    plt.ylabel('Number of Logins')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    chart_dir = ensure_chart_dir()
    chart_path = os.path.join(chart_dir, 'user_login_activity.png')
    plt.savefig(chart_path)
    plt.close()

    return render(request, 'analytics/user_login_activity.html', {
        'chart_url': f"{settings.MEDIA_URL}analytics_charts/user_login_activity.png"
    })

def applications_per_vacancy(request):
    # Count applications per vacancy
    data = (
        Application.objects
        .values('vacancy__position_name__name')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]  # top 10 vacancies
    )
    vacancies = [d['vacancy__position_name__name'] for d in data]
    counts = [d['count'] for d in data]

    plt.figure(figsize=(10,5))
    plt.barh(vacancies, counts, color='orange')
    plt.title('Top 10 Vacancies by Application Count')
    plt.xlabel('Applications')
    plt.ylabel('Vacancy')
    plt.tight_layout()
    chart_dir = ensure_chart_dir()
    chart_path = os.path.join(chart_dir, 'applications_per_vacancy.png')
    plt.savefig(chart_path)
    plt.close()

    return render(request, 'analytics/applications_per_vacancy.html', {
        'chart_url': f"{settings.MEDIA_URL}analytics_charts/applications_per_vacancy.png"
    })

def abilities_distribution(request):
    # Count how many users have each technology (Ability.technology)
    # Since abilities are many-to-many, we count distinct users per technology
    data = (
        Ability.objects
        .values('technology')
        .annotate(user_count=Count('users', distinct=True))
        .order_by('-user_count')[:10]
    )
    technologies = [d['technology'] for d in data]
    user_counts = [d['user_count'] for d in data]

    plt.figure(figsize=(10,5))
    plt.bar(technologies, user_counts, color='purple')
    plt.title('Top 10 Technologies by Number of Users with That Ability')
    plt.xlabel('Technology')
    plt.ylabel('Number of Users')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    chart_dir = ensure_chart_dir()
    chart_path = os.path.join(chart_dir, 'abilities_distribution.png')
    plt.savefig(chart_path)
    plt.close()

    return render(request, 'analytics/abilities_distribution.html', {
        'chart_url': f"{settings.MEDIA_URL}analytics_charts/abilities_distribution.png"
    })

def analytics_home(request):
    # A simple page with links to different analytics pages
    return render(request, 'analytics/analytics_home.html', {})


def vacancies_per_day(request):
    # Consider the last 30 days, or adjust as needed
    now = timezone.now()
    start_date = now - timedelta(days=30)

    data = (
        Vacancy.objects.filter(created_at__gte=start_date)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    dates = [d['date'].strftime('%Y-%m-%d') for d in data]
    counts = [d['count'] for d in data]

    # If there's no data (no vacancies), handle gracefully
    if not dates:
        dates = [start_date.strftime('%Y-%m-%d'), now.strftime('%Y-%m-%d')]
        counts = [0, 0]

    plt.figure(figsize=(10,5))
    plt.plot(dates, counts, marker='o', color='blue')
    plt.title('Vacancies Created Per Day (Last 30 Days)')
    plt.xlabel('Date')
    plt.ylabel('Number of Vacancies')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    chart_dir = ensure_chart_dir()
    chart_path = os.path.join(chart_dir, 'vacancies_per_day.png')
    plt.savefig(chart_path)
    plt.close()

    return render(request, 'analytics/vacancies_per_day.html', {
        'chart_url': f"{settings.MEDIA_URL}analytics_charts/vacancies_per_day.png"
    })