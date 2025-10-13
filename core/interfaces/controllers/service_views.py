"""Service views implementation."""
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ...models import Service
from ...forms import ServiceForm
from ...utils import SearchFilterMixin, get_model_field_choices, get_related_model_choices


class ServiceListView(SearchFilterMixin, ListView):
    model = Service
    template_name = "core/service_list.html"
    context_object_name = "services"
    
    # Search configuration
    search_fields = ['name', 'description', 'facility__name']
    
    # Filter configuration
    filter_fields = {
        'category': [],
        'skill_type': [],
        'facility': [],
    }
    
    items_per_page = 15
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Populate filter choices dynamically
        self.filter_fields['category'] = get_model_field_choices(Service, 'category')
        self.filter_fields['skill_type'] = get_model_field_choices(Service, 'skill_type')
        self.filter_fields['facility'] = get_related_model_choices(Service, 'facility')
    
    def get_queryset(self):
        """Apply search and filters to the queryset."""
        queryset = Service.objects.select_related('facility').all()
        
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
        paginated_services = self.get_paginated_queryset(queryset)
        context['services'] = paginated_services
        context['object_list'] = paginated_services
        
        # Add total count
        context['total_count'] = queryset.count()
        
        return context


class ServiceDetailView(DetailView):
    model = Service
    template_name = "core/service_detail.html"
    context_object_name = "service"


class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = "core/service_form.html"
    success_url = reverse_lazy("service_list")


class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = "core/service_form.html"
    success_url = reverse_lazy("service_list")


class ServiceDeleteView(DeleteView):
    model = Service
    template_name = "core/service_confirm_delete.html"
    success_url = reverse_lazy("service_list")