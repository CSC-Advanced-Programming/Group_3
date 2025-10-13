"""Facility views implementation."""
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import ProtectedError
from ...models import Facility
from ...utils import SearchFilterMixin, get_model_field_choices


class FacilityListView(SearchFilterMixin, ListView):
    model = Facility
    template_name = "core/facility_list.html"
    context_object_name = "facilities"
    
    # Search configuration
    search_fields = ['name', 'location', 'description', 'facility_id']
    
    # Filter configuration
    filter_fields = {
        'partner_organization': [],
        'facility_type': [],
        'capabilities': [],
    }
    
    items_per_page = 15
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Populate filter choices dynamically
        self.filter_fields['partner_organization'] = get_model_field_choices(Facility, 'partner_organization')
        self.filter_fields['facility_type'] = get_model_field_choices(Facility, 'facility_type')
        self.filter_fields['capabilities'] = get_model_field_choices(Facility, 'capabilities')
    
    def get_queryset(self):
        """Apply search and filters to the queryset."""
        queryset = Facility.objects.all()
        
        # Apply search
        search_query = self.get_search_query()
        queryset = self.apply_search(queryset, search_query)
        
        # Apply filters
        filter_params = self.get_filter_params()
        queryset = self.apply_filters(queryset, filter_params)
        
        return queryset.order_by('name')
    
    def get_context_data(self, **kwargs):
        """Add paginated results and extra context."""
        context = super().get_context_data(**kwargs)
        
        # Get the filtered queryset
        queryset = self.get_queryset()
        
        # Apply pagination
        paginated_facilities = self.get_paginated_queryset(queryset)
        context['facilities'] = paginated_facilities
        context['object_list'] = paginated_facilities
        
        # Add total count
        context['total_count'] = queryset.count()
        
        return context


class FacilityDetailView(DetailView):
    model = Facility
    template_name = "core/facility_detail.html"
    context_object_name = "facility"


class FacilityCreateView(CreateView):
    model = Facility
    fields = ["name", "location", "description", "partner_organization", "facility_type", "capabilities"]
    template_name = "core/facility_form.html"
    success_url = reverse_lazy("facility_list")


class FacilityUpdateView(UpdateView):
    model = Facility
    fields = ["name", "location", "description", "partner_organization", "facility_type", "capabilities"]
    template_name = "core/facility_form.html"
    success_url = reverse_lazy("facility_list")


class FacilityDeleteView(DeleteView):
    model = Facility
    template_name = "core/facility_confirm_delete.html"
    success_url = reverse_lazy("facility_list")

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, "Cannot delete this facility because it is referenced by other records.")
            return self.get(request, *args, **kwargs)