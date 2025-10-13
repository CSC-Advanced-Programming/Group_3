"""
Django ORM implementation of ProgramRepositoryInterface.
"""
from typing import List, Optional
from django.db.models import Q
from core.application.interfaces.program_repository import ProgramRepositoryInterface
from core.domain.entities.program import Program as ProgramEntity
from core.infrastructure.models.django_models import Program


class DjangoProgramRepository(ProgramRepositoryInterface):
    """
    Django ORM implementation of Program repository.
    """

    def _to_entity(self, django_program: Program) -> ProgramEntity:
        """Convert Django model to domain entity."""
        return ProgramEntity(
            id=django_program.id,
            program_id=django_program.program_id,
            name=django_program.name,
            description=django_program.description,
            national_alignment=django_program.national_alignment,
            focus_areas=django_program.focus_areas,
            phases=django_program.phases,
            created_at=None,
            updated_at=None
        )

    def _to_django_model(self, program: ProgramEntity, django_program: Optional[Program] = None) -> Program:
        """Convert domain entity to Django model."""
        if django_program is None:
            django_program = Program()
        
        if program.id:
            django_program.id = program.id
        django_program.program_id = program.program_id
        django_program.name = program.name
        django_program.description = program.description
        django_program.national_alignment = program.national_alignment
        django_program.focus_areas = program.focus_areas
        django_program.phases = program.phases
        
        return django_program

    def save(self, program: ProgramEntity) -> ProgramEntity:
        """Save a program entity."""
        # Validate business rules
        existing_names = self.get_all_names(exclude_id=program.id)
        ProgramEntity.validate_uniqueness(program.name, existing_names)
        
        # Convert to Django model and save
        django_program = self._to_django_model(program)
        django_program.save()
        
        # Convert back to entity and return
        return self._to_entity(django_program)

    def get_by_id(self, program_id: int) -> Optional[ProgramEntity]:
        """Get a program by its ID."""
        try:
            django_program = Program.objects.get(id=program_id)
            return self._to_entity(django_program)
        except Program.DoesNotExist:
            return None

    def get_by_program_id(self, program_id: str) -> Optional[ProgramEntity]:
        """Get a program by its program_id."""
        try:
            django_program = Program.objects.get(program_id=program_id)
            return self._to_entity(django_program)
        except Program.DoesNotExist:
            return None

    def get_all(self) -> List[ProgramEntity]:
        """Get all programs."""
        django_programs = Program.objects.all()
        return [self._to_entity(p) for p in django_programs]

    def get_by_name(self, name: str) -> Optional[ProgramEntity]:
        """Get a program by its name."""
        try:
            django_program = Program.objects.get(name__iexact=name)
            return self._to_entity(django_program)
        except Program.DoesNotExist:
            return None

    def exists_by_name(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """Check if a program exists by name."""
        queryset = Program.objects.filter(name__iexact=name)
        if exclude_id is not None:
            queryset = queryset.exclude(id=exclude_id)
        return queryset.exists()

    def get_all_names(self, exclude_id: Optional[int] = None) -> List[str]:
        """Get all program names."""
        queryset = Program.objects.all()
        if exclude_id is not None:
            queryset = queryset.exclude(id=exclude_id)
        return list(queryset.values_list('name', flat=True))

    def has_projects(self, program_id: int) -> bool:
        """Check if program has associated projects."""
        try:
            django_program = Program.objects.get(id=program_id)
            return django_program.projects.exists()
        except Program.DoesNotExist:
            return False

    def delete(self, program_id: int) -> bool:
        """Delete a program by ID."""
        try:
            # Validate lifecycle protection
            ProgramEntity.validate_lifecycle_protection(self.has_projects(program_id))
            
            django_program = Program.objects.get(id=program_id)
            django_program.delete()
            return True
        except (Program.DoesNotExist, ValueError):
            return False

    def update(self, program: ProgramEntity) -> ProgramEntity:
        """Update an existing program."""
        if not program.id:
            raise ValueError("Program ID is required for update")
        
        # Validate business rules
        existing_names = self.get_all_names(exclude_id=program.id)
        ProgramEntity.validate_uniqueness(program.name, existing_names)
        
        try:
            django_program = Program.objects.get(id=program.id)
            django_program = self._to_django_model(program, django_program)
            django_program.save()
            return self._to_entity(django_program)
        except Program.DoesNotExist:
            raise ValueError(f"Program with ID {program.id} not found")

    def search(self, query: str) -> List[ProgramEntity]:
        """Search programs by query string."""
        django_programs = Program.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(focus_areas__icontains=query) |
            Q(national_alignment__icontains=query)
        )
        return [self._to_entity(dp) for dp in django_programs]

    def get_by_focus_area(self, focus_area: str) -> List[ProgramEntity]:
        """Get programs by focus area."""
        django_programs = Program.objects.filter(focus_areas__icontains=focus_area)
        return [self._to_entity(dp) for dp in django_programs]

    def get_by_national_alignment(self, alignment: str) -> List[ProgramEntity]:
        """Get programs by national alignment."""
        django_programs = Program.objects.filter(national_alignment__icontains=alignment)
        return [self._to_entity(dp) for dp in django_programs]