from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from vacancies.models import Vacancy
from django.contrib.auth import get_user_model
from companies.models import Company
from .forms import CompanyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy


def home_view(request):
    # Example: show some vacancies
    vacancies = Vacancy.objects.filter(is_active=True)[:5]
    return render(request, 'home.html', {'title': 'Home', 'vacancies': vacancies})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html', {'title': 'Login'})

User = get_user_model()  # This now returns CustomUser

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # Get the selected role from the form

        if not username or not password or not role:
            messages.error(request, 'Please fill out all fields, including role.')
        else:
            if role not in ['seeker', 'hr']:
                messages.error(request, 'Invalid role selected.')
            else:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already taken.')
                else:
                    User.objects.create_user(username=username, password=password, role=role)
                    messages.success(request, 'Registered successfully!')
                    return redirect('login')
    # On GET or if validation failed, show the register page again
    return render(request, 'register.html', {'title': 'Register'})

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'title': 'Profile'})

@login_required
def post_view(request):
    # Handle a form for posting a new job listing or something else
    if request.method == 'POST':
        # process form
        messages.success(request, 'Post created!')
        return redirect('home')
    return render(request, 'post.html', {'title': 'Create Post'})

class CompanyCreateTemplateView(LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = "company_create.html"

    def form_valid(self, form):
        if self.request.user.role not in ['hr', 'admin']:
            return redirect('home')  # or show an error
        # Set head_manager to current user
        form.instance.head_manager = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')