"""
Equipment domain entity - Core business logic for Equipment.
"""
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class Equipment:
    """
    Equipment entity representing facility equipment.
    Contains pure business logic without any framework dependencies.
    """
    id: Optional[int] = None
    equipment_id: Optional[str] = None
    facility_id: Optional[int] = None
    name: str = ""
    capabilities: str = ""
    description: str = ""
    inventory_code: str = ""
    usage_domain: str = ""
    support_phase: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate equipment data after initialization."""
        self._validate()

    def _validate(self):
        """Validate equipment business rules."""
        # Required Fields Rule
        if not self.facility_id:
            raise ValueError("Equipment.FacilityId, Equipment.Name, and Equipment.InventoryCode are required.")
        
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Equipment.FacilityId, Equipment.Name, and Equipment.InventoryCode are required.")
        
        if not self.inventory_code or len(self.inventory_code.strip()) == 0:
            raise ValueError("Equipment.FacilityId, Equipment.Name, and Equipment.InventoryCode are required.")
        
        # Usage Domain - Support Phase Coherence Rule
        if self.usage_domain and 'Electronics' in self.usage_domain:
            if not self.support_phase or not any(phase in self.support_phase for phase in ['Prototyping', 'Testing']):
                raise ValueError("Electronics equipment must support Prototyping or Testing.")

    @classmethod
    def validate_uniqueness(cls, inventory_code: str, existing_codes: List[str]) -> None:
        """Validate inventory code uniqueness."""
        if inventory_code in existing_codes:
            raise ValueError("Equipment.InventoryCode already exists.")

    @classmethod
    def validate_delete_guard(cls, is_referenced_by_active_project: bool) -> None:
        """Validate that equipment can be deleted (not referenced by active projects)."""
        if is_referenced_by_active_project:
            raise ValueError("Equipment referenced by active Project.")

    @property
    def capabilities_list(self) -> List[str]:
        """Convert comma-separated capabilities to list."""
        if not self.capabilities:
            return []
        return [cap.strip() for cap in self.capabilities.split(',') if cap.strip()]

    @property
    def usage_domain_list(self) -> List[str]:
        """Convert comma-separated usage domains to list."""
        if not self.usage_domain:
            return []
        return [domain.strip() for domain in self.usage_domain.split(',') if domain.strip()]

    def has_capability(self, capability: str) -> bool:
        """Check if equipment has a specific capability."""
        return capability in self.capabilities_list

    def can_be_used_in_domain(self, domain: str) -> bool:
        """Check if equipment can be used in a specific domain."""
        return domain in self.usage_domain_list

    def supports_phase(self, phase: str) -> bool:
        """Check if equipment supports a specific project phase."""
        return self.support_phase.lower() == phase.lower()

    def is_in_facility(self, facility_id: int) -> bool:
        """Check if equipment belongs to a specific facility."""
        return self.facility_id == facility_id

    def add_capability(self, capability: str) -> None:
        """Add a new capability to the equipment."""
        if not capability or not capability.strip():
            raise ValueError("Capability cannot be empty")
        
        current_capabilities = self.capabilities_list
        if capability not in current_capabilities:
            current_capabilities.append(capability.strip())
            self.capabilities = ', '.join(current_capabilities)

    def remove_capability(self, capability: str) -> None:
        """Remove a capability from the equipment."""
        current_capabilities = self.capabilities_list
        if capability in current_capabilities:
            current_capabilities.remove(capability)
            self.capabilities = ', '.join(current_capabilities)

    def add_usage_domain(self, domain: str) -> None:
        """Add a new usage domain to the equipment."""
        if not domain or not domain.strip():
            raise ValueError("Usage domain cannot be empty")
        
        current_domains = self.usage_domain_list
        if domain not in current_domains:
            current_domains.append(domain.strip())
            self.usage_domain = ', '.join(current_domains)

    def remove_usage_domain(self, domain: str) -> None:
        """Remove a usage domain from the equipment."""
        current_domains = self.usage_domain_list
        if domain in current_domains:
            current_domains.remove(domain)
            self.usage_domain = ', '.join(current_domains)

    def supports_electronics_properly(self) -> bool:
        """Check if electronics equipment properly supports required phases."""
        if not self.usage_domain or 'Electronics' not in self.usage_domain:
            return True  # Rule doesn't apply to non-electronics equipment
        
        return self.support_phase and any(phase in self.support_phase for phase in ['Prototyping', 'Testing'])

    def can_be_used_for_electronics(self) -> bool:
        """Check if equipment can be used for electronics projects."""
        return 'Electronics' in self.usage_domain_list and self.supports_electronics_properly()

    def __str__(self) -> str:
        return f"{self.name} ({self.inventory_code})"