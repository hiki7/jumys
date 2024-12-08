from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

import users.permissions
from .models import Vacancy
from .serializers import VacancySerializer

class VacancyListCreateView(generics.ListCreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class VacancyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ApplyToVacancyView(APIView):
    permission_classes = [permissions.IsAuthenticated, users.permissions.IsSeeker]

    def post(self, request, vacancy_id):
        user = request.user
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id, is_active=True)
        except Vacancy.DoesNotExist:
            return Response({'detail': 'Vacancy does not exist or is inactive.'}, status=status.HTTP_404_NOT_FOUND)

        if user in vacancy.applications.all():
            return Response({'detail': 'You have already applied to this vacancy.'}, status=status.HTTP_400_BAD_REQUEST)

        vacancy.applications.add(user)
        return Response({'detail': 'Application submitted successfully.'}, status=status.HTTP_200_OK)


class BookmarkVacancyView(APIView):
    permission_classes = [permissions.IsAuthenticated, users.permissions.IsSeeker]

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
