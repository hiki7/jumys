from django.shortcuts import render, redirect
from django.views.generic import CreateView,UpdateView,DeleteView,ListView
from .models import UserProfile,Ability,Application,WorkExperience
from django.urls import reverse_lazy

class UserProfileCreateView(CreateView):
    model = UserProfile
    fields = ['phone', 'links', 'resume', 'abilities']  # Fields to be filled by user
    template_name = 'userprofile_form.html'
    success_url = reverse_lazy('userprofile_detail')  # Redirect after successful creation

    def form_valid(self, form):
        form.instance.user = self.request.user  # Bind profile to logged-in user
        return super().form_valid(form)


class UserProfileUpdateView(UpdateView):
    model = UserProfile
    fields = ['phone', 'links', 'resume', 'abilities']  # Fields that can be updated
    template_name = 'userprofile_form.html'
    success_url = reverse_lazy('userprofile_detail')

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)  # Get the current user's profile


def remove_ability(request, ability_id):
    user_profile = request.user.profile  # Get the user's profile
    ability = Ability.objects.get(id=ability_id)
    user_profile.abilities.remove(ability)  # Remove the ability
    return redirect('userprofile_detail')



def remove_ability(request, ability_id):
    user_profile = request.user.profile  # Get the user's profile
    ability = Ability.objects.get(id=ability_id)
    user_profile.abilities.remove(ability)  # Remove the ability
    return redirect('userprofile_detail')



class AbilityCreateView(CreateView):
    model = Ability
    fields = ['technology', 'experience_years', 'proficiency_level']
    template_name = 'ability_form.html'
    success_url = reverse_lazy('userprofile_detail')

    def form_valid(self, form):
        ability = form.save()  # Save the new ability
        user_profile = self.request.user.profile
        user_profile.abilities.add(ability)  # Add the ability to the user's profile
        return super().form_valid(form)



class WorkExperienceCreateView(CreateView):
    model = WorkExperience
    fields = ['company', 'position', 'start_date', 'end_date', 'description', 'abilities']
    template_name = 'workexperience_form.html'
    success_url = reverse_lazy('userprofile_detail')

    def form_valid(self, form):
        form.instance.user_profile = self.request.user.profile  # Link to user profile
        return super().form_valid(form)



class WorkExperienceUpdateView(UpdateView):
    model = WorkExperience
    fields = ['company', 'position', 'start_date', 'end_date', 'description', 'abilities']
    template_name = 'workexperience_form.html'
    success_url = reverse_lazy('userprofile_detail')

    def get_object(self, queryset=None):
        return WorkExperience.objects.get(id=self.kwargs['pk'], user_profile=self.request.user.profile)


class WorkExperienceDeleteView(DeleteView):
    model = WorkExperience
    template_name = 'workexperience_confirm_delete.html'
    success_url = reverse_lazy('userprofile_detail')

    def get_object(self, queryset=None):
        return WorkExperience.objects.get(id=self.kwargs['pk'], user_profile=self.request.user.profile)


class ApplicationListView(ListView):
    model = Application
    template_name = 'application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.filter(user_profile=self.request.user.profile)

class ApplicationDeleteView(DeleteView):
    model = Application
    template_name = 'application_confirm_delete.html'
    success_url = reverse_lazy('application_list')

    def get_object(self, queryset=None):
        return Application.objects.get(id=self.kwargs['pk'], user_profile=self.request.user.profile)
