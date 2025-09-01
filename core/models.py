from django.db import models

# Create your models here.
class Program(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    national_alignment = models.CharField(max_length=255, blank=True, null=True)
    focus_areas = models.TextField(help_text="Comma-separated list of domains")
    phases = models.TextField(help_text="Comma-separated list of phases")
