"""
Django ORM implementation of EquipmentRepositoryInterface.
"""
from typing import List, Optional
from django.db.models import Q
from core.application.interfaces.equipment_repository import EquipmentRepositoryInterface
from core.domain.entities.equipment import Equipment as EquipmentEntity
from core.infrastructure.models.django_models import Equipment, Facility


class DjangoEquipmentRepository(EquipmentRepositoryInterface):
    """
    Django ORM implementation of Equipment repository.
    """

    def _to_entity(self, django_equipment: Equipment) -> EquipmentEntity:
        """Convert Django model to domain entity."""
        return EquipmentEntity(
            id=django_equipment.id,
            equipment_id=django_equipment.equipment_id,
            facility_id=django_equipment.facility.id if django_equipment.facility else None,
            name=django_equipment.name,
            capabilities=django_equipment.capabilities,
            description=django_equipment.description,
            inventory_code=django_equipment.inventory_code,
            usage_domain=django_equipment.usage_domain,
            support_phase=django_equipment.support_phase,
            created_at=None,
            updated_at=None
        )

    def _to_django_model(self, equipment: EquipmentEntity, django_equipment: Optional[Equipment] = None) -> Equipment:
        """Convert domain entity to Django model."""
        if django_equipment is None:
            django_equipment = Equipment()
        
        if equipment.id:
            django_equipment.id = equipment.id
        django_equipment.equipment_id = equipment.equipment_id
        django_equipment.facility_id = equipment.facility_id
        django_equipment.name = equipment.name
        django_equipment.capabilities = equipment.capabilities
        django_equipment.description = equipment.description
        django_equipment.inventory_code = equipment.inventory_code
        django_equipment.usage_domain = equipment.usage_domain
        django_equipment.support_phase = equipment.support_phase
        
        return django_equipment

    def save(self, equipment: Equipment) -> Equipment:
        """Save an equipment entity."""
        # Validate business rules
        existing_codes = self.get_all_inventory_codes(exclude_id=equipment.id)
        Equipment.validate_uniqueness(equipment.inventory_code, existing_codes)
        
        # Convert to Django model and save
        django_equipment = self._to_django_model(equipment)
        django_equipment.save()
        
        # Convert back to entity and return
        return self._to_entity(django_equipment)

    def get_by_id(self, equipment_id: int) -> Optional[Equipment]:
        """Retrieve equipment by its ID."""
        try:
            django_equipment = Equipment.objects.select_related('facility').get(id=equipment_id)
            return self._to_entity(django_equipment)
        except DjangoEquipment.DoesNotExist:
            return None

    def get_by_equipment_id(self, equipment_id: str) -> Optional[Equipment]:
        """Retrieve equipment by its equipment_id field."""
        try:
            django_equipment = Equipment.objects.select_related('facility').get(equipment_id=equipment_id)
            return self._to_entity(django_equipment)
        except DjangoEquipment.DoesNotExist:
            return None

    def get_by_inventory_code(self, inventory_code: str) -> Optional[Equipment]:
        """Retrieve equipment by its inventory code."""
        try:
            django_equipment = Equipment.objects.select_related('facility').get(inventory_code=inventory_code)
            return self._to_entity(django_equipment)
        except DjangoEquipment.DoesNotExist:
            return None

    def get_all(self) -> List[Equipment]:
        """Retrieve all equipment."""
        django_equipment = Equipment.objects.select_related('facility').all()
        return [self._to_entity(de) for de in django_equipment]

    def get_by_facility_id(self, facility_id: int) -> List[Equipment]:
        """Get equipment by facility ID."""
        django_equipment = DjangoEquipment.objects.select_related('facility').filter(facility_id=facility_id)
        return [self._to_entity(de) for de in django_equipment]

    def exists_by_inventory_code(self, inventory_code: str, exclude_id: Optional[int] = None) -> bool:
        """Check if equipment with given inventory code exists."""
        queryset = DjangoEquipment.objects.filter(inventory_code=inventory_code)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return queryset.exists()

    def get_all_inventory_codes(self, exclude_id: Optional[int] = None) -> List[str]:
        """Get all inventory codes for uniqueness validation."""
        queryset = Equipment.objects.all()
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return list(queryset.values_list('inventory_code', flat=True))

    def is_referenced_by_active_project(self, equipment_id: int) -> bool:
        """Check if equipment is referenced by any active project."""
        # This would need to be implemented based on how projects reference equipment
        # For now, return False as we don't have this relationship defined
        # In a real implementation, you might have a ProjectEquipment model
        return False

    def delete(self, equipment_id: int) -> bool:
        """Delete equipment by ID."""
        try:
            # Validate delete guard
            Equipment.validate_delete_guard(self.is_referenced_by_active_project(equipment_id))
            
            django_equipment = Equipment.objects.get(id=equipment_id)
            django_equipment.delete()
            return True
        except (Equipment.DoesNotExist, ValueError):
            return False

    def update(self, equipment: Equipment) -> Equipment:
        """Update an existing equipment."""
        if not equipment.id:
            raise ValueError("Equipment ID is required for update")
        
        # Validate business rules
        existing_codes = self.get_all_inventory_codes(exclude_id=equipment.id)
        Equipment.validate_uniqueness(equipment.inventory_code, existing_codes)
        
        try:
            django_equipment = Equipment.objects.get(id=equipment.id)
            django_equipment = self._to_django_model(equipment, django_equipment)
            django_equipment.save()
            return self._to_entity(django_equipment)
        except DjangoEquipment.DoesNotExist:
            raise ValueError(f"Equipment with ID {equipment.id} not found")

    def search(self, query: str) -> List[Equipment]:
        """Search equipment by query string."""
        django_equipment = Equipment.objects.select_related('facility').filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(capabilities__icontains=query) |
            Q(inventory_code__icontains=query) |
            Q(usage_domain__icontains=query)
        )
        return [self._to_entity(de) for de in django_equipment]

    def get_by_capability(self, capability: str) -> List[Equipment]:
        """Get equipment that has a specific capability."""
        django_equipment = Equipment.objects.select_related('facility').filter(capabilities__icontains=capability)
        return [self._to_entity(de) for de in django_equipment]

    def get_by_usage_domain(self, domain: str) -> List[Equipment]:
        """Get equipment by usage domain."""
        django_equipment = Equipment.objects.select_related('facility').filter(usage_domain__icontains=domain)
        return [self._to_entity(de) for de in django_equipment]

    def get_by_support_phase(self, phase: str) -> List[Equipment]:
        """Get equipment by support phase."""
        django_equipment = Equipment.objects.select_related('facility').filter(support_phase__icontains=phase)
        return [self._to_entity(de) for de in django_equipment]

    def get_electronics_equipment(self) -> List[Equipment]:
        """Get all electronics equipment."""
        django_equipment = Equipment.objects.select_related('facility').filter(usage_domain__icontains='Electronics')
        return [self._to_entity(de) for de in django_equipment]

    def get_equipment_for_project_requirements(self, capabilities: List[str], domains: List[str]) -> List[Equipment]:
        """Get equipment that can support project requirements."""
        # Build query for capabilities
        capability_q = Q()
        for capability in capabilities:
            capability_q |= Q(capabilities__icontains=capability)
        
        # Build query for domains
        domain_q = Q()
        for domain in domains:
            domain_q |= Q(usage_domain__icontains=domain)
        
        django_equipment = DjangoEquipment.objects.select_related('facility').filter(capability_q & domain_q)
        return [self._to_entity(de) for de in django_equipment]