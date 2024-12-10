from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile, Application, Ability, WorkExperience
from vacancies.models import Vacancy
from .forms import UserProfileForm, AbilityForm, WorkExperienceForm
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

# User Profile Detail View
class UserProfileDetailView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        profile = get_object_or_404(UserProfile, user_id=user_id)
        return render(request, 'seekers/profile.html', {'profile': profile})

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'seekers/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user.profile


# Applied Vacancies View
class UserAppliedVacanciesView(LoginRequiredMixin, View):
    def get(self, request):
        applications = Application.objects.filter(user_profile=request.user.profile).select_related('vacancy')
        context = {'applications': applications}
        return render(request, 'seekers/applied_vacancies.html', context)


class UserBookmarkedVacanciesView(LoginRequiredMixin, View):
    def get(self, request):
        bookmarked_vacancies = request.user.profile.bookmarked_vacancies.filter(is_active=True)
        context = {'bookmarked_vacancies': bookmarked_vacancies}
        return render(request, 'seekers/bookmarked_vacancies.html', context)

    def post(self, request, vacancy_id):
        vacancy = get_object_or_404(request.user.profile.bookmarked_vacancies, id=vacancy_id)
        request.user.profile.bookmarked_vacancies.remove(vacancy)
        return redirect('bookmarked_vacancies')


# Abilities Management
class UserAbilitiesView(LoginRequiredMixin, View):
    def get(self, request):
        abilities = request.user.profile.abilities.all()
        form = AbilityForm()
        context = {'abilities': abilities, 'form': form}
        return render(request, 'seekers/abilities.html', context)

    def post(self, request):
        form = AbilityForm(request.POST)
        if form.is_valid():
            ability = form.save()
            request.user.profile.abilities.add(ability)
            return redirect('abilities')
        abilities = request.user.profile.abilities.all()
        context = {'abilities': abilities, 'form': form}
        return render(request, 'seekers/abilities.html', context)


# Remove Ability
class RemoveAbilityView(LoginRequiredMixin, View):
    def post(self, request, ability_id):
        ability = get_object_or_404(request.user.profile.abilities, id=ability_id)
        request.user.profile.abilities.remove(ability)
        return redirect('abilities')


# Work Experience Management
class UserWorkExperienceView(LoginRequiredMixin, View):
    def get(self, request):
        work_experience = WorkExperience.objects.filter(user_profile=request.user.profile)
        form = WorkExperienceForm()
        context = {'work_experience': work_experience, 'form': form}
        return render(request, 'seekers/work_experience.html', context)

    def post(self, request):
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            work_experience = form.save(commit=False)
            work_experience.user_profile = request.user.profile
            work_experience.save()
            return redirect('work_experience')
        work_experience = WorkExperience.objects.filter(user_profile=request.user.profile)
        context = {'work_experience': work_experience, 'form': form}
        return render(request, 'seekers/work_experience.html', context)


# Remove Work Experience
class ManageWorkExperienceView(LoginRequiredMixin, View):
    def get(self, request, work_experience_id):
        work_experience = get_object_or_404(WorkExperience, id=work_experience_id, user_profile=request.user.profile)
        form = WorkExperienceForm(instance=work_experience)
        context = {'form': form}
        return render(request, 'seekers/manage_work_experience.html', context)

    def post(self, request, work_experience_id):
        work_experience = get_object_or_404(WorkExperience, id=work_experience_id, user_profile=request.user.profile)
        form = WorkExperienceForm(request.POST, instance=work_experience)
        if form.is_valid():
            form.save()
            return redirect('work_experience')
        context = {'form': form}
        return render(request, 'seekers/manage_work_experience.html', context)


class DeleteWorkExperienceView(LoginRequiredMixin, View):
    def post(self, request, work_experience_id):
        work_experience = get_object_or_404(WorkExperience, id=work_experience_id, user_profile=request.user.profile)
        work_experience.delete()
        return redirect('work_experience')