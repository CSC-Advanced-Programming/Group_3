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
    name = models.CharField(max_length=200)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT, related_name='projects')

    def __str__(Sself):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=200)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT, related_name='equipment')

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=200)
    facility = models.ForeignKey(Facility, on_delete=models.PROTECT, related_name='services')

    def __str__(self):
        return self.name
