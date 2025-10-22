from django.db import models
from django.db.models.functions import Lower
from django.core.exceptions import ValidationError

# Create your models here.
import re

NATIONAL_ALIGNMENT_CHOICES = (
    ('NDPIII', 'NDPIII'),
    ('Roadmap', 'Roadmap'),
    ('4IR goals', '4IR goals'),
)

FOCUS_AREAS_CHOICES = (
    ('IoT', 'IoT'),
    ('automation', 'automation'),
    ('renewable energy', 'renewable energy'),
)

PHASES_CHOICES = (
    ('Cross-Skilling', 'Cross-Skilling'),
    ('Collaboration', 'Collaboration'),
    ('Technical Skills', 'Technical Skills'),
    ('Prototyping', 'Prototyping'),
    ('Commercialization', 'Commercialization'),
)

class Program(models.Model):
    program_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    national_alignment = models.CharField(max_length=255, choices=NATIONAL_ALIGNMENT_CHOICES, blank=True, null=True)
    focus_areas = models.CharField(max_length=255, choices=FOCUS_AREAS_CHOICES, help_text="Comma-separated list of domains")
    phases = models.CharField(max_length=255, choices=PHASES_CHOICES, help_text="Comma-separated list of phases")

    def save(self, *args, **kwargs):
        if not self.program_id:
            last_program = Program.objects.order_by('-program_id').first()
            if last_program and last_program.program_id:
                match = re.match(r'Pg-(\d+)', last_program.program_id)
                if match:
                    last_number = int(match.group(1))
                    new_number = last_number + 1
                else:
                    new_number = 1
            else:
                new_number = 1
            self.program_id = f'Pg-{new_number:03d}'
        super().save(*args, **kwargs)

    def clean(self):
        """Custom validation for Program business rules."""
        # Business Rule: If focus_areas set, national_alignment must be present
        if self.focus_areas and (not self.national_alignment):
            raise ValidationError({'national_alignment': 'When FocusAreas is set, NationalAlignment must also be valid.'})

        # Business Rule: name must be unique case-insensitive
        qs = Program.objects.filter(name__iexact=self.name)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError({'name': 'Program name must be unique (case-insensitive).'})

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        # Prevent deletion if related Projects exist (lifecycle protection)
        if self.projects.exists():
            raise ValidationError('Cannot delete Program with linked Projects.')
        return super().delete(*args, **kwargs)

PARTNER_ORGANIZATION_CHOICES = (
    ('UniPod', 'UniPod'),
    ('UIRI', 'UIRI'),
    ('Lwera', 'Lwera'),
)

FACILITY_TYPE_CHOICES = (
    ('Lab', 'Lab'),
    ('Workshop', 'Workshop'),
    ('Testing Center', 'Testing Center'),
)

CAPABILITIES_CHOICES = (
    ('CNC', 'CNC'),
    ('PCB fabrication', 'PCB fabrication'),
    ('materials testing', 'materials testing'),
)

class Facility(models.Model):
    facility_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    partner_organization = models.CharField(max_length=200, choices=PARTNER_ORGANIZATION_CHOICES, blank=True, null=True)
    facility_type = models.CharField(max_length=100, choices=FACILITY_TYPE_CHOICES)
    capabilities = models.CharField(max_length=255, choices=CAPABILITIES_CHOICES)

    def save(self, *args, **kwargs):
        if not self.facility_id:
            last_facility = Facility.objects.order_by('-facility_id').first()
            if last_facility and last_facility.facility_id:
                match = re.match(r'F-(\d+)', last_facility.facility_id)
                if match:
                    last_number = int(match.group(1))
                    new_number = last_number + 1
                else:
                    new_number = 1
            else:
                new_number = 1
            self.facility_id = f'F-{new_number:03d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Project(models.Model):
    project_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    program = models.ForeignKey('Program', on_delete=models.PROTECT, related_name='projects', null=True, blank=True)
    facility = models.ForeignKey('Facility', on_delete=models.PROTECT, related_name='projects', null=True, blank=True)
    title = models.CharField(max_length=200, default='New Project')
    nature_of_project = models.CharField(max_length=100, choices=(
        ('Research', 'Research'),
        ('Prototype', 'Prototype'),
        ('Applied', 'Applied'),
    ), default='Research')
    description = models.TextField(default='Project description')
    innovation_focus = models.CharField(max_length=255, blank=True, null=True)
    prototype_stage = models.CharField(max_length=100, choices=(
        ('Concept', 'Concept'),
        ('Prototype', 'Prototype'),
        ('MVP', 'MVP'),
        ('Market Launch', 'Market Launch'),
    ), blank=True, null=True)
    testing_requirements = models.TextField(blank=True, null=True)
    commercialization_plan = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.project_id:
            last_project = Project.objects.order_by('-project_id').first()
            if last_project and last_project.project_id:
                match = re.match(r'P-(\d+)', last_project.project_id)
                if match:
                    last_number = int(match.group(1))
                    new_number = last_number + 1
                else:
                    new_number = 1
            else:
                new_number = 1
            self.project_id = f'P-{new_number:03d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Equipment(models.Model):
    equipment_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    facility = models.ForeignKey('Facility', on_delete=models.PROTECT, related_name='equipment', null=True, blank=True)
    name = models.CharField(max_length=200)
    capabilities = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    inventory_code = models.CharField(max_length=100, blank=True, null=True)
    usage_domain = models.CharField(max_length=100, choices=(
        ('Electronics', 'Electronics'),
        ('Mechanical', 'Mechanical'),
        ('IoT', 'IoT'),
    ), blank=True, null=True)
    support_phase = models.CharField(max_length=100, choices=(
        ('Training', 'Training'),
        ('Prototyping', 'Prototyping'),
        ('Testing', 'Testing'),
        ('Commercialization', 'Commercialization'),
    ), blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.equipment_id:
            last_equipment = Equipment.objects.order_by('-equipment_id').first()
            if last_equipment and last_equipment.equipment_id:
                match = re.match(r'E-(\d+)', last_equipment.equipment_id)
                if match:
                    last_number = int(match.group(1))
                    new_number = last_number + 1
                else:
                    new_number = 1
            else:
                new_number = 1
            self.equipment_id = f'E-{new_number:03d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Service(models.Model):
    service_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    facility = models.ForeignKey('Facility', on_delete=models.PROTECT, related_name='services', null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, choices=(
        ('Machining', 'Machining'),
        ('Testing', 'Testing'),
        ('Training', 'Training'),
    ), blank=True, null=True)
    skill_type = models.CharField(max_length=100, choices=(
        ('Hardware', 'Hardware'),
        ('Software', 'Software'),
        ('Integration', 'Integration'),
    ), blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.service_id:
            last_service = Service.objects.order_by('-service_id').first()
            if last_service and last_service.service_id:
                match = re.match(r'S-(\d+)', last_service.service_id)
                if match:
                    last_number = int(match.group(1))
                    new_number = last_number + 1
                else:
                    new_number = 1
            else:
                new_number = 1
            self.service_id = f'S-{new_number:03d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
class Participant(models.Model):
    """
    Participant Entity - Represents individuals involved in projects.
    
    Business Rules:
    - BR1: Required Fields - FullName, Email, and Affiliation must be provided
    - BR2: Email Uniqueness - Email must be unique (case-insensitive)
    - BR3: Specialization Requirement - CrossSkillTrained can only be true if Specialization is set
    """
    participant_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=200)  # BR1: Required field
    # remove field-level unique=True so we can enforce case-insensitive uniqueness
    email = models.EmailField()  # BR1: Required, BR2: Unique (case-insensitive via DB constraint)
    affiliation = models.CharField(max_length=100, choices=(
        ('CS', 'CS'),
        ('SE', 'SE'),
        ('Engineering', 'Engineering'),
        ('Other', 'Other'),
    ))  # BR1: Required field
    specialization = models.CharField(max_length=100, choices=(
        ('Software', 'Software'),
        ('Hardware', 'Hardware'),
        ('Business', 'Business'),
    ), blank=True, null=True)  # BR3: Optional, but required if cross_skill_trained is True
    cross_skill_trained = models.BooleanField(default=False)  # BR3: Can only be True if specialization is set
    institution = models.CharField(max_length=100, choices=(
        ('SCIT', 'SCIT'),
        ('CEDAT', 'CEDAT'),
        ('UniPod', 'UniPod'),
        ('UIRI', 'UIRI'),
        ('Lwera', 'Lwera'),
    ), default='SCIT')

    def clean(self):
        """
        Validate business rules before saving.
        """
        from django.core.exceptions import ValidationError
        errors = {}

        # BR1: Required Fields - FullName, Email, and Affiliation must be provided
        if not self.full_name or not self.full_name.strip():
            errors['full_name'] = "Participant.FullName, Participant.Email, and Participant.Affiliation are required."
        
        if not self.email or not self.email.strip():
            if 'email' not in errors:
                errors['email'] = "Participant.FullName, Participant.Email, and Participant.Affiliation are required."
        
        if not self.affiliation:
            errors['affiliation'] = "Participant.FullName, Participant.Email, and Participant.Affiliation are required."

        # BR2: Email Uniqueness (case-insensitive)
        if self.email:
            existing = Participant.objects.filter(email__iexact=self.email).exclude(pk=self.pk)
            if existing.exists():
                errors['email'] = "Participant.Email already exists."

        # BR3: Specialization Requirement - CrossSkillTrained can only be true if Specialization is set
        if self.cross_skill_trained and not self.specialization:
            errors['cross_skill_trained'] = "Cross-skill flag requires Specialization."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        # Auto-generate participant_id if not provided
        if not self.participant_id:
            last_participant = Participant.objects.order_by('-participant_id').first()
            if last_participant and last_participant.participant_id:
                match = re.match(r'PT-(\d+)', last_participant.participant_id)
                if match:
                    last_number = int(match.group(1))
                    new_number = last_number + 1
                else:
                    new_number = 1
            else:
                new_number = 1
            self.participant_id = f'PT-{new_number:03d}'
        
        # Run validation before saving
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
    class Meta:
        constraints = [
            # Enforce case-insensitive uniqueness at the DB level for email
            models.UniqueConstraint(Lower('email'), name='unique_participant_email_ci')
        ]
class ProjectParticipant(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='project_participants')
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name='project_participants')
    role_on_project = models.CharField(max_length=100, choices=(
        ('Student', 'Student'),
        ('Lecturer', 'Lecturer'),
        ('Contributor', 'Contributor'),
    ), default='Student')
    skill_role = models.CharField(max_length=100, choices=(
        ('Developer', 'Developer'),
        ('Engineer', 'Engineer'),
        ('Designer', 'Designer'),
        ('Business Lead', 'Business Lead'),
    ), default='Developer')

    class Meta:
        unique_together = ('project', 'participant')

    def __str__(self):
        return f"{self.participant.full_name} on {self.project.title} as {self.role_on_project}"
class Outcome(models.Model):
    outcome_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='outcomes', null=True, blank=True)
    title = models.CharField(max_length=200, default='New Outcome')
    description = models.TextField(default='Outcome description')
    artifact_link = models.URLField(blank=True, null=True)
    outcome_type = models.CharField(max_length=100, choices=(
        ('CAD', 'CAD'),
        ('PCB', 'PCB'),
        ('Prototype', 'Prototype'),
        ('Report', 'Report'),
        ('Business Plan', 'Business Plan'),
    ), default='Report')
    quality_certification = models.CharField(max_length=255, blank=True, null=True)
    commercialization_status = models.CharField(max_length=100, choices=(
        ('Demoed', 'Demoed'),
        ('Market Linked', 'Market Linked'),
        ('Launched', 'Launched'),
    ), blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.outcome_id:
            last_outcome = Outcome.objects.order_by('-outcome_id').first()
            if last_outcome and last_outcome.outcome_id:
                match = re.match(r'O-(\d+)', last_outcome.outcome_id)
                if match:
                    last_number = int(match.group(1))
                    new_number = last_number + 1
                else:
                    new_number = 1
            else:
                new_number = 1
            self.outcome_id = f'O-{new_number:03d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
