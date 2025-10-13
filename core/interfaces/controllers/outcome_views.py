"""Outcome views implementation."""
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ...models import Outcome, Project
from ...forms import OutcomeForm
from ...utils import SearchFilterMixin, get_model_field_choices, get_related_model_choices


class OutcomeListView(SearchFilterMixin, ListView):
    model = Outcome
    template_name = "core/outcome_list.html"
    context_object_name = "outcomes"
    
    # Search configuration
    search_fields = ['title', 'description', 'project__title']
    
    # Filter configuration
    filter_fields = {
        'outcome_type': [],
        'quality_certification': [],
        'commercialization_status': [],
        'project': [],
    }
    
    items_per_page = 15
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Populate filter choices dynamically
        self.filter_fields['outcome_type'] = get_model_field_choices(Outcome, 'outcome_type')
        self.filter_fields['quality_certification'] = get_model_field_choices(Outcome, 'quality_certification')
        self.filter_fields['commercialization_status'] = get_model_field_choices(Outcome, 'commercialization_status')
        self.filter_fields['project'] = get_related_model_choices(Outcome, 'project')
    
    def get_queryset(self):
        """Apply search and filters to the queryset."""
        queryset = Outcome.objects.select_related('project').all()
        
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
        paginated_outcomes = self.get_paginated_queryset(queryset)
        context['outcomes'] = paginated_outcomes
        context['object_list'] = paginated_outcomes
        
        # Add total count
        context['total_count'] = queryset.count()
        
        return context


class OutcomeDetailView(DetailView):
    model = Outcome
    template_name = "core/outcome_detail.html"
    context_object_name = "outcome"


class OutcomeCreateView(CreateView):
    model = Outcome
    form_class = OutcomeForm
    template_name = "core/outcome_form.html"
    success_url = reverse_lazy("outcome_list")
    
    def get_initial(self):
        initial = super().get_initial()
        if 'project' in self.request.GET:
            project_id = self.request.GET.get('project')
            try:
                initial['project'] = Project.objects.get(pk=project_id)
            except Project.DoesNotExist:
                pass
        return initial
    
    def get_success_url(self):
        if 'project' in self.request.GET:
            try:
                project_id = self.request.GET.get('project')
                return reverse_lazy('project_detail', kwargs={'pk': project_id})
            except:
                pass
        return self.success_url


class OutcomeUpdateView(UpdateView):
    model = Outcome
    form_class = OutcomeForm
    template_name = "core/outcome_form.html"
    success_url = reverse_lazy("outcome_list")


class OutcomeDeleteView(DeleteView):
    model = Outcome
    template_name = "core/outcome_confirm_delete.html"
    success_url = reverse_lazy("outcome_list")