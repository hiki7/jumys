from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from vacancies.models import Vacancy
from core.forms import CompanyForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views import View
from companies.models import Company, Country, City, Location, Street
from core.utils import get_location_from_nominatim
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()  # CustomUser model

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

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # Get role from form

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

    return render(request, 'register.html', {'title': 'Register'})

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'title': 'Profile'})

@login_required
def post_view(request):
    # Example form handling for a new job post
    if request.method == 'POST':
        # Process form
        messages.success(request, 'Post created!')
        return redirect('home')
    return render(request, 'post.html', {'title': 'Create Post'})


@method_decorator(login_required, name='dispatch')
class CreateCompanyHTMLView(View):
    def get(self, request):
        form = CompanyForm()
        return render(request, 'create_company.html', {'form': form, 'title': 'Create Company'})

    def post(self, request):
        form = CompanyForm(request.POST)
        if form.is_valid():
            country_name = form.cleaned_data['country_name']
            city_name = form.cleaned_data['city_name']
            street_name = form.cleaned_data.get('street_name', '')

            location_data = get_location_from_nominatim(country_name, city_name, street_name)
            if not location_data:
                form.add_error(None, "Could not determine location from provided data.")
                return render(request, 'create_company.html', {'form': form, 'title': 'Create Company'})

            validated_country = location_data['country']
            validated_city = location_data['city']
            validated_street = location_data['street']
            latitude = location_data['latitude']
            longitude = location_data['longitude']

            country, _ = Country.objects.get_or_create(name=validated_country)
            city, _ = City.objects.get_or_create(name=validated_city, country=country)
            street = None
            if validated_street:
                street, _ = Street.objects.get_or_create(name=validated_street)

            location, created = Location.objects.get_or_create(
                country=country,
                city=city,
                street=street,
                defaults={'latitude': latitude, 'longitude': longitude}
            )
            if not created:
                location.latitude = latitude
                location.longitude = longitude
                location.save()

            company = Company.objects.create(
                name=form.cleaned_data['name'],
                company_description=form.cleaned_data['company_description'],
                location=location,
                head_manager=request.user
            )

            messages.success(request, "Company created successfully!")
            return redirect('company_detail', pk=company.pk)

        return render(request, 'create_company.html', {'form': form, 'title': 'Create Company'})


class CompanyDetailView(DetailView):
    model = Company
    template_name = "company_detail.html"
    context_object_name = 'company'


class EditCompanyView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'edit_company.html'
    
    def test_func(self):
        company = self.get_object()
        return self.request.user == company.head_manager or self.request.user.role == 'admin'
    
    def get_success_url(self):
        messages.success(self.request, "Company updated successfully!")
        return reverse_lazy('company_detail', kwargs={'pk': self.object.pk})

class DeleteCompanyView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Company
    template_name = 'delete_company_confirm.html'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        company = self.get_object()
        return self.request.user.role == 'admin'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Company deleted successfully!")
        return super().delete(request, *args, **kwargs)