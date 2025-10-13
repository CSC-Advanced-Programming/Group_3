"""Participant views implementation."""
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ...models import Participant
from ...forms import ParticipantForm
from ...utils import SearchFilterMixin, get_model_field_choices


class ParticipantListView(SearchFilterMixin, ListView):
    model = Participant
    template_name = "core/participant_list.html"
    context_object_name = "participants"
    
    # Search configuration
    search_fields = ['full_name', 'email', 'affiliation', 'specialization', 'institution']
    
    # Filter configuration
    filter_fields = {
        'affiliation': [],
        'specialization': [],
        'cross_skill_trained': [('True', 'Yes'), ('False', 'No')],
    }
    
    items_per_page = 15
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Populate filter choices dynamically
        self.filter_fields['affiliation'] = get_model_field_choices(Participant, 'affiliation')
        self.filter_fields['specialization'] = get_model_field_choices(Participant, 'specialization')
    
    def get_queryset(self):
        """Apply search and filters to the queryset."""
        queryset = Participant.objects.all()
        
        # Apply search
        search_query = self.get_search_query()
        queryset = self.apply_search(queryset, search_query)
        
        # Apply filters
        filter_params = self.get_filter_params()
        
        # Handle boolean filter for cross_skill_trained
        if 'cross_skill_trained' in filter_params:
            cross_skill_value = filter_params.pop('cross_skill_trained')
            if cross_skill_value == 'True':
                queryset = queryset.filter(cross_skill_trained=True)
            elif cross_skill_value == 'False':
                queryset = queryset.filter(cross_skill_trained=False)
        
        queryset = self.apply_filters(queryset, filter_params)
        
        return queryset.order_by('full_name')
    
    def get_context_data(self, **kwargs):
        """Add paginated results and extra context."""
        context = super().get_context_data(**kwargs)
        
        # Get the filtered queryset
        queryset = self.get_queryset()
        
        # Apply pagination
        paginated_participants = self.get_paginated_queryset(queryset)
        context['participants'] = paginated_participants
        context['object_list'] = paginated_participants
        
        # Add total count
        context['total_count'] = queryset.count()
        
        return context


class ParticipantDetailView(DetailView):
    model = Participant
    template_name = "core/participant_detail.html"
    context_object_name = "participant"


class ParticipantCreateView(CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = "core/participant_form.html"
    success_url = reverse_lazy("participant_list")


class ParticipantUpdateView(UpdateView):
    model = Participant
    form_class = ParticipantForm
    template_name = "core/participant_form.html"
    success_url = reverse_lazy("participant_list")


class ParticipantDeleteView(DeleteView):
    model = Participant
    template_name = "core/participant_confirm_delete.html"
    success_url = reverse_lazy("participant_list")