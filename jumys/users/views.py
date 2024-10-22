from django.contrib import messages  # Correct import for messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from django.contrib.auth.views import LoginView, LogoutView

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

#  Function Based views

@login_required
def ViewUser(request):
    user = request.user  
    return render(request, 'auth/user_profile.html', {'user': user})

@login_required
def UpdateUser(request):
    user = request.user  
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('user_profile')  
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomUserChangeForm(instance=user)
    
    return render(request, 'auth/user_update.html', {'form': form})

@login_required
def DeleteUser(request):
    user = request.user  
    if request.method == 'POST':
        user.delete()
        logout(request)  
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('home')  
    return render(request, 'auth/user_delete.html')
