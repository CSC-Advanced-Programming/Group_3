from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Q
from .models import Program, Facility, Project, Equipment, Service, Participant, ProjectParticipant, Outcome
from .utils import SearchFilterMixin, get_model_field_choices, get_related_model_choices
# Project Views
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
    fields = ["program", "facility", "title", "nature_of_project", "description", "innovation_focus", "prototype_stage", "testing_requirements", "commercialization_plan"]
    template_name = "core/project_form.html"
    success_url = reverse_lazy("project_list")

    def get_initial(self):
        initial = super().get_initial()
        program_pk = self.request.GET.get('program')
        facility_pk = self.request.GET.get('facility')
        if program_pk:
            initial['program'] = program_pk
        if facility_pk:
            initial['facility'] = facility_pk
        return initial

class ProjectUpdateView(UpdateView):
    model = Project
    fields = ["program", "facility", "title", "nature_of_project", "description", "innovation_focus", "prototype_stage", "testing_requirements", "commercialization_plan"]
    template_name = "core/project_form.html"
    success_url = reverse_lazy("project_list")

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "core/project_confirm_delete.html"
    success_url = reverse_lazy("project_list")

# Equipment Views
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
        queryset = Equipment.objects.select_related('facility').all()
        
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

class EquipmentCreateView(CreateView):
    model = Equipment
    fields = ["facility", "name", "capabilities", "description", "inventory_code", "usage_domain", "support_phase"]
    template_name = "core/equipment_form.html"
    success_url = reverse_lazy("equipment_list")

    def get_initial(self):
        initial = super().get_initial()
        facility_pk = self.request.GET.get('facility')
        if facility_pk:
            initial['facility'] = facility_pk
        return initial

class EquipmentUpdateView(UpdateView):
    model = Equipment
    fields = ["facility", "name", "capabilities", "description", "inventory_code", "usage_domain", "support_phase"]
    template_name = "core/equipment_form.html"
    success_url = reverse_lazy("equipment_list")

class EquipmentDeleteView(DeleteView):
    model = Equipment
    template_name = "core/equipment_confirm_delete.html"
    success_url = reverse_lazy("equipment_list")

# Service Views
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
    fields = ["facility", "name", "description", "category", "skill_type"]
    template_name = "core/service_form.html"
    success_url = reverse_lazy("service_list")

    def get_initial(self):
        initial = super().get_initial()
        facility_pk = self.request.GET.get('facility')
        if facility_pk:
            initial['facility'] = facility_pk
        return initial

class ServiceUpdateView(UpdateView):
    model = Service
    fields = ["facility", "name", "description", "category", "skill_type"]
    template_name = "core/service_form.html"
    success_url = reverse_lazy("service_list")

class ServiceDeleteView(DeleteView):
    model = Service
    template_name = "core/service_confirm_delete.html"
    success_url = reverse_lazy("service_list")

# Participant Views
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
    fields = ["full_name", "email", "affiliation", "specialization", "cross_skill_trained", "institution"]
    template_name = "core/participant_form.html"
    success_url = reverse_lazy("participant_list")

class ParticipantUpdateView(UpdateView):
    model = Participant
    fields = ["full_name", "email", "affiliation", "specialization", "cross_skill_trained", "institution"]
    template_name = "core/participant_form.html"
    success_url = reverse_lazy("participant_list")

class ParticipantDeleteView(DeleteView):
    model = Participant
    template_name = "core/participant_confirm_delete.html"
    success_url = reverse_lazy("participant_list")

# ProjectParticipant Views
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
    fields = ["project", "participant", "role_on_project", "skill_role"]
    template_name = "core/projectparticipant_form.html"
    
    def get_initial(self):
        initial = super().get_initial()
        project_pk = self.request.GET.get('project')
        participant_pk = self.request.GET.get('participant')
        if project_pk:
            initial['project'] = project_pk
        if participant_pk:
            initial['participant'] = participant_pk
        return initial

    def get_success_url(self):
        # Redirect back to project detail if possible
        project = self.object.project
        if project:
            return reverse('project_detail', args=[project.pk])
        return reverse_lazy('projectparticipant_list')

class ProjectParticipantUpdateView(UpdateView):
    model = ProjectParticipant
    fields = ["project", "participant", "role_on_project", "skill_role"]
    template_name = "core/projectparticipant_form.html"
    success_url = reverse_lazy("projectparticipant_list")

class ProjectParticipantDeleteView(DeleteView):
    model = ProjectParticipant
    template_name = "core/projectparticipant_confirm_delete.html"
    def get_success_url(self):
        project = self.object.project
        if project:
            return reverse('project_detail', args=[project.pk])
        return reverse_lazy('projectparticipant_list')

# Outcome Views
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

from django import forms


class OutcomeForm(forms.ModelForm):
    class Meta:
        model = Outcome
        fields = ["project", "title", "description", "artifact_link", "artifact_file", "outcome_type", "quality_certification", "commercialization_status"]


class OutcomeCreateView(CreateView):
    model = Outcome
    form_class = OutcomeForm
    template_name = "core/outcome_form.html"

    def get_initial(self):
        initial = super().get_initial()
        project_pk = self.request.GET.get('project')
        if project_pk:
            initial['project'] = project_pk
        return initial

    def get_success_url(self):
        # If created from a project page, redirect to that project's detail
        project = self.object.project
        if project:
            return reverse('project_detail', args=[project.pk])
        return reverse_lazy("outcome_list")

class OutcomeUpdateView(UpdateView):
    model = Outcome
    form_class = OutcomeForm
    template_name = "core/outcome_form.html"

    def get_success_url(self):
        project = self.object.project
        if project:
            return reverse('project_detail', args=[project.pk])
        return reverse_lazy("outcome_list")

class OutcomeDeleteView(DeleteView):
    model = Outcome
    template_name = "core/outcome_confirm_delete.html"
    success_url = reverse_lazy("outcome_list")
from django.contrib import messages
from django.db.models import ProtectedError

class HomeView(TemplateView):
    template_name = "core/home.html"

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

# Facility Views
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
