"""ProjectParticipant views implementation."""
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ...models import ProjectParticipant, Project
from ...forms import ProjectParticipantForm
from ...utils import SearchFilterMixin, get_model_field_choices, get_related_model_choices


class ProjectParticipantListView(SearchFilterMixin, ListView):
    model = ProjectParticipant
    template_name = "core/projectparticipant_list.html"
    context_object_name = "projectparticipants"
    
    # Search configuration
    search_fields = ['project__title', 'participant__full_name', 'role_on_project']
    
    # Filter configuration
    filter_fields = {
        'role_on_project': [],
        'skill_role': [],
        'project': [],
        'participant': [],
    }
    
    items_per_page = 15
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Populate filter choices dynamically
        self.filter_fields['role_on_project'] = get_model_field_choices(ProjectParticipant, 'role_on_project')
        self.filter_fields['skill_role'] = get_model_field_choices(ProjectParticipant, 'skill_role')
        self.filter_fields['project'] = get_related_model_choices(ProjectParticipant, 'project')
        self.filter_fields['participant'] = get_related_model_choices(ProjectParticipant, 'participant')
    
    def get_queryset(self):
        """Apply search and filters to the queryset."""
        queryset = ProjectParticipant.objects.select_related('project', 'participant').all()
        
        # Apply search
        search_query = self.get_search_query()
        queryset = self.apply_search(queryset, search_query)
        
        # Apply filters
        filter_params = self.get_filter_params()
        queryset = self.apply_filters(queryset, filter_params)
        
        return queryset.order_by('-id')
    
    def get_context_data(self, **kwargs):
        """Add paginated results and extra context."""
        context = super().get_context_data(**kwargs)
        
        # Get the filtered queryset
        queryset = self.get_queryset()
        
        # Apply pagination
        paginated_projectparticipants = self.get_paginated_queryset(queryset)
        context['projectparticipants'] = paginated_projectparticipants
        context['object_list'] = paginated_projectparticipants
        
        # Add total count
        context['total_count'] = queryset.count()
        
        return context


class ProjectParticipantDetailView(DetailView):
    model = ProjectParticipant
    template_name = "core/projectparticipant_detail.html"
    context_object_name = "projectparticipant"


class ProjectParticipantCreateView(CreateView):
    model = ProjectParticipant
    form_class = ProjectParticipantForm
    template_name = "core/projectparticipant_form.html"
    success_url = reverse_lazy("projectparticipant_list")


class ProjectParticipantUpdateView(UpdateView):
    model = ProjectParticipant
    form_class = ProjectParticipantForm
    template_name = "core/projectparticipant_form.html"
    success_url = reverse_lazy("projectparticipant_list")


class ProjectParticipantForProjectCreateView(CreateView):
    model = ProjectParticipant
    fields = ["participant", "role_on_project", "skill_role"]
    template_name = "core/project_participant_form.html"
    
    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.kwargs['project_id']})
    
    def form_valid(self, form):
        form.instance.project_id = self.kwargs['project_id']
        return super().form_valid(form)


class ProjectParticipantDeleteView(DeleteView):
    model = ProjectParticipant
    template_name = "core/projectparticipant_confirm_delete.html"
    success_url = reverse_lazy("projectparticipant_list")