# users/permissions.py

from rest_framework.permissions import BasePermission
from .models import CustomUser
from companies.models import Company
from vacancies.models import Vacancy

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsHR(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'hr'


class IsSeeker(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'seeker'


class IsAdminOrHR(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'hr']


class IsHeadManager(BasePermission):
    """
    Allows access only to the head manager of a company.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Vacancy):
            company = obj.company
        elif isinstance(obj, Company):
            company = obj
        else:
            return False
        return request.user == company.head_manager


class IsManagerOfCompany(BasePermission):
    """
    Allows access to managers assigned to a specific company.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Vacancy):
            company = obj.company
        elif isinstance(obj, Company):
            company = obj
        else:
            return False
        return company.managers.filter(id=request.user.id).exists()


class IsAdminOrCompanyManager(BasePermission):
    """
    Custom permission to allow admins or managers of the company to perform actions.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if isinstance(obj, Vacancy):
            company = obj.company
        elif isinstance(obj, Company):
            company = obj
        else:
            return False
        return company.managers.filter(id=request.user.id).exists() or request.user == company.head_manager
