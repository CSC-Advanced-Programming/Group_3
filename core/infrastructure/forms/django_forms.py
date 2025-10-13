"""Django form implementations."""
from typing import Any, Dict, Optional
from django import forms

from core.application.interfaces.form_interfaces import (
    ProjectFormInterface,
    EquipmentFormInterface,
    ServiceFormInterface,
    ProjectParticipantFormInterface
)
from core.models import (
    Program, Facility, Project, Equipment, Service,
    Participant, ProjectParticipant, Outcome
)


# Common form interface methods are implemented directly in each form class


class DjangoProjectForm(forms.ModelForm):
    """Django implementation of project form."""

    class Meta:
        model = Project
        fields = [
            "program", "facility", "title", "nature_of_project", "description",
            "innovation_focus", "prototype_stage", "testing_requirements", 
            "commercialization_plan"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setup_fields()

    def _setup_fields(self):
        """Setup form fields with customizations."""
        # Program field
        self.fields['program'].empty_label = "Select a program"
        self.fields['program'].queryset = self.get_programs()

        # Facility field
        self.fields['facility'].empty_label = "Select a facility"
        self.fields['facility'].queryset = self.get_facilities()

        # Field customizations
        self.fields['title'].widget.attrs.update({'placeholder': 'Enter project title'})
        self.fields['description'].widget.attrs.update({
            'placeholder': 'Describe the project...',
            'rows': 4
        })
        self.fields['innovation_focus'].widget.attrs.update({
            'placeholder': 'e.g., IoT, AI, Renewable Energy'
        })
        self.fields['testing_requirements'].widget.attrs.update({
            'placeholder': 'Describe testing requirements...',
            'rows': 3
        })
        self.fields['commercialization_plan'].widget.attrs.update({
            'placeholder': 'Describe commercialization plan...',
            'rows': 3
        })

    def get_programs(self):
        """Get available programs."""
        return Program.objects.all().order_by('name')

    def get_facilities(self):
        """Get available facilities."""
        return Facility.objects.all().order_by('name')


class DjangoEquipmentForm(forms.ModelForm):
    """Django implementation of equipment form."""

    class Meta:
        model = Equipment
        fields = [
            "facility", "name", "capabilities", "description", 
            "inventory_code", "usage_domain", "support_phase"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setup_fields()

    def _setup_fields(self):
        """Setup form fields with customizations."""
        self.fields['facility'].empty_label = "Select a facility"
        self.fields['facility'].queryset = self.get_facilities()

    def get_facilities(self):
        """Get available facilities."""
        return Facility.objects.all().order_by('name')


class DjangoServiceForm(forms.ModelForm):
    """Django implementation of service form."""

    class Meta:
        model = Service
        fields = ["facility", "name", "description", "category", "skill_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setup_fields()

    def _setup_fields(self):
        """Setup form fields with customizations."""
        self.fields['facility'].empty_label = "Select a facility"
        self.fields['facility'].queryset = self.get_facilities()

    def get_facilities(self):
        """Get available facilities."""
        return Facility.objects.all().order_by('name')


class DjangoParticipantForm(forms.ModelForm):
    """Django implementation of participant form."""

    class Meta:
        model = Participant
        fields = [
            "full_name", "email", "affiliation", "specialization", 
            "cross_skill_trained", "institution"
        ]


class DjangoProjectParticipantForm(forms.ModelForm):
    """Django implementation of project participant form."""

    class Meta:
        model = ProjectParticipant
        fields = ["project", "participant", "role_on_project", "skill_role"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setup_fields()

    def _setup_fields(self):
        """Setup form fields with customizations."""
        self.fields['project'].empty_label = "Select a project"
        self.fields['project'].queryset = self.get_projects()
        self.fields['participant'].empty_label = "Select a participant"
        self.fields['participant'].queryset = self.get_participants()

    def get_projects(self):
        """Get available projects."""
        return Project.objects.all().order_by('title')

    def get_participants(self):
        """Get available participants."""
        return Participant.objects.all().order_by('full_name')


class DjangoOutcomeForm(forms.ModelForm):
    """Django implementation of outcome form."""

    class Meta:
        model = Outcome
        fields = [
            "project", "title", "description", "artifact_link", 
            "outcome_type", "quality_certification", "commercialization_status"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._setup_fields()

    def _setup_fields(self):
        """Setup form fields with customizations."""
        self.fields['project'].empty_label = "Select a project"
        self.fields['project'].queryset = Project.objects.all().order_by('title')