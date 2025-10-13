"""
Django ORM implementation of FacilityRepositoryInterface.
"""
from typing import List, Optional, Tuple
from django.db.models import Q
from core.application.interfaces.facility_repository import FacilityRepositoryInterface
from core.domain.entities.facility import Facility as FacilityEntity
from core.infrastructure.models.django_models import Facility


class DjangoFacilityRepository(FacilityRepositoryInterface):
    """
    Django ORM implementation of Facility repository.
    """

    def _to_entity(self, django_facility: Facility) -> FacilityEntity:
        """Convert Django model to domain entity."""
        return FacilityEntity(
            id=django_facility.id,
            facility_id=django_facility.facility_id,
            name=django_facility.name,
            location=django_facility.location,
            description=django_facility.description,
            partner_organization=django_facility.partner_organization,
            facility_type=django_facility.facility_type,
            capabilities=django_facility.capabilities,
            created_at=None,
            updated_at=None
        )

    def _to_django_model(self, facility: FacilityEntity, django_facility: Optional[Facility] = None) -> Facility:
        """Convert domain entity to Django model."""
        if django_facility is None:
            django_facility = Facility()
        
        if facility.id:
            django_facility.id = facility.id
        django_facility.facility_id = facility.facility_id
        django_facility.name = facility.name
        django_facility.location = facility.location
        django_facility.description = facility.description
        django_facility.partner_organization = facility.partner_organization
        django_facility.facility_type = facility.facility_type
        django_facility.capabilities = facility.capabilities
        
        return django_facility

    def save(self, facility: FacilityEntity) -> FacilityEntity:
        """Save a facility entity."""
        # Validate business rules
        existing_combinations = self.get_all_name_location_combinations(exclude_id=facility.id)
        FacilityEntity.validate_uniqueness(facility.name, facility.location, existing_combinations)
        
        # Check capabilities requirement if this is an update
        if facility.id:
            has_services = self.has_services(facility.id)
            has_equipment = self.has_equipment(facility.id)
            facility.validate_capabilities_requirement(has_services, has_equipment)
        
        # Convert to Django model and save
        django_facility = self._to_django_model(facility)
        django_facility.save()
        
        # Convert back to entity and return
        return self._to_entity(django_facility)

    def get_by_id(self, facility_id: int) -> Optional[FacilityEntity]:
        """Get a facility by its ID."""
        try:
            django_facility = Facility.objects.get(id=facility_id)
            return self._to_entity(django_facility)
        except Facility.DoesNotExist:
            return None

    def get_by_facility_id(self, facility_id: str) -> Optional[FacilityEntity]:
        """Get a facility by its facility_id."""
        try:
            django_facility = Facility.objects.get(facility_id=facility_id)
            return self._to_entity(django_facility)
        except Facility.DoesNotExist:
            return None

    def get_all(self) -> List[FacilityEntity]:
        """Get all facilities."""
        django_facilities = Facility.objects.all()
        return [self._to_entity(df) for df in django_facilities]

    def get_by_name_and_location(self, name: str, location: str) -> Optional[FacilityEntity]:
        """Get a facility by name and location combination."""
        try:
            django_facility = Facility.objects.get(name__iexact=name, location__iexact=location)
            return self._to_entity(django_facility)
        except Facility.DoesNotExist:
            return None

    def exists_by_name_and_location(self, name: str, location: str, exclude_id: Optional[int] = None) -> bool:
        """Check if a facility with given name and location exists."""
        queryset = Facility.objects.filter(name__iexact=name, location__iexact=location)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return queryset.exists()

    def get_all_name_location_combinations(self, exclude_id: Optional[int] = None) -> List[Tuple[str, str]]:
        """Get all name-location combinations for uniqueness validation."""
        queryset = Facility.objects.all()
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return list(queryset.values_list('name', 'location'))

    def has_services(self, facility_id: int) -> bool:
        """Check if facility has associated services."""
        try:
            django_facility = Facility.objects.get(id=facility_id)
            return django_facility.services.exists()
        except Facility.DoesNotExist:
            return False

    def has_equipment(self, facility_id: int) -> bool:
        """Check if facility has associated equipment."""
        try:
            django_facility = Facility.objects.get(id=facility_id)
            return django_facility.equipment.exists()
        except Facility.DoesNotExist:
            return False

    def has_projects(self, facility_id: int) -> bool:
        """Check if facility has associated projects."""
        try:
            django_facility = Facility.objects.get(id=facility_id)
            return django_facility.projects.exists()
        except Facility.DoesNotExist:
            return False

    def delete(self, facility_id: int) -> bool:
        """Delete a facility by ID."""
        try:
            # Validate deletion constraints
            has_services = self.has_services(facility_id)
            has_equipment = self.has_equipment(facility_id)
            has_projects = self.has_projects(facility_id)
            FacilityEntity.validate_deletion_constraints(has_services, has_equipment, has_projects)
            
            django_facility = Facility.objects.get(id=facility_id)
            django_facility.delete()
            return True
        except (Facility.DoesNotExist, ValueError):
            return False

    def update(self, facility: FacilityEntity) -> FacilityEntity:
        """Update an existing facility."""
        if not facility.id:
            raise ValueError("Facility ID is required for update")
        
        # Validate business rules
        existing_combinations = self.get_all_name_location_combinations(exclude_id=facility.id)
        FacilityEntity.validate_uniqueness(facility.name, facility.location, existing_combinations)
        
        # Check capabilities requirement
        has_services = self.has_services(facility.id)
        has_equipment = self.has_equipment(facility.id)
        facility.validate_capabilities_requirement(has_services, has_equipment)
        
        try:
            django_facility = Facility.objects.get(id=facility.id)
            django_facility = self._to_django_model(facility, django_facility)
            django_facility.save()
            return self._to_entity(django_facility)
        except Facility.DoesNotExist:
            raise ValueError(f"Facility with ID {facility.id} not found")

    def search(self, query: str) -> List[FacilityEntity]:
        """Search facilities by query string."""
        django_facilities = Facility.objects.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query) |
            Q(capabilities__icontains=query) |
            Q(partner_organization__icontains=query)
        )
        return [self._to_entity(df) for df in django_facilities]

    def get_by_facility_type(self, facility_type: str) -> List[FacilityEntity]:
        """Get facilities by type."""
        django_facilities = Facility.objects.filter(facility_type__iexact=facility_type)
        return [self._to_entity(df) for df in django_facilities]

    def get_by_partner_organization(self, organization: str) -> List[FacilityEntity]:
        """Get facilities by partner organization."""
        django_facilities = Facility.objects.filter(partner_organization__iexact=organization)
        return [self._to_entity(df) for df in django_facilities]
        """Save a facility entity."""
        # Validate business rules
        existing_combinations = self.get_all_name_location_combinations(exclude_id=facility.id)
        Facility.validate_uniqueness(facility.name, facility.location, existing_combinations)
        
        # Check capabilities requirement if this is an update
        if facility.id:
            has_services = self.has_services(facility.id)
            has_equipment = self.has_equipment(facility.id)
            facility.validate_capabilities_requirement(has_services, has_equipment)
        
        # Convert to Django model and save
        django_facility = self._to_django_model(facility)
        django_facility.save()
        
        # Convert back to entity and return
        return self._to_entity(django_facility)

    def get_by_id(self, facility_id: int) -> Optional[Facility]:
        """Retrieve a facility by its ID."""
        try:
            django_facility = DjangoFacility.objects.get(id=facility_id)
            return self._to_entity(django_facility)
        except DjangoFacility.DoesNotExist:
            return None

    def get_by_facility_id(self, facility_id: str) -> Optional[Facility]:
        """Retrieve a facility by its facility_id field."""
        try:
            django_facility = DjangoFacility.objects.get(facility_id=facility_id)
            return self._to_entity(django_facility)
        except DjangoFacility.DoesNotExist:
            return None

    def get_all(self) -> List[Facility]:
        """Retrieve all facilities."""
        django_facilities = DjangoFacility.objects.all()
        return [self._to_entity(df) for df in django_facilities]

    def get_by_name_and_location(self, name: str, location: str) -> Optional[Facility]:
        """Retrieve a facility by name and location combination."""
        try:
            django_facility = DjangoFacility.objects.get(name__iexact=name, location__iexact=location)
            return self._to_entity(django_facility)
        except DjangoFacility.DoesNotExist:
            return None

    def exists_by_name_and_location(self, name: str, location: str, exclude_id: Optional[int] = None) -> bool:
        """Check if a facility with given name and location exists."""
        queryset = DjangoFacility.objects.filter(name__iexact=name, location__iexact=location)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return queryset.exists()

    def get_all_name_location_combinations(self, exclude_id: Optional[int] = None) -> List[Tuple[str, str]]:
        """Get all name-location combinations for uniqueness validation."""
        queryset = DjangoFacility.objects.all()
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return [(f.name, f.location) for f in queryset.values_list('name', 'location')]

    def has_services(self, facility_id: int) -> bool:
        """Check if facility has associated services."""
        try:
            django_facility = DjangoFacility.objects.get(id=facility_id)
            return django_facility.services.exists()
        except DjangoFacility.DoesNotExist:
            return False

    def has_equipment(self, facility_id: int) -> bool:
        """Check if facility has associated equipment."""
        try:
            django_facility = DjangoFacility.objects.get(id=facility_id)
            return django_facility.equipment.exists()
        except DjangoFacility.DoesNotExist:
            return False

    def has_projects(self, facility_id: int) -> bool:
        """Check if facility has associated projects."""
        try:
            django_facility = DjangoFacility.objects.get(id=facility_id)
            return django_facility.projects.exists()
        except DjangoFacility.DoesNotExist:
            return False

    def delete(self, facility_id: int) -> bool:
        """Delete a facility by ID."""
        try:
            # Validate deletion constraints
            has_services = self.has_services(facility_id)
            has_equipment = self.has_equipment(facility_id)
            has_projects = self.has_projects(facility_id)
            Facility.validate_deletion_constraints(has_services, has_equipment, has_projects)
            
            django_facility = DjangoFacility.objects.get(id=facility_id)
            django_facility.delete()
            return True
        except (DjangoFacility.DoesNotExist, ValueError):
            return False

    def update(self, facility: Facility) -> Facility:
        """Update an existing facility."""
        if not facility.id:
            raise ValueError("Facility ID is required for update")
        
        # Validate business rules
        existing_combinations = self.get_all_name_location_combinations(exclude_id=facility.id)
        Facility.validate_uniqueness(facility.name, facility.location, existing_combinations)
        
        # Check capabilities requirement
        has_services = self.has_services(facility.id)
        has_equipment = self.has_equipment(facility.id)
        facility.validate_capabilities_requirement(has_services, has_equipment)
        
        try:
            django_facility = DjangoFacility.objects.get(id=facility.id)
            django_facility = self._to_django_model(facility, django_facility)
            django_facility.save()
            return self._to_entity(django_facility)
        except DjangoFacility.DoesNotExist:
            raise ValueError(f"Facility with ID {facility.id} not found")

    def search(self, query: str) -> List[Facility]:
        """Search facilities by query string."""
        django_facilities = DjangoFacility.objects.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query) |
            Q(capabilities__icontains=query) |
            Q(partner_organization__icontains=query)
        )
        return [self._to_entity(df) for df in django_facilities]

    def get_by_facility_type(self, facility_type: str) -> List[Facility]:
        """Get facilities by type."""
        django_facilities = DjangoFacility.objects.filter(facility_type__iexact=facility_type)
        return [self._to_entity(df) for df in django_facilities]

    def get_by_partner_organization(self, organization: str) -> List[Facility]:
        """Get facilities by partner organization."""
        django_facilities = DjangoFacility.objects.filter(partner_organization__iexact=organization)
        return [self._to_entity(df) for df in django_facilities]

    def get_by_capability(self, capability: str) -> List[Facility]:
        """Get facilities that have a specific capability."""
        django_facilities = DjangoFacility.objects.filter(capabilities__icontains=capability)
        return [self._to_entity(df) for df in django_facilities]

    def get_by_location(self, location: str) -> List[Facility]:
        """Get facilities by location."""
        django_facilities = DjangoFacility.objects.filter(location__icontains=location)
        return [self._to_entity(df) for df in django_facilities]