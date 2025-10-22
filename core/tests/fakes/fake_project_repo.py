"""
Fake repository and pytest fixture for Project domain tests.
"""

import pytest
from typing import List, Dict, Optional
from core.domain.entities.project import Project
from core.application.interfaces.project_repository import ProjectRepositoryInterface


class FakeProjectRepository(ProjectRepositoryInterface):
    """
    A fake repository for projects that stores data in-memory.
    Simulates database constraints and behaviors for testing purposes.
    """

    def __init__(self) -> None:
        self._projects: Dict[int, Project] = {}
        self._next_id = 1
        self._team_members: Dict[int, List[str]] = {}  # project_id -> list of team member names
        self._outcomes: Dict[int, List[str]] = {}  # project_id -> list of outcome titles
        self._facility_capabilities: Dict[int, List[str]] = {}  # facility_id -> capabilities

    def save(self, project: Project) -> Project:
        is_update = project.id is not None
        
        # Intrinsic validation is handled by the entity's __post_init__
        project._validate()

        # Required Associations validation (already done in entity __post_init__)
        
        # Name uniqueness validation within program
        if project.program_id is not None and self.exists_by_title_in_program(project.title, project.program_id, project.id if is_update else None):
            raise ValueError("A project with this name already exists in this program.")

        if not is_update:
            project.id = self._next_id
            self._next_id += 1
            # Initialize empty team and outcomes for new projects
            self._team_members[project.id] = []
            self._outcomes[project.id] = []
        
        if project.id is not None:
            self._projects[project.id] = project
        return project

    def update(self, project: Project) -> Project:
        if project.id is None or project.id not in self._projects:
            raise ValueError("Project not found for update.")
        return self.save(project)

    def get_by_id(self, project_id: int) -> Optional[Project]:
        return self._projects.get(project_id)

    def get_by_project_id(self, project_id: str) -> Optional[Project]:
        for project in self._projects.values():
            if project.project_id == project_id:
                return project
        return None

    def get_all(self) -> List[Project]:
        return list(self._projects.values())

    def get_by_program_id(self, program_id: int) -> List[Project]:
        return [p for p in self._projects.values() if p.program_id == program_id]

    def get_by_facility_id(self, facility_id: int) -> List[Project]:
        return [p for p in self._projects.values() if p.facility_id == facility_id]

    def exists_by_title_in_program(self, title: str, program_id: int, exclude_id: Optional[int] = None) -> bool:
        for p_id, project in self._projects.items():
            if p_id == exclude_id:
                continue
            if project.title == title and project.program_id == program_id:
                return True
        return False

    def get_all_titles_in_program(self, program_id: int, exclude_id: Optional[int] = None) -> List[str]:
        titles = []
        for p_id, project in self._projects.items():
            if p_id == exclude_id:
                continue
            if project.program_id == program_id:
                titles.append(project.title)
        return titles

    def has_team_members(self, project_id: int) -> bool:
        return len(self._team_members.get(project_id, [])) > 0

    def has_outcomes(self, project_id: int) -> bool:
        return len(self._outcomes.get(project_id, [])) > 0

    def get_facility_capabilities(self, facility_id: int) -> List[str]:
        return self._facility_capabilities.get(facility_id, [])

    def delete(self, project_id: int) -> bool:
        if project_id not in self._projects:
            return False
        del self._projects[project_id]
        # Clean up related data
        self._team_members.pop(project_id, None)
        self._outcomes.pop(project_id, None)
        return True

    # Test helper methods
    def add_team_member(self, project_id: int, member_name: str):
        """Add a team member to a project for testing purposes."""
        if project_id not in self._team_members:
            self._team_members[project_id] = []
        self._team_members[project_id].append(member_name)

    def add_outcome(self, project_id: int, outcome_title: str):
        """Add an outcome to a project for testing purposes."""
        if project_id not in self._outcomes:
            self._outcomes[project_id] = []
        self._outcomes[project_id].append(outcome_title)

    def set_facility_capabilities(self, facility_id: int, capabilities: List[str]):
        """Set facility capabilities for testing purposes."""
        self._facility_capabilities[facility_id] = capabilities

    def validate_team_tracking_for_project(self, project_id: int):
        """Validate team tracking rule for a specific project."""
        Project.validate_team_tracking(self.has_team_members(project_id))

    def validate_outcome_validation_for_project(self, project_id: int, status: str):
        """Validate outcome validation rule for a specific project."""
        Project.validate_outcome_validation(status, self.has_outcomes(project_id))

    def validate_name_uniqueness_for_project(self, project: Project):
        """Validate name uniqueness rule for a project."""
        if project.program_id is not None:
            existing_titles = self.get_all_titles_in_program(project.program_id, project.id)
            Project.validate_name_uniqueness(project.title, project.program_id, existing_titles)

    def validate_facility_compatibility_for_project(self, project: Project):
        """Validate facility compatibility rule for a project."""
        if project.facility_id is not None:
            facility_capabilities = self.get_facility_capabilities(project.facility_id)
            project_requirements = project.get_technical_requirements()
            Project.validate_facility_compatibility(project_requirements, facility_capabilities)

    # --- Unused abstract methods (simple implementations for completeness) ---
    def search(self, query: str) -> List[Project]:
        return [p for p in self._projects.values() if query.lower() in p.title.lower()]

    def get_by_nature(self, nature: str) -> List[Project]:
        return [p for p in self._projects.values() if p.nature_of_project == nature]

    def get_by_prototype_stage(self, stage: str) -> List[Project]:
        return [p for p in self._projects.values() if p.prototype_stage == stage]

    def get_by_innovation_focus(self, focus: str) -> List[Project]:
        return [p for p in self._projects.values() if focus in p.innovation_focus_list]

    def get_completed_projects(self) -> List[Project]:
        return [p for p in self._projects.values() if hasattr(p, 'status') and getattr(p, 'status', '').lower() == 'completed']

    def get_active_projects(self) -> List[Project]:
        return [p for p in self._projects.values() if not (hasattr(p, 'status') and getattr(p, 'status', '').lower() == 'completed')]


@pytest.fixture
def fake_project_repo() -> FakeProjectRepository:
    """Provides a fresh instance of the fake project repository for each test."""
    return FakeProjectRepository()