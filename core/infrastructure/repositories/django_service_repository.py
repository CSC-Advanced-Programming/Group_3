"""
Django ORM implementation of ServiceRepositoryInterface.
"""
from typing import List, Optional
from django.db.models import Q
from core.application.interfaces.service_repository import ServiceRepositoryInterface
from core.domain.entities.service import Service
from core.infrastructure.models.django_models import DjangoService


class DjangoServiceRepository(ServiceRepositoryInterface):
    """
    Django ORM implementation of Service repository.
    """

    def _to_entity(self, django_service: DjangoService) -> Service:
        """Convert Django model to domain entity."""
        return Service(
            id=django_service.id,
            service_id=django_service.service_id,
            facility_id=django_service.facility_id,
            name=django_service.name,
            description=django_service.description,
            category=django_service.category,
            skill_type=django_service.skill_type,
            created_at=django_service.created_at,
            updated_at=django_service.updated_at
        )

    def _to_django_model(self, service: Service, django_service: Optional[DjangoService] = None) -> DjangoService:
        """Convert domain entity to Django model."""
        if django_service is None:
            django_service = DjangoService()
        
        if service.id:
            django_service.id = service.id
        django_service.service_id = service.service_id
        django_service.facility_id = service.facility_id
        django_service.name = service.name
        django_service.description = service.description
        django_service.category = service.category
        django_service.skill_type = service.skill_type
        
        return django_service

    def save(self, service: Service) -> Service:
        """Save a service entity."""
        # Validate business rules
        if service.facility_id:
            existing_names = self.get_all_names_in_facility(service.facility_id, exclude_id=service.id)
            Service.validate_scoped_uniqueness(service.name, service.facility_id, existing_names)
        
        # Convert to Django model and save
        django_service = self._to_django_model(service)
        django_service.save()
        
        # Convert back to entity and return
        return self._to_entity(django_service)

    def get_by_id(self, service_id: int) -> Optional[Service]:
        """Retrieve a service by its ID."""
        try:
            django_service = DjangoService.objects.select_related('facility').get(id=service_id)
            return self._to_entity(django_service)
        except DjangoService.DoesNotExist:
            return None

    def get_by_service_id(self, service_id: str) -> Optional[Service]:
        """Retrieve a service by its service_id field."""
        try:
            django_service = DjangoService.objects.select_related('facility').get(service_id=service_id)
            return self._to_entity(django_service)
        except DjangoService.DoesNotExist:
            return None

    def get_all(self) -> List[Service]:
        """Retrieve all services."""
        django_services = DjangoService.objects.select_related('facility').all()
        return [self._to_entity(ds) for ds in django_services]

    def get_by_facility_id(self, facility_id: int) -> List[Service]:
        """Get services by facility ID."""
        django_services = DjangoService.objects.select_related('facility').filter(facility_id=facility_id)
        return [self._to_entity(ds) for ds in django_services]

    def exists_by_name_in_facility(self, name: str, facility_id: int, exclude_id: Optional[int] = None) -> bool:
        """Check if a service with given name exists in a facility."""
        queryset = DjangoService.objects.filter(name__iexact=name, facility_id=facility_id)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return queryset.exists()

    def get_all_names_in_facility(self, facility_id: int, exclude_id: Optional[int] = None) -> List[str]:
        """Get all service names in a facility for uniqueness validation."""
        queryset = DjangoService.objects.filter(facility_id=facility_id)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return list(queryset.values_list('name', flat=True))

    def is_used_by_project_testing(self, service_id: int) -> bool:
        """Check if service is used by any project testing requirements."""
        try:
            service = DjangoService.objects.get(id=service_id)
            # Check if any project's testing requirements mention this service's category
            from core.infrastructure.models.django_models import DjangoProject
            return DjangoProject.objects.filter(
                testing_requirements__icontains=service.category,
                facility_id=service.facility_id
            ).exists()
        except DjangoService.DoesNotExist:
            return False

    def delete(self, service_id: int) -> bool:
        """Delete a service by ID."""
        try:
            # Validate delete guard
            Service.validate_delete_guard(self.is_used_by_project_testing(service_id))
            
            django_service = DjangoService.objects.get(id=service_id)
            django_service.delete()
            return True
        except (DjangoService.DoesNotExist, ValueError):
            return False

    def update(self, service: Service) -> Service:
        """Update an existing service."""
        if not service.id:
            raise ValueError("Service ID is required for update")
        
        # Validate business rules
        if service.facility_id:
            existing_names = self.get_all_names_in_facility(service.facility_id, exclude_id=service.id)
            Service.validate_scoped_uniqueness(service.name, service.facility_id, existing_names)
        
        try:
            django_service = DjangoService.objects.get(id=service.id)
            django_service = self._to_django_model(service, django_service)
            django_service.save()
            return self._to_entity(django_service)
        except DjangoService.DoesNotExist:
            raise ValueError(f"Service with ID {service.id} not found")

    def search(self, query: str) -> List[Service]:
        """Search services by query string."""
        django_services = DjangoService.objects.select_related('facility').filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(skill_type__icontains=query)
        )
        return [self._to_entity(ds) for ds in django_services]

    def get_by_category(self, category: str) -> List[Service]:
        """Get services by category."""
        django_services = DjangoService.objects.select_related('facility').filter(category__iexact=category)
        return [self._to_entity(ds) for ds in django_services]

    def get_by_skill_type(self, skill_type: str) -> List[Service]:
        """Get services by skill type."""
        django_services = DjangoService.objects.select_related('facility').filter(skill_type__iexact=skill_type)
        return [self._to_entity(ds) for ds in django_services]

    def get_by_phase(self, phase: str) -> List[Service]:
        """Get services relevant for a specific project phase."""
        # This implementation uses the business logic from the Service entity
        all_services = self.get_all()
        return [service for service in all_services if service.is_relevant_for_project_phase(phase)]

    def get_for_skill_development(self, skill: str) -> List[Service]:
        """Get services that can support development of a specific skill."""
        # This implementation uses the business logic from the Service entity
        all_services = self.get_all()
        return [service for service in all_services if service.can_support_skill_development(skill)]