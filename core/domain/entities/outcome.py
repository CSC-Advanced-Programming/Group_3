"""
Outcome domain entity - Core business logic for Project Outcomes.
"""
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
import re


@dataclass
class Outcome:
    """
    Outcome entity representing project outcomes/deliverables.
    Contains pure business logic without any framework dependencies.
    """
    id: Optional[int] = None
    outcome_id: Optional[str] = None
    project_id: Optional[int] = None
    title: str = ""
    description: str = ""
    artifact_link: Optional[str] = None
    outcome_type: str = ""
    quality_certification: Optional[str] = None
    commercialization_status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate outcome data after initialization."""
        self._validate()

    def _validate(self):
        """Validate outcome business rules."""
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Outcome title cannot be empty")
        
        if len(self.title) > 200:
            raise ValueError("Outcome title cannot exceed 200 characters")
        
        if not self.description or len(self.description.strip()) == 0:
            raise ValueError("Outcome description cannot be empty")
        
        if not self.outcome_type or len(self.outcome_type.strip()) == 0:
            raise ValueError("Outcome type cannot be empty")
        
        if self.artifact_link and not self._is_valid_url(self.artifact_link):
            raise ValueError("Artifact link must be a valid URL")

    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format."""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None

    def is_type(self, outcome_type: str) -> bool:
        """Check if outcome is of a specific type."""
        return self.outcome_type.lower() == outcome_type.lower()

    def belongs_to_project(self, project_id: int) -> bool:
        """Check if outcome belongs to a specific project."""
        return self.project_id == project_id

    def has_artifact(self) -> bool:
        """Check if outcome has an associated artifact link."""
        return bool(self.artifact_link and self.artifact_link.strip())

    def is_certified(self) -> bool:
        """Check if outcome has quality certification."""
        return bool(self.quality_certification and self.quality_certification.strip())

    def has_commercialization_status(self) -> bool:
        """Check if outcome has commercialization status."""
        return bool(self.commercialization_status and self.commercialization_status.strip())

    def is_commercialization_status(self, status: str) -> bool:
        """Check if outcome has a specific commercialization status."""
        return self.commercialization_status and self.commercialization_status.lower() == status.lower()

    def is_demoed(self) -> bool:
        """Check if outcome has been demoed."""
        return self.is_commercialization_status('demoed')

    def is_market_linked(self) -> bool:
        """Check if outcome is market linked."""
        return self.is_commercialization_status('market linked')

    def is_launched(self) -> bool:
        """Check if outcome has been launched."""
        return self.is_commercialization_status('launched')

    def is_ready_for_commercialization(self) -> bool:
        """Check if outcome is ready for commercialization."""
        # Business logic: outcome needs to be certified and have certain types
        commercial_types = ['prototype', 'business plan', 'pcb']
        return (self.is_certified() and 
                any(self.is_type(otype) for otype in commercial_types))

    def update_commercialization_status(self, new_status: str) -> None:
        """Update commercialization status with validation."""
        valid_statuses = ['demoed', 'market linked', 'launched']
        if new_status.lower() not in valid_statuses:
            raise ValueError(f"Invalid commercialization status. Must be one of: {', '.join(valid_statuses)}")
        self.commercialization_status = new_status

    def add_quality_certification(self, certification: str) -> None:
        """Add quality certification to the outcome."""
        if not certification or not certification.strip():
            raise ValueError("Certification cannot be empty")
        self.quality_certification = certification.strip()

    def update_artifact_link(self, new_link: str) -> None:
        """Update artifact link with validation."""
        if new_link and not self._is_valid_url(new_link):
            raise ValueError("Artifact link must be a valid URL")
        self.artifact_link = new_link

    def get_outcome_summary(self) -> str:
        """Get a summary of the outcome."""
        status = f" - {self.commercialization_status}" if self.commercialization_status else ""
        certification = " (Certified)" if self.is_certified() else ""
        return f"{self.title} [{self.outcome_type}]{status}{certification}"

    def is_tangible_deliverable(self) -> bool:
        """Check if outcome is a tangible deliverable."""
        tangible_types = ['cad', 'pcb', 'prototype']
        return any(self.is_type(otype) for otype in tangible_types)

    def is_documentation(self) -> bool:
        """Check if outcome is documentation."""
        doc_types = ['report', 'business plan']
        return any(self.is_type(otype) for otype in doc_types)

    def matches_search_criteria(self, search_term: str) -> bool:
        """Check if outcome matches search criteria."""
        search_term = search_term.lower()
        return (search_term in self.title.lower() or 
                search_term in self.description.lower() or
                search_term in self.outcome_type.lower() or
                (self.quality_certification and search_term in self.quality_certification.lower()) or
                (self.commercialization_status and search_term in self.commercialization_status.lower()))

    def __str__(self) -> str:
        return self.title