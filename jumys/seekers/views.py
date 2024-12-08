from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from .models import UserProfile, Application, Ability, WorkExperience
from .serializers import UserProfileSerializer, ApplicationSerializer, AbilitySerializer, WorkExperienceSerializer
from vacancies.models import Vacancy
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class UserAppliedVacanciesView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(user_profile=self.request.user.profile).select_related('vacancy')


class BookmarkVacancyView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, vacancy_id):
        user_profile = request.user.profile
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            return Response({'detail': 'Vacancy does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        user_profile.bookmarked_vacancies.add(vacancy)
        return Response({'detail': 'Vacancy bookmarked.'}, status=status.HTTP_200_OK)

    def delete(self, request, vacancy_id):
        user_profile = request.user.profile
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            return Response({'detail': 'Vacancy does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        user_profile.bookmarked_vacancies.remove(vacancy)
        return Response({'detail': 'Vacancy unbookmarked.'}, status=status.HTTP_200_OK)

class UserAbilitiesView(generics.ListCreateAPIView):
    serializer_class = AbilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.profile.abilities.all()

    def perform_create(self, serializer):
        serializer.save()


class RemoveAbilityView(generics.DestroyAPIView):
    serializer_class = AbilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        ability_id = self.kwargs['ability_id']
        return get_object_or_404(self.request.user.profile.abilities, id=ability_id)


class UserWorkExperienceView(generics.ListCreateAPIView):
    serializer_class = WorkExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkExperience.objects.filter(user_profile=self.request.user.profile)

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.profile)


class ManageWorkExperienceView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WorkExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkExperience.objects.filter(user_profile=self.request.user.profile)
