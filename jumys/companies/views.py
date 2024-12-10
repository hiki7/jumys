import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Company, Location, Country, City, Street
from .forms import CompanyForm, AddManagerForm
from .utils import get_location_from_nominatim
from users.models import CustomUser

logger = logging.getLogger('app_logger')

@method_decorator(login_required, name='dispatch')
class CreateCompanyHTMLView(View):
    def get(self, request):
        logger.debug('Rendering create company page')
        form = CompanyForm()
        return render(request, 'companies/create_company.html', {'form': form, 'title': 'Create Company'})

    def post(self, request):
        logger.info('Attempting to create a new company')
        form = CompanyForm(request.POST)
        if form.is_valid():
            try:
                country_name = form.cleaned_data['country_name']
                city_name = form.cleaned_data['city_name']
                street_name = form.cleaned_data.get('street_name', '')

                location_data = get_location_from_nominatim(country_name, city_name, street_name)
                if not location_data:
                    logger.warning('Could not determine location from provided data.')
                    form.add_error(None, "Could not determine location from provided data.")
                    return render(request, 'companies/create_company.html', {'form': form, 'title': 'Create Company'})

                validated_country = location_data['country']
                validated_city = location_data['city']
                validated_street = location_data.get('street', '')
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

                if not location:
                    location = Location.objects.create(
                        country=country,
                        city=city,
                        street=street,
                        latitude=latitude,
                        longitude=longitude
                    )
                else:
                    location.latitude = latitude
                    location.longitude = longitude
                    location.save()

                company = Company.objects.create(
                    name=form.cleaned_data['name'],
                    company_description=form.cleaned_data['company_description'],
                    location=location,
                    head_manager=request.user
                )

                logger.info(f'Successfully created company: {company.name} (ID: {company.pk})')
                messages.success(request, "Company created successfully!")
                return redirect('company_detail', pk=company.pk)
            except Exception as e:
                logger.error(f'Error creating company: {e}', exc_info=True)
                messages.error(request, "An error occurred while creating the company.")
        else:
            logger.warning('Company form validation failed')
        return render(request, 'companies/create_company.html', {'form': form, 'title': 'Create Company'})


class CompanyDetailView(DetailView):
    model = Company
    template_name = "companies/company_detail.html"
    context_object_name = 'company'

    def get(self, request, *args, **kwargs):
        logger.debug(f'Fetching company details for company ID: {self.kwargs.get("pk")}')
        return super().get(request, *args, **kwargs)


class EditCompanyView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'companies/edit_company.html'

    def test_func(self):
        logger.debug('Checking if user is authorized to edit this company')
        company = self.get_object()
        return self.request.user == company.head_manager or self.request.user.role == 'admin'

    def get_success_url(self):
        logger.info(f'Company updated successfully: {self.object.name} (ID: {self.object.pk})')
        messages.success(self.request, "Company updated successfully!")
        return reverse_lazy('company_detail', kwargs={'pk': self.object.pk})


class DeleteCompanyView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Company
    template_name = 'companies/delete_company_confirm.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        logger.debug('Checking if user is authorized to delete this company')
        company = self.get_object()
        return self.request.user.role == 'admin'

    def delete(self, request, *args, **kwargs):
        logger.info(f'Deleting company {self.get_object().name} (ID: {self.get_object().pk})')
        messages.success(request, "Company deleted successfully!")
        return super().delete(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class AddManagerView(View):
    def get(self, request, company_id):
        logger.debug(f'Rendering add manager page for company ID: {company_id}')
        form = AddManagerForm()
        return render(request, 'companies/add_manager.html', {'form': form, 'company_id': company_id})

    def post(self, request, company_id):
        logger.info(f'Attempting to add manager(s) to company ID: {company_id}')
        form = AddManagerForm(request.POST)
        if form.is_valid():
            try:
                managers = form.cleaned_data['user']
                company = get_object_or_404(Company, id=company_id)
                for manager in managers:
                    company.managers.add(manager)
                logger.info(f'Successfully added managers to company ID: {company_id}')
                messages.success(request, "Manager(s) added successfully!")
                return redirect('company_detail', pk=company_id)
            except Exception as e:
                logger.error(f'Error adding manager(s) to company ID: {company_id}: {e}', exc_info=True)
                messages.error(request, "An error occurred while adding managers.")
        else:
            logger.warning(f'Manager form validation failed for company ID: {company_id}')
        return render(request, 'companies/add_manager.html', {'form': form, 'company_id': company_id})
