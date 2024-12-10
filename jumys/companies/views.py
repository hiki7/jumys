from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy

# Third-Party Imports
from rest_framework import generics, permissions, status
from rest_framework.response import Response

# Application-Specific Imports
from .models import Company
from .serializers import CompanySerializer
from .permissions import IsManagerOrAdmin
from .forms import CompanyForm
from .utils import get_location_from_nominatim  # Adjust the import path as needed
from companies.models import Location, Country, City, Street
from users.serializers import UserSerializer
from users.models import CustomUser

#renders

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



class AddManagerToCompanyView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, IsManagerOrAdmin]
    serializer_class = UserSerializer

    def post(self, request, company_id):
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({'detail': 'Company does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        if company.head_manager != request.user:
            return Response({'detail': 'You are not the head manager of this company.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.role = 'manager'
        user.save()
        company.managers.add(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

