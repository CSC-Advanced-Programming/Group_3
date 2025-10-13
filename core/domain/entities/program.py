"""
Program domain entity - Core business logic for Programs.
"""
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class Program:
    """
    Program entity representing an innovation program.
    Contains pure business logic without any framework dependencies.
    """
    id: Optional[int] = None
    program_id: Optional[str] = None
    name: str = ""
    description: str = ""
    national_alignment: Optional[str] = None
    focus_areas: str = ""
    phases: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validate program data after initialization."""
        self._validate()

    def _validate(self):
        """Validate program business rules."""
        # Required Fields Rule
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Program.Name is required.")
        
        if not self.description or len(self.description.strip()) == 0:
            raise ValueError("Program.Description is required.")
        
        # National Alignment Rule
        if self.focus_areas and self.focus_areas.strip():
            valid_alignments = ['NDPIII', 'DigitalRoadmap2023_2028', '4IR']
            if not self.national_alignment or not any(alignment in self.national_alignment for alignment in valid_alignments):
                raise ValueError("Program.NationalAlignment must include at least one recognized alignment when FocusAreas are specified.")

    @classmethod
    def validate_uniqueness(cls, name: str, existing_names: List[str]) -> None:
        """Validate program name uniqueness (case-insensitive)."""
        if any(existing_name.lower() == name.lower() for existing_name in existing_names):
            raise ValueError("Program.Name already exists.")

    @classmethod
    def validate_lifecycle_protection(cls, has_projects: bool) -> None:
        """Validate that program can be deleted (lifecycle protection)."""
        if has_projects:
            raise ValueError("Program has Projects; archive or reassign before delete.")

    @property
    def focus_areas_list(self) -> List[str]:
        """Convert comma-separated focus areas to list."""
        if not self.focus_areas:
            return []
        return [area.strip() for area in self.focus_areas.split(',') if area.strip()]

    @property
    def phases_list(self) -> List[str]:
        """Convert comma-separated phases to list."""
        if not self.phases:
            return []
        return [phase.strip() for phase in self.phases.split(',') if phase.strip()]

    def has_focus_areas(self) -> bool:
        """Check if program has any focus areas defined."""
        return bool(self.focus_areas and self.focus_areas.strip())

    def is_aligned_with_national_framework(self) -> bool:
        """Check if program is properly aligned with national frameworks."""
        if not self.has_focus_areas():
            return True  # No alignment required if no focus areas
        
        valid_alignments = ['NDPIII', 'DigitalRoadmap2023_2028', '4IR']
        return self.national_alignment and any(alignment in self.national_alignment for alignment in valid_alignments)

    def add_focus_area(self, focus_area: str) -> None:
        """Add a new focus area to the program."""
        if not focus_area or not focus_area.strip():
            raise ValueError("Focus area cannot be empty")
        
        current_areas = self.focus_areas_list
        if focus_area not in current_areas:
            current_areas.append(focus_area.strip())
            self.focus_areas = ', '.join(current_areas)
            # Re-validate national alignment requirement
            self._validate()

    def remove_focus_area(self, focus_area: str) -> None:
        """Remove a focus area from the program."""
        current_areas = self.focus_areas_list
        if focus_area in current_areas:
            current_areas.remove(focus_area)
            self.focus_areas = ', '.join(current_areas)

    def has_focus_area(self, focus_area: str) -> bool:
        """Check if program has a specific focus area."""
        return focus_area in self.focus_areas_list

    def is_aligned_with(self, alignment: str) -> bool:
        """Check if program is aligned with specific national goal."""
        return self.national_alignment and alignment in self.national_alignment

    def __str__(self) -> str:
        return self.name