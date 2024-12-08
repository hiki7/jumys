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

class ApplyToVacancyView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ApplicationSerializer

    def post(self, request, vacancy_id):
        user_profile = request.user.profile
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            return Response({'detail': 'Vacancy does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        if Application.objects.filter(user_profile=user_profile, vacancy=vacancy).exists():
            return Response({'detail': 'Already applied to this vacancy.'}, status=status.HTTP_400_BAD_REQUEST)
        application = Application.objects.create(user_profile=user_profile, vacancy=vacancy)
        serializer = self.get_serializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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


class WorkExperienceListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkExperience.objects.filter(user_profile=self.request.user.profile)

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.profile)
