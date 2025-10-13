"""
Project domain entity - Core business logic for Projects.
"""
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class Project:
    """
    Project entity representing an innovation project.
    Contains pure business logic without any framework dependencies.
    """
    id: Optional[int] = None
    project_id: Optional[str] = None
    program_id: Optional[int] = None
    facility_id: Optional[int] = None
    title: str = ""
    nature_of_project: str = ""
    description: str = ""
    innovation_focus: str = ""
    prototype_stage: str = ""
    testing_requirements: str = ""
    commercialization_plan: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate project data after initialization."""
        self._validate()

    def _validate(self):
        """Validate project business rules."""
        # Required Associations Rule
        if not self.program_id:
            raise ValueError("Project.ProgramId and Project.FacilityId are required.")
        
        if not self.facility_id:
            raise ValueError("Project.ProgramId and Project.FacilityId are required.")
        
        # Basic field validation
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Project title cannot be empty")
        
        if not self.description or len(self.description.strip()) == 0:
            raise ValueError("Project description cannot be empty")
        
        if not self.nature_of_project or len(self.nature_of_project.strip()) == 0:
            raise ValueError("Project nature cannot be empty")

    @classmethod
    def validate_team_tracking(cls, has_team_members: bool) -> None:
        """Validate that project has at least one team member."""
        if not has_team_members:
            raise ValueError("Project must have at least one team member assigned.")

    @classmethod
    def validate_outcome_validation(cls, status: str, has_outcomes: bool) -> None:
        """Validate outcome requirement for completed projects."""
        if status.lower() == 'completed' and not has_outcomes:
            raise ValueError("Completed projects must have at least one documented outcome.")

    @classmethod
    def validate_name_uniqueness(cls, title: str, program_id: int, existing_titles_in_program: List[str]) -> None:
        """Validate project name uniqueness within a program."""
        if title in existing_titles_in_program:
            raise ValueError("A project with this name already exists in this program.")

    @classmethod
    def validate_facility_compatibility(cls, project_requirements: List[str], facility_capabilities: List[str]) -> None:
        """Validate that project requirements are compatible with facility capabilities."""
        if not all(req in facility_capabilities for req in project_requirements):
            raise ValueError("Project requirements not compatible with facility capabilities.")

    @property
    def innovation_focus_list(self) -> List[str]:
        """Convert comma-separated innovation focuses to list."""
        if not self.innovation_focus:
            return []
        return [focus.strip() for focus in self.innovation_focus.split(',') if focus.strip()]

    def is_prototype_stage(self, stage: str) -> bool:
        """Check if project is at a specific prototype stage."""
        return self.prototype_stage.lower() == stage.lower()

    def is_nature_of(self, nature: str) -> bool:
        """Check if project is of a specific nature."""
        return self.nature_of_project.lower() == nature.lower()

    def has_innovation_focus(self, focus: str) -> bool:
        """Check if project has a specific innovation focus."""
        return focus in self.innovation_focus_list

    def add_innovation_focus(self, focus: str) -> None:
        """Add a new innovation focus to the project."""
        if not focus or not focus.strip():
            raise ValueError("Innovation focus cannot be empty")
        
        current_focuses = self.innovation_focus_list
        if focus not in current_focuses:
            current_focuses.append(focus.strip())
            self.innovation_focus = ', '.join(current_focuses)

    def remove_innovation_focus(self, focus: str) -> None:
        """Remove an innovation focus from the project."""
        current_focuses = self.innovation_focus_list
        if focus in current_focuses:
            current_focuses.remove(focus)
            self.innovation_focus = ', '.join(current_focuses)

    def is_assigned_to_program(self, program_id: int) -> bool:
        """Check if project is assigned to a specific program."""
        return self.program_id == program_id

    def is_assigned_to_facility(self, facility_id: int) -> bool:
        """Check if project is assigned to a specific facility."""
        return self.facility_id == facility_id

    def has_testing_requirements(self) -> bool:
        """Check if project has testing requirements."""
        return bool(self.testing_requirements and self.testing_requirements.strip())

    def has_commercialization_plan(self) -> bool:
        """Check if project has a commercialization plan."""
        return bool(self.commercialization_plan and self.commercialization_plan.strip())

    def has_required_associations(self) -> bool:
        """Check if project has required program and facility associations."""
        return self.program_id is not None and self.facility_id is not None

    def is_completed(self) -> bool:
        """Check if project is completed."""
        return hasattr(self, 'status') and getattr(self, 'status', '').lower() == 'completed'

    def requires_outcomes(self) -> bool:
        """Check if project requires outcomes (when completed)."""
        return self.is_completed()

    def has_compatible_facility(self, facility_capabilities: List[str]) -> bool:
        """Check if project is compatible with facility capabilities."""
        project_requirements = self.get_technical_requirements()
        return all(req in facility_capabilities for req in project_requirements)

    def get_technical_requirements(self) -> List[str]:
        """Extract technical requirements from project."""
        requirements = []
        
        # Extract from innovation focus
        if self.innovation_focus:
            requirements.extend(self.innovation_focus_list)
        
        # Extract from testing requirements
        if self.testing_requirements:
            # Simple extraction - in real implementation this might be more sophisticated
            requirements.extend([req.strip() for req in self.testing_requirements.split(',') if req.strip()])
        
        return requirements

    def __str__(self) -> str:
        return self.title