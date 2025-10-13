"""
Participant domain entity - Core business logic for Participants.
"""
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
import re


@dataclass
class Participant:
    """
    Participant entity representing project participants.
    Contains pure business logic without any framework dependencies.
    """
    id: Optional[int] = None
    participant_id: Optional[str] = None
    full_name: str = ""
    email: str = ""
    affiliation: str = ""
    specialization: str = ""
    cross_skill_trained: bool = False
    institution: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate participant data after initialization."""
        self._validate()

    def _validate(self):
        """Validate participant business rules."""
        # Required Fields Rule
        if not self.full_name or len(self.full_name.strip()) == 0:
            raise ValueError("Participant.FullName, Participant.Email, and Participant.Affiliation are required.")
        
        if not self.email or len(self.email.strip()) == 0:
            raise ValueError("Participant.FullName, Participant.Email, and Participant.Affiliation are required.")
        
        if not self.affiliation or len(self.affiliation.strip()) == 0:
            raise ValueError("Participant.FullName, Participant.Email, and Participant.Affiliation are required.")
        
        if not self._is_valid_email(self.email):
            raise ValueError("Participant email format is invalid")
        
        # Specialization Requirement Rule
        if self.cross_skill_trained and (not self.specialization or not self.specialization.strip()):
            raise ValueError("Cross-skill flag requires Specialization.")

    @classmethod
    def validate_email_uniqueness(cls, email: str, existing_emails: List[str]) -> None:
        """Validate email uniqueness (case-insensitive)."""
        if any(existing_email.lower() == email.lower() for existing_email in existing_emails):
            raise ValueError("Participant.Email already exists.")

    def _is_valid_email(self, email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @property
    def first_name(self) -> str:
        """Extract first name from full name."""
        return self.full_name.split()[0] if self.full_name else ""

    @property
    def last_name(self) -> str:
        """Extract last name from full name."""
        name_parts = self.full_name.split()
        return name_parts[-1] if len(name_parts) > 1 else ""

    def is_affiliated_with(self, affiliation: str) -> bool:
        """Check if participant is affiliated with a specific group."""
        return self.affiliation.lower() == affiliation.lower()

    def has_specialization(self, specialization: str) -> bool:
        """Check if participant has a specific specialization."""
        return self.specialization.lower() == specialization.lower()

    def is_from_institution(self, institution: str) -> bool:
        """Check if participant is from a specific institution."""
        return self.institution.lower() == institution.lower()

    def is_cross_skill_trained(self) -> bool:
        """Check if participant has received cross-skill training."""
        return self.cross_skill_trained

    def mark_as_cross_skill_trained(self) -> None:
        """Mark participant as having received cross-skill training."""
        if not self.specialization or not self.specialization.strip():
            raise ValueError("Cross-skill flag requires Specialization.")
        self.cross_skill_trained = True

    def can_be_cross_skill_trained(self) -> bool:
        """Check if participant can be marked as cross-skill trained."""
        return bool(self.specialization and self.specialization.strip())

    def has_valid_cross_skill_status(self) -> bool:
        """Check if cross-skill status is valid according to business rules."""
        if not self.cross_skill_trained:
            return True  # If not cross-skilled, no specialization requirement
        return bool(self.specialization and self.specialization.strip())

    def can_contribute_to_project(self, required_specialization: str) -> bool:
        """Check if participant can contribute to a project requiring specific skills."""
        # Direct specialization match
        if self.has_specialization(required_specialization):
            return True
        
        # Cross-skilled participants can contribute to multiple areas
        if self.cross_skill_trained:
            return True
        
        return False

    def get_participant_profile(self) -> str:
        """Get a summary profile of the participant."""
        cross_skilled = "Cross-skilled" if self.cross_skill_trained else "Specialized"
        return f"{self.full_name} - {self.specialization} ({cross_skilled}) from {self.institution}"

    def has_technical_background(self) -> bool:
        """Check if participant has technical background."""
        technical_specializations = ['software', 'hardware', 'engineering']
        technical_affiliations = ['cs', 'se', 'engineering']
        
        return (any(spec in self.specialization.lower() for spec in technical_specializations) or
                any(aff in self.affiliation.lower() for aff in technical_affiliations))

    def has_business_background(self) -> bool:
        """Check if participant has business background."""
        return 'business' in self.specialization.lower()

    def matches_search_criteria(self, search_term: str) -> bool:
        """Check if participant matches search criteria."""
        search_term = search_term.lower()
        return (search_term in self.full_name.lower() or 
                search_term in self.email.lower() or
                search_term in self.affiliation.lower() or
                search_term in self.specialization.lower() or
                search_term in self.institution.lower())

    def update_email(self, new_email: str) -> None:
        """Update participant email with validation."""
        if not self._is_valid_email(new_email):
            raise ValueError("Invalid email format")
        self.email = new_email

    def __str__(self) -> str:
        return self.full_name