"""
Facility domain entity - Core business logic for Facilities.
"""
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class Facility:
    """
    Facility entity representing a research/innovation facility.
    Contains pure business logic without any framework dependencies.
    """
    id: Optional[int] = None
    facility_id: Optional[str] = None
    name: str = ""
    location: str = ""
    description: str = ""
    partner_organization: Optional[str] = None
    facility_type: str = ""
    capabilities: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate facility data after initialization."""
        self._validate()

    def _validate(self):
        """Validate facility business rules."""
        # Required Fields Rule
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Facility.Name, Facility.Location, and Facility.FacilityType are required.")
        
        if not self.location or len(self.location.strip()) == 0:
            raise ValueError("Facility.Name, Facility.Location, and Facility.FacilityType are required.")
        
        if not self.facility_type or len(self.facility_type.strip()) == 0:
            raise ValueError("Facility.Name, Facility.Location, and Facility.FacilityType are required.")

    @classmethod
    def validate_uniqueness(cls, name: str, location: str, existing_combinations: List[tuple]) -> None:
        """Validate name-location combination uniqueness."""
        name_location = (name.strip(), location.strip())
        if name_location in existing_combinations:
            raise ValueError("A facility with this name already exists at this location.")

    @classmethod
    def validate_deletion_constraints(cls, has_services: bool, has_equipment: bool, has_projects: bool) -> None:
        """Validate that facility can be deleted (no dependent records)."""
        if has_services or has_equipment or has_projects:
            raise ValueError("Facility has dependent records (Services/Equipment/Projects).")

    def validate_capabilities_requirement(self, has_services: bool, has_equipment: bool) -> None:
        """Validate capabilities requirement when services or equipment exist."""
        if (has_services or has_equipment) and not self.has_capabilities():
            raise ValueError("Facility.Capabilities must be populated when Services/Equipment exist.")

    def has_capabilities(self) -> bool:
        """Check if facility has any capabilities defined."""
        return bool(self.capabilities and self.capabilities.strip())

    @property
    def capabilities_list(self) -> List[str]:
        """Convert comma-separated capabilities to list."""
        if not self.capabilities:
            return []
        return [cap.strip() for cap in self.capabilities.split(',') if cap.strip()]

    def add_capability(self, capability: str) -> None:
        """Add a new capability to the facility."""
        if not capability or not capability.strip():
            raise ValueError("Capability cannot be empty")
        
        current_capabilities = self.capabilities_list
        if capability not in current_capabilities:
            current_capabilities.append(capability.strip())
            self.capabilities = ', '.join(current_capabilities)

    def remove_capability(self, capability: str) -> None:
        """Remove a capability from the facility."""
        current_capabilities = self.capabilities_list
        if capability in current_capabilities:
            current_capabilities.remove(capability)
            self.capabilities = ', '.join(current_capabilities)

    def has_capability(self, capability: str) -> bool:
        """Check if facility has a specific capability."""
        return capability in self.capabilities_list

    def is_type(self, facility_type: str) -> bool:
        """Check if facility is of a specific type."""
        return self.facility_type.lower() == facility_type.lower()

    def is_operated_by(self, organization: str) -> bool:
        """Check if facility is operated by a specific organization."""
        return self.partner_organization == organization

    def can_support_project(self, required_capabilities: List[str]) -> bool:
        """Check if facility can support a project with required capabilities."""
        facility_capabilities = self.capabilities_list
        return all(cap in facility_capabilities for cap in required_capabilities)

    def __str__(self) -> str:
        return f"{self.name} ({self.location})"