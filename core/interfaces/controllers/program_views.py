"""Home and Program views implementation."""
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.db.models import ProtectedError
from ...models import Program
from ...utils import SearchFilterMixin, get_model_field_choices


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        """Add statistics to the context."""
        context = super().get_context_data(**kwargs)
        # Get all programs for the stats
        context['programs'] = Program.objects.all()
        return context


class ProgramListView(SearchFilterMixin, ListView):
    model = Program
    template_name = "core/program_list.html"
    context_object_name = "programs"
    
    # Search configuration
    search_fields = ['name', 'description', 'program_id']
    
    # Filter configuration
    filter_fields = {
        'national_alignment': [],
        'focus_areas': [],
        'phases': [],
    }
    
    items_per_page = 15
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Populate filter choices dynamically
        self.filter_fields['national_alignment'] = get_model_field_choices(Program, 'national_alignment')
        self.filter_fields['focus_areas'] = get_model_field_choices(Program, 'focus_areas')
        self.filter_fields['phases'] = get_model_field_choices(Program, 'phases')
    
    def get_queryset(self):
        """Apply search and filters to the queryset."""
        queryset = Program.objects.all()
        
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
        paginated_programs = self.get_paginated_queryset(queryset)
        context['programs'] = paginated_programs
        context['object_list'] = paginated_programs
        
        # Add total count
        context['total_count'] = queryset.count()
        
        return context


class ProgramDetailView(DetailView):
    model = Program
    template_name = "core/program_detail.html"
    context_object_name = "program"

    def get_context_data(self, **kwargs):
        """Add associated projects to the context.

        Ensure `projects` is present for templates that expect it and also
        provide `associated_projects` for backward compatibility.
        """
        context = super().get_context_data(**kwargs)
        # Get all projects associated with this program and include facility
        projects_qs = self.object.projects.select_related('facility').all()
        context['projects'] = projects_qs
        context['associated_projects'] = projects_qs
        return context


class ProgramCreateView(CreateView):
    model = Program
    fields = ["name", "description", "national_alignment", "focus_areas", "phases"]
    template_name = "core/program_form.html"
    success_url = reverse_lazy("program_list")


class ProgramUpdateView(UpdateView):
    model = Program
    fields = ["name", "description", "national_alignment", "focus_areas", "phases"]
    template_name = "core/program_form.html"
    success_url = reverse_lazy("program_list")


class ProgramDeleteView(DeleteView):
    model = Program
    template_name = "core/program_confirm_delete.html"
    success_url = reverse_lazy("program_list")