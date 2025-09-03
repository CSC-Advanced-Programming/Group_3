from django.contrib import admin
from .models import Program, Facility, Project, Equipment, Service, Participant, ProjectParticipant, Outcome

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("program_id", "name", "national_alignment", "focus_areas")
    search_fields = ("name", "national_alignment", "focus_areas")
    list_filter = ("national_alignment", "focus_areas")
    readonly_fields = ("program_id",)

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("facility_id", "name", "location", "facility_type", "partner_organization")
    search_fields = ("name", "location", "description")
    list_filter = ("facility_type", "partner_organization", "capabilities")
    readonly_fields = ("facility_id",)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("project_id", "title", "nature_of_project", "prototype_stage", "program", "facility")
    search_fields = ("title", "description", "innovation_focus")
    list_filter = ("nature_of_project", "prototype_stage", "program", "facility")
    readonly_fields = ("project_id",)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("equipment_id", "name", "facility", "usage_domain", "support_phase")
    search_fields = ("name", "capabilities", "description")
    list_filter = ("usage_domain", "support_phase", "facility")
    readonly_fields = ("equipment_id",)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("service_id", "name", "facility", "category", "skill_type")
    search_fields = ("name", "description")
    list_filter = ("category", "skill_type", "facility")
    readonly_fields = ("service_id",)

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("participant_id", "full_name", "email", "affiliation", "specialization", "institution")
    search_fields = ("full_name", "email")
    list_filter = ("affiliation", "specialization", "institution", "cross_skill_trained")
    readonly_fields = ("participant_id",)

@admin.register(ProjectParticipant)
class ProjectParticipantAdmin(admin.ModelAdmin):
    list_display = ("project", "participant", "role_on_project", "skill_role")
    search_fields = ("project__title", "participant__full_name")
    list_filter = ("role_on_project", "skill_role")

@admin.register(Outcome)
class OutcomeAdmin(admin.ModelAdmin):
    list_display = ("outcome_id", "title", "project", "outcome_type", "commercialization_status")
    search_fields = ("title", "description")
    list_filter = ("outcome_type", "commercialization_status", "project")
    readonly_fields = ("outcome_id",)
