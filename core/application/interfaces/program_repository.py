"""
Repository interface for Program entity.
Defines the contract for Program data access operations.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.program import Program


class ProgramRepositoryInterface(ABC):
    """
    Abstract interface for Program repository operations.
    Infrastructure layer must implement these methods.
    """

    @abstractmethod
    def save(self, program: Program) -> Program:
        """
        Save a program entity.
        
        Args:
            program: Program entity to save
            
        Returns:
            Program: Saved program with updated ID
            
        Raises:
            ValueError: If business rules are violated
        """
        pass

    @abstractmethod
    def get_by_id(self, program_id: int) -> Optional[Program]:
        """
        Retrieve a program by its ID.
        
        Args:
            program_id: Unique identifier of the program
            
        Returns:
            Program or None if not found
        """
        pass

    @abstractmethod
    def get_by_program_id(self, program_id: str) -> Optional[Program]:
        """
        Retrieve a program by its program_id field.
        
        Args:
            program_id: Program identifier (e.g., 'Pg-001')
            
        Returns:
            Program or None if not found
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Program]:
        """
        Retrieve all programs.
        
        Returns:
            List of all programs
        """
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Program]:
        """
        Retrieve a program by its name.
        
        Args:
            name: Program name
            
        Returns:
            Program or None if not found
        """
        pass

    @abstractmethod
    def exists_by_name(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """
        Check if a program with given name exists.
        
        Args:
            name: Program name to check
            exclude_id: Optional ID to exclude from check (for updates)
            
        Returns:
            True if program with name exists, False otherwise
        """
        pass

    @abstractmethod
    def get_all_names(self, exclude_id: Optional[int] = None) -> List[str]:
        """
        Get all program names for uniqueness validation.
        
        Args:
            exclude_id: Optional ID to exclude (for updates)
            
        Returns:
            List of all program names
        """
        pass

    @abstractmethod
    def has_projects(self, program_id: int) -> bool:
        """
        Check if program has associated projects.
        
        Args:
            program_id: Program ID to check
            
        Returns:
            True if program has projects, False otherwise
        """
        pass

    @abstractmethod
    def delete(self, program_id: int) -> bool:
        """
        Delete a program by ID.
        
        Args:
            program_id: ID of program to delete
            
        Returns:
            True if deletion successful, False otherwise
            
        Raises:
            ValueError: If program has projects or other constraints violated
        """
        pass

    @abstractmethod
    def update(self, program: Program) -> Program:
        """
        Update an existing program.
        
        Args:
            program: Program entity with updated data
            
        Returns:
            Updated program entity
            
        Raises:
            ValueError: If business rules are violated
        """
        pass

    @abstractmethod
    def search(self, query: str) -> List[Program]:
        """
        Search programs by query string.
        
        Args:
            query: Search query
            
        Returns:
            List of matching programs
        """
        pass

    @abstractmethod
    def get_by_focus_area(self, focus_area: str) -> List[Program]:
        """
        Get programs by focus area.
        
        Args:
            focus_area: Focus area to filter by
            
        Returns:
            List of programs with specified focus area
        """
        pass

    @abstractmethod
    def get_by_national_alignment(self, alignment: str) -> List[Program]:
        """
        Get programs by national alignment.
        
        Args:
            alignment: National alignment to filter by
            
        Returns:
            List of programs with specified alignment
        """
        pass