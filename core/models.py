from django.db import models

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
    program = models.ForeignKey('Program', on_delete=models.PROTECT, related_name='projects')
    facility = models.ForeignKey('Facility', on_delete=models.PROTECT, related_name='projects')
    title = models.CharField(max_length=200)
    nature_of_project = models.CharField(
        max_length=100,
        choices=(
            ('Research', 'Research'),
            ('Prototype', 'Prototype'),
            ('Applied', 'Applied'),
        ),
        blank=True,
        null=True
    )
    description = models.TextField(blank=True, null=True)
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
    facility = models.ForeignKey('Facility', on_delete=models.PROTECT, related_name='equipment')
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
    facility = models.ForeignKey('Facility', on_delete=models.PROTECT, related_name='services')
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
    participant_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    affiliation = models.CharField(max_length=100, choices=(
        ('CS', 'CS'),
        ('SE', 'SE'),
        ('Engineering', 'Engineering'),
        ('Other', 'Other'),
    ))
    specialization = models.CharField(max_length=100, choices=(
        ('Software', 'Software'),
        ('Hardware', 'Hardware'),
        ('Business', 'Business'),
    ))
    cross_skill_trained = models.BooleanField(default=False)
    institution = models.CharField(max_length=100, choices=(
        ('SCIT', 'SCIT'),
        ('CEDAT', 'CEDAT'),
        ('UniPod', 'UniPod'),
        ('UIRI', 'UIRI'),
        ('Lwera', 'Lwera'),
    ))

    def save(self, *args, **kwargs):
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
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
class ProjectParticipant(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='project_participants')
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name='project_participants')
    role_on_project = models.CharField(max_length=100, choices=(
        ('Student', 'Student'),
        ('Lecturer', 'Lecturer'),
        ('Contributor', 'Contributor'),
    ))
    skill_role = models.CharField(max_length=100, choices=(
        ('Developer', 'Developer'),
        ('Engineer', 'Engineer'),
        ('Designer', 'Designer'),
        ('Business Lead', 'Business Lead'),
    ))

    class Meta:
        unique_together = ('project', 'participant')

    def __str__(self):
        return f"{self.participant.full_name} on {self.project.title} as {self.role_on_project}"
class Outcome(models.Model):
    outcome_id = models.CharField(max_length=10, unique=True, blank=True, null=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='outcomes')
    title = models.CharField(max_length=200)
    description = models.TextField()
    artifact_link = models.URLField(blank=True, null=True)
    outcome_type = models.CharField(max_length=100, choices=(
        ('CAD', 'CAD'),
        ('PCB', 'PCB'),
        ('Prototype', 'Prototype'),
        ('Report', 'Report'),
        ('Business Plan', 'Business Plan'),
    ))
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
