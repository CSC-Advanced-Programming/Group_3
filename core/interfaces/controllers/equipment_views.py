"""Equipment views implementation."""
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ...models import Equipment
from ...forms import EquipmentForm
from ...utils import SearchFilterMixin, get_model_field_choices, get_related_model_choices


class EquipmentListView(SearchFilterMixin, ListView):
    model = Equipment
    template_name = "core/equipment_list.html"
    context_object_name = "equipment_list"
    
    # Search configuration
    search_fields = ['name', 'description', 'inventory_code', 'capabilities', 'facility__name']
    
    # Filter configuration
    filter_fields = {
        'usage_domain': [],
        'support_phase': [],
        'facility': [],
    }
    
    items_per_page = 15
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Populate filter choices dynamically
        self.filter_fields['usage_domain'] = get_model_field_choices(Equipment, 'usage_domain')
        self.filter_fields['support_phase'] = get_model_field_choices(Equipment, 'support_phase')
        self.filter_fields['facility'] = get_related_model_choices(Equipment, 'facility')
    
    def get_queryset(self):
        """Apply search and filters to the queryset."""
        queryset = Equipment.objects.select_related('facility').prefetch_related('facility__projects').all()
        
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
        paginated_equipment = self.get_paginated_queryset(queryset)
        context['equipment_list'] = paginated_equipment
        context['object_list'] = paginated_equipment
        
        # Add total count
        context['total_count'] = queryset.count()
        
        return context


class EquipmentDetailView(DetailView):
    model = Equipment
    template_name = "core/equipment_detail.html"
    context_object_name = "equipment"
    
    def get_queryset(self):
        return Equipment.objects.select_related('facility').prefetch_related(
            'facility__projects__program',
            'facility__equipment'
        )


class EquipmentCreateView(CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = "core/equipment_form.html"
    success_url = reverse_lazy("equipment_list")


class EquipmentUpdateView(UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = "core/equipment_form.html"
    success_url = reverse_lazy("equipment_list")


class EquipmentDeleteView(DeleteView):
    model = Equipment
    template_name = "core/equipment_confirm_delete.html"
    success_url = reverse_lazy("equipment_list")