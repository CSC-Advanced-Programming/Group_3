from django import forms
from .models import Program, Facility, Project, Equipment, Service, Participant, ProjectParticipant, Outcome


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["program", "facility", "title", "nature_of_project", "description",
                 "innovation_focus", "prototype_stage", "testing_requirements", "commercialization_plan"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize program field to show program names instead of object representation
        self.fields['program'].empty_label = "Select a program"
        self.fields['program'].queryset = Program.objects.all().order_by('name')

        # Customize facility field
        self.fields['facility'].empty_label = "Select a facility"
        self.fields['facility'].queryset = Facility.objects.all().order_by('name')

        # Add helpful text and make required fields clear
        self.fields['title'].widget.attrs.update({'placeholder': 'Enter project title'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Describe the project...', 'rows': 4})
        self.fields['innovation_focus'].widget.attrs.update({'placeholder': 'e.g., IoT, AI, Renewable Energy'})
        self.fields['testing_requirements'].widget.attrs.update({'placeholder': 'Describe testing requirements...', 'rows': 3})
        self.fields['commercialization_plan'].widget.attrs.update({'placeholder': 'Describe commercialization plan...', 'rows': 3})


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ["facility", "name", "capabilities", "description", "inventory_code",
                 "usage_domain", "support_phase"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['facility'].empty_label = "Select a facility"
        self.fields['facility'].queryset = Facility.objects.all().order_by('name')


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["facility", "name", "description", "category", "skill_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['facility'].empty_label = "Select a facility"
        self.fields['facility'].queryset = Facility.objects.all().order_by('name')


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["full_name", "email", "affiliation", "specialization", "cross_skill_trained", "institution"]


class ProjectParticipantForm(forms.ModelForm):
    class Meta:
        model = ProjectParticipant
        fields = ["project", "participant", "role_on_project", "skill_role"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].empty_label = "Select a project"
        self.fields['project'].queryset = Project.objects.all().order_by('title')
        self.fields['participant'].empty_label = "Select a participant"
        self.fields['participant'].queryset = Participant.objects.all().order_by('full_name')


class OutcomeForm(forms.ModelForm):
    class Meta:
        model = Outcome
        fields = ["project", "title", "description", "artifact_link", "outcome_type",
                 "quality_certification", "commercialization_status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].empty_label = "Select a project"
        self.fields['project'].queryset = Project.objects.all().order_by('title')