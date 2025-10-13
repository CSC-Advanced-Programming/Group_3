"""Project views implementation."""
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ...models import Project
from ...forms import ProjectForm
from ...utils import SearchFilterMixin, get_model_field_choices, get_related_model_choices


class ProjectListView(SearchFilterMixin, ListView):
    model = Project
    template_name = "core/project_list.html"
    context_object_name = "projects"
    
    # Search configuration
    search_fields = ['title', 'description', 'program__name', 'facility__name']
    
    # Filter configuration
    filter_fields = {
        'nature_of_project': [],  # Will be populated from model choices
        'innovation_focus': [],
        'prototype_stage': [],
        'program': [],  # Will be populated from related Program objects
        'facility': [],  # Will be populated from related Facility objects
    }
    
    # Sortable fields
    sortable_fields = ['title', 'nature_of_project', 'innovation_focus', 'prototype_stage', 'program__name', 'facility__name']
    
    items_per_page = 15
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Populate filter choices dynamically
        self.filter_fields['nature_of_project'] = get_model_field_choices(Project, 'nature_of_project')
        self.filter_fields['innovation_focus'] = get_model_field_choices(Project, 'innovation_focus')
        self.filter_fields['prototype_stage'] = get_model_field_choices(Project, 'prototype_stage')
        self.filter_fields['program'] = get_related_model_choices(Project, 'program')
        self.filter_fields['facility'] = get_related_model_choices(Project, 'facility')
    
    def get_queryset(self):
        """Apply search and filters to the queryset."""
        queryset = Project.objects.select_related('program', 'facility').all()
        
        # Apply search
        search_query = self.get_search_query()
        queryset = self.apply_search(queryset, search_query)
        
        # Apply filters
        filter_params = self.get_filter_params()
        queryset = self.apply_filters(queryset, filter_params)
        
        # Apply sorting
        sort_param = self.get_sort_param()
        if sort_param:
            queryset = self.apply_sorting(queryset, sort_param)
        else:
            queryset = queryset.order_by('-id')  # Default order by newest first
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add paginated results and extra context."""
        context = super().get_context_data(**kwargs)
        
        # Get the filtered queryset
        queryset = self.get_queryset()
        
        # Apply pagination
        paginated_projects = self.get_paginated_queryset(queryset)
        context['projects'] = paginated_projects
        context['object_list'] = paginated_projects
        
        # Add total count
        context['total_count'] = queryset.count()
        
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "core/project_detail.html"
    context_object_name = "project"


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "core/project_form.html"
    success_url = reverse_lazy("project_list")


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "core/project_form.html"
    success_url = reverse_lazy("project_list")


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "core/project_confirm_delete.html"
    success_url = reverse_lazy("project_list")