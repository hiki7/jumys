from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from users.permissions import IsSeeker, IsAdmin, IsHR, IsAdminOrHR
from .models import Vacancy
from seekers.models import Application
from .serializers import VacancySerializer

class VacancyListCreateView(generics.ListCreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsAdminOrHR()]

class VacancyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsAdminOrHR()]


class ApplyToVacancyView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsSeeker]

    def post(self, request, vacancy_id):
        user = request.user
        user_profile = user.profile
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id, is_active=True)
        except Vacancy.DoesNotExist:
            return Response({'detail': 'Vacancy does not exist or is inactive.'}, status=status.HTTP_404_NOT_FOUND)

        if Application.objects.filter(user_profile=user_profile, vacancy=vacancy).exists():
            return Response({'detail': 'You have already applied to this vacancy.'}, status=status.HTTP_400_BAD_REQUEST)

        Application.objects.create(user_profile=user_profile, vacancy=vacancy)
        vacancy.applications.add(user)
        return Response({'detail': 'Application submitted successfully.'}, status=status.HTTP_200_OK)


class BookmarkVacancyView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsSeeker]

    def post(self, request, vacancy_id):
        user = request.user
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id, is_active=True)
        except Vacancy.DoesNotExist:
            return Response({'detail': 'Vacancy does not exist or is inactive.'}, status=status.HTTP_404_NOT_FOUND)

        if user in vacancy.bookmarked_by.all():
            return Response({'detail': 'Vacancy is already bookmarked.'}, status=status.HTTP_400_BAD_REQUEST)

        vacancy.bookmarked_by.add(user)
        return Response({'detail': 'Vacancy bookmarked successfully.'}, status=status.HTTP_200_OK)

    def delete(self, request, vacancy_id):
        user = request.user
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id, is_active=True)
        except Vacancy.DoesNotExist:
            return Response({'detail': 'Vacancy does not exist or is inactive.'}, status=status.HTTP_404_NOT_FOUND)

        if user not in vacancy.bookmarked_by.all():
            return Response({'detail': 'Vacancy is not bookmarked.'}, status=status.HTTP_400_BAD_REQUEST)

        vacancy.bookmarked_by.remove(user)
        return Response({'detail': 'Vacancy unbookmarked successfully.'}, status=status.HTTP_200_OK)
