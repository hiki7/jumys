from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from django.contrib.auth.views import LoginView,LogoutView

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  
        return redirect('home')

    def form_invalid(self, form):
        print(form.errors)  
        return super().form_invalid(form)
    
class CustomLoginView(LoginView):
    template_name = 'auth/login.html'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return self.success_url or reverse_lazy('home')
    
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home') 
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'registration/profile_update.html'
    
    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'pk': self.request.user.pk})  # Redirect to profile detail after update

    def get_object(self):
        return self.request.user  

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    success_url = reverse_lazy('login')

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        # Get the user object
        user = self.get_object()

        user.profile.delete()  
 
        user.delete()
        return redirect(self.success_url)