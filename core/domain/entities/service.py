"""
Service domain entity - Core business logic for Services.
"""
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class Service:
    """
    Service entity representing facility services.
    Contains pure business logic without any framework dependencies.
    """
    id: Optional[int] = None
    service_id: Optional[str] = None
    facility_id: Optional[int] = None
    name: str = ""
    description: str = ""
    category: str = ""
    skill_type: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate service data after initialization."""
        self._validate()

    def _validate(self):
        """Validate service business rules."""
        # Required Fields Rule
        if not self.facility_id:
            raise ValueError("Service.FacilityId, Service.Name, Service.Category, and Service.SkillType are required.")
        
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Service.FacilityId, Service.Name, Service.Category, and Service.SkillType are required.")
        
        if not self.description or len(self.description.strip()) == 0:
            raise ValueError("Service.FacilityId, Service.Name, Service.Category, and Service.SkillType are required.")
        
        if not self.category or len(self.category.strip()) == 0:
            raise ValueError("Service.FacilityId, Service.Name, Service.Category, and Service.SkillType are required.")
        
        if not self.skill_type or len(self.skill_type.strip()) == 0:
            raise ValueError("Service.FacilityId, Service.Name, Service.Category, and Service.SkillType are required.")

    @classmethod
    def validate_scoped_uniqueness(cls, name: str, facility_id: int, existing_names_in_facility: List[str]) -> None:
        """Validate service name uniqueness within a facility."""
        if name in existing_names_in_facility:
            raise ValueError("A service with this name already exists in this facility.")

    @classmethod
    def validate_delete_guard(cls, is_used_by_project_testing: bool) -> None:
        """Validate that service can be deleted (not used by project testing requirements)."""
        if is_used_by_project_testing:
            raise ValueError("Service in use by Project testing requirements.")

    def is_category(self, category: str) -> bool:
        """Check if service belongs to a specific category."""
        return self.category.lower() == category.lower()

    def is_skill_type(self, skill_type: str) -> bool:
        """Check if service is of a specific skill type."""
        return self.skill_type.lower() == skill_type.lower()

    def is_provided_by_facility(self, facility_id: int) -> bool:
        """Check if service is provided by a specific facility."""
        return self.facility_id == facility_id

    def can_support_skill_development(self, required_skill: str) -> bool:
        """Check if service can support development of a specific skill."""
        return required_skill.lower() in self.skill_type.lower() or required_skill.lower() in self.category.lower()

    def is_relevant_for_project_phase(self, phase: str) -> bool:
        """Check if service is relevant for a specific project phase."""
        # Define service relevance based on category and phase
        phase_service_mapping = {
            'cross-skilling': ['training', 'skill development', 'workshop'],
            'collaboration': ['mentoring', 'consulting', 'collaboration'],
            'technical skills': ['technical training', 'skill development', 'workshop'],
            'prototyping': ['fabrication', 'development', 'design'],
            'commercialization': ['business', 'marketing', 'consulting']
        }
        
        phase_lower = phase.lower()
        if phase_lower in phase_service_mapping:
            relevant_categories = phase_service_mapping[phase_lower]
            return any(cat in self.category.lower() for cat in relevant_categories)
        
        return False

    def matches_search_criteria(self, search_term: str) -> bool:
        """Check if service matches search criteria."""
        search_term = search_term.lower()
        return (search_term in self.name.lower() or 
                search_term in self.description.lower() or
                search_term in self.category.lower() or
                search_term in self.skill_type.lower())

    def get_service_summary(self) -> str:
        """Get a summary of the service."""
        return f"{self.name} - {self.category} ({self.skill_type})"

    def __str__(self) -> str:
        return self.name