"""
Django ORM implementation of ProjectRepositoryInterface.
"""
from typing import List, Optional
from django.db.models import Q
from core.application.interfaces.project_repository import ProjectRepositoryInterface
from core.domain.entities.project import Project as ProjectEntity
from core.infrastructure.models.django_models import Project, Facility, Program


class DjangoProjectRepository(ProjectRepositoryInterface):
    """
    Django ORM implementation of Project repository.
    """

    def _to_entity(self, django_project: Project) -> ProjectEntity:
        """Convert Django model to domain entity."""
        return ProjectEntity(
            id=django_project.id,
            project_id=django_project.project_id,
            program_id=django_project.program.id if django_project.program else None,
            facility_id=django_project.facility.id if django_project.facility else None,
            title=django_project.title,
            nature_of_project=django_project.nature_of_project,
            description=django_project.description,
            innovation_focus=django_project.innovation_focus,
            prototype_stage=django_project.prototype_stage,
            testing_requirements=django_project.testing_requirements,
            commercialization_plan=django_project.commercialization_plan,
            created_at=None,
            updated_at=None
        )

    def _to_django_model(self, project: ProjectEntity, django_project: Optional[Project] = None) -> Project:
        """Convert domain entity to Django model."""
        if django_project is None:
            django_project = Project()
        
        if project.id:
            django_project.id = project.id
        django_project.project_id = project.project_id
        if project.program_id:
            django_project.program = Program.objects.get(id=project.program_id)
        if project.facility_id:
            django_project.facility = Facility.objects.get(id=project.facility_id)
        django_project.title = project.title
        django_project.nature_of_project = project.nature_of_project
        django_project.description = project.description
        django_project.innovation_focus = project.innovation_focus
        django_project.prototype_stage = project.prototype_stage
        django_project.testing_requirements = project.testing_requirements
        django_project.commercialization_plan = project.commercialization_plan
        
        return django_project

    def save(self, project: Project) -> Project:
        """Save a project entity."""
        # Validate business rules
        if project.program_id:
            existing_titles = self.get_all_titles_in_program(project.program_id, exclude_id=project.id)
            Project.validate_name_uniqueness(project.title, project.program_id, existing_titles)
        
        if project.facility_id:
            facility_capabilities = self.get_facility_capabilities(project.facility_id)
            project_requirements = project.get_technical_requirements()
            Project.validate_facility_compatibility(project_requirements, facility_capabilities)
        
        # Convert to Django model and save
        django_project = self._to_django_model(project)
        django_project.save()
        
        # Convert back to entity and return
        return self._to_entity(django_project)

    def get_by_id(self, project_id: int) -> Optional[Project]:
        """Retrieve a project by its ID."""
        try:
            django_project = DjangoProject.objects.select_related('program', 'facility').get(id=project_id)
            return self._to_entity(django_project)
        except DjangoProject.DoesNotExist:
            return None

    def get_by_project_id(self, project_id: str) -> Optional[Project]:
        """Retrieve a project by its project_id field."""
        try:
            django_project = DjangoProject.objects.select_related('program', 'facility').get(project_id=project_id)
            return self._to_entity(django_project)
        except DjangoProject.DoesNotExist:
            return None

    def get_all(self) -> List[Project]:
        """Retrieve all projects."""
        django_projects = DjangoProject.objects.select_related('program', 'facility').all()
        return [self._to_entity(dp) for dp in django_projects]

    def get_by_program_id(self, program_id: int) -> List[Project]:
        """Get projects by program ID."""
        django_projects = DjangoProject.objects.select_related('program', 'facility').filter(program_id=program_id)
        return [self._to_entity(dp) for dp in django_projects]

    def get_by_facility_id(self, facility_id: int) -> List[Project]:
        """Get projects by facility ID."""
        django_projects = DjangoProject.objects.select_related('program', 'facility').filter(facility_id=facility_id)
        return [self._to_entity(dp) for dp in django_projects]

    def exists_by_title_in_program(self, title: str, program_id: int, exclude_id: Optional[int] = None) -> bool:
        """Check if a project with given title exists in a program."""
        queryset = DjangoProject.objects.filter(title__iexact=title, program_id=program_id)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return queryset.exists()

    def get_all_titles_in_program(self, program_id: int, exclude_id: Optional[int] = None) -> List[str]:
        """Get all project titles in a program for uniqueness validation."""
        queryset = DjangoProject.objects.filter(program_id=program_id)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return list(queryset.values_list('title', flat=True))

    def has_team_members(self, project_id: int) -> bool:
        """Check if project has team members assigned."""
        try:
            django_project = DjangoProject.objects.get(id=project_id)
            return django_project.project_participants.exists()
        except DjangoProject.DoesNotExist:
            return False

    def has_outcomes(self, project_id: int) -> bool:
        """Check if project has outcomes."""
        try:
            django_project = DjangoProject.objects.get(id=project_id)
            return django_project.outcomes.exists()
        except DjangoProject.DoesNotExist:
            return False

    def get_facility_capabilities(self, facility_id: int) -> List[str]:
        """Get capabilities of a facility for compatibility checking."""
        try:
            facility = DjangoFacility.objects.get(id=facility_id)
            if facility.capabilities:
                return [cap.strip() for cap in facility.capabilities.split(',') if cap.strip()]
            return []
        except DjangoFacility.DoesNotExist:
            return []

    def delete(self, project_id: int) -> bool:
        """Delete a project by ID."""
        try:
            django_project = DjangoProject.objects.get(id=project_id)
            django_project.delete()
            return True
        except DjangoProject.DoesNotExist:
            return False

    def update(self, project: Project) -> Project:
        """Update an existing project."""
        if not project.id:
            raise ValueError("Project ID is required for update")
        
        # Validate business rules
        if project.program_id:
            existing_titles = self.get_all_titles_in_program(project.program_id, exclude_id=project.id)
            Project.validate_name_uniqueness(project.title, project.program_id, existing_titles)
        
        if project.facility_id:
            facility_capabilities = self.get_facility_capabilities(project.facility_id)
            project_requirements = project.get_technical_requirements()
            Project.validate_facility_compatibility(project_requirements, facility_capabilities)
        
        try:
            django_project = DjangoProject.objects.get(id=project.id)
            django_project = self._to_django_model(project, django_project)
            django_project.save()
            return self._to_entity(django_project)
        except DjangoProject.DoesNotExist:
            raise ValueError(f"Project with ID {project.id} not found")

    def search(self, query: str) -> List[Project]:
        """Search projects by query string."""
        django_projects = DjangoProject.objects.select_related('program', 'facility').filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(innovation_focus__icontains=query) |
            Q(program__name__icontains=query) |
            Q(facility__name__icontains=query)
        )
        return [self._to_entity(dp) for dp in django_projects]

    def get_by_nature(self, nature: str) -> List[Project]:
        """Get projects by nature."""
        django_projects = DjangoProject.objects.select_related('program', 'facility').filter(nature_of_project__iexact=nature)
        return [self._to_entity(dp) for dp in django_projects]

    def get_by_prototype_stage(self, stage: str) -> List[Project]:
        """Get projects by prototype stage."""
        django_projects = DjangoProject.objects.select_related('program', 'facility').filter(prototype_stage__iexact=stage)
        return [self._to_entity(dp) for dp in django_projects]

    def get_by_innovation_focus(self, focus: str) -> List[Project]:
        """Get projects by innovation focus."""
        django_projects = DjangoProject.objects.select_related('program', 'facility').filter(innovation_focus__icontains=focus)
        return [self._to_entity(dp) for dp in django_projects]

    def get_completed_projects(self) -> List[Project]:
        """Get all completed projects."""
        django_projects = DjangoProject.objects.select_related('program', 'facility').filter(status__iexact='completed')
        return [self._to_entity(dp) for dp in django_projects]

    def get_active_projects(self) -> List[Project]:
        """Get all active (non-completed) projects."""
        django_projects = DjangoProject.objects.select_related('program', 'facility').exclude(status__iexact='completed')
        return [self._to_entity(dp) for dp in django_projects]