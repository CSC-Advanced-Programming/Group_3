"""
Repository interface for Project entity.
Defines the contract for Project data access operations.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.project import Project


class ProjectRepositoryInterface(ABC):
    """
    Abstract interface for Project repository operations.
    Infrastructure layer must implement these methods.
    """

    @abstractmethod
    def save(self, project: Project) -> Project:
        """
        Save a project entity.
        
        Args:
            project: Project entity to save
            
        Returns:
            Project: Saved project with updated ID
            
        Raises:
            ValueError: If business rules are violated
        """
        pass

    @abstractmethod
    def get_by_id(self, project_id: int) -> Optional[Project]:
        """
        Retrieve a project by its ID.
        
        Args:
            project_id: Unique identifier of the project
            
        Returns:
            Project or None if not found
        """
        pass

    @abstractmethod
    def get_by_project_id(self, project_id: str) -> Optional[Project]:
        """
        Retrieve a project by its project_id field.
        
        Args:
            project_id: Project identifier (e.g., 'PR-001')
            
        Returns:
            Project or None if not found
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Project]:
        """
        Retrieve all projects.
        
        Returns:
            List of all projects
        """
        pass

    @abstractmethod
    def get_by_program_id(self, program_id: int) -> List[Project]:
        """
        Get projects by program ID.
        
        Args:
            program_id: Program ID to filter by
            
        Returns:
            List of projects in specified program
        """
        pass

    @abstractmethod
    def get_by_facility_id(self, facility_id: int) -> List[Project]:
        """
        Get projects by facility ID.
        
        Args:
            facility_id: Facility ID to filter by
            
        Returns:
            List of projects at specified facility
        """
        pass

    @abstractmethod
    def exists_by_title_in_program(self, title: str, program_id: int, exclude_id: Optional[int] = None) -> bool:
        """
        Check if a project with given title exists in a program.
        
        Args:
            title: Project title
            program_id: Program ID to check within
            exclude_id: Optional ID to exclude from check (for updates)
            
        Returns:
            True if project with title exists in program, False otherwise
        """
        pass

    @abstractmethod
    def get_all_titles_in_program(self, program_id: int, exclude_id: Optional[int] = None) -> List[str]:
        """
        Get all project titles in a program for uniqueness validation.
        
        Args:
            program_id: Program ID to get titles from
            exclude_id: Optional ID to exclude (for updates)
            
        Returns:
            List of project titles in the program
        """
        pass

    @abstractmethod
    def has_team_members(self, project_id: int) -> bool:
        """
        Check if project has team members assigned.
        
        Args:
            project_id: Project ID to check
            
        Returns:
            True if project has team members, False otherwise
        """
        pass

    @abstractmethod
    def has_outcomes(self, project_id: int) -> bool:
        """
        Check if project has outcomes.
        
        Args:
            project_id: Project ID to check
            
        Returns:
            True if project has outcomes, False otherwise
        """
        pass

    @abstractmethod
    def get_facility_capabilities(self, facility_id: int) -> List[str]:
        """
        Get capabilities of a facility for compatibility checking.
        
        Args:
            facility_id: Facility ID
            
        Returns:
            List of facility capabilities
        """
        pass

    @abstractmethod
    def delete(self, project_id: int) -> bool:
        """
        Delete a project by ID.
        
        Args:
            project_id: ID of project to delete
            
        Returns:
            True if deletion successful, False otherwise
        """
        pass

    @abstractmethod
    def update(self, project: Project) -> Project:
        """
        Update an existing project.
        
        Args:
            project: Project entity with updated data
            
        Returns:
            Updated project entity
            
        Raises:
            ValueError: If business rules are violated
        """
        pass

    @abstractmethod
    def search(self, query: str) -> List[Project]:
        """
        Search projects by query string.
        
        Args:
            query: Search query
            
        Returns:
            List of matching projects
        """
        pass

    @abstractmethod
    def get_by_nature(self, nature: str) -> List[Project]:
        """
        Get projects by nature.
        
        Args:
            nature: Project nature to filter by
            
        Returns:
            List of projects of specified nature
        """
        pass

    @abstractmethod
    def get_by_prototype_stage(self, stage: str) -> List[Project]:
        """
        Get projects by prototype stage.
        
        Args:
            stage: Prototype stage to filter by
            
        Returns:
            List of projects at specified stage
        """
        pass

    @abstractmethod
    def get_by_innovation_focus(self, focus: str) -> List[Project]:
        """
        Get projects by innovation focus.
        
        Args:
            focus: Innovation focus to filter by
            
        Returns:
            List of projects with specified focus
        """
        pass

    @abstractmethod
    def get_completed_projects(self) -> List[Project]:
        """
        Get all completed projects.
        
        Returns:
            List of completed projects
        """
        pass

    @abstractmethod
    def get_active_projects(self) -> List[Project]:
        """
        Get all active (non-completed) projects.
        
        Returns:
            List of active projects
        """
        pass