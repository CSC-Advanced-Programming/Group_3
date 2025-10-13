"""
Repository interface for Outcome entity.
Defines the contract for Outcome data access operations.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.outcome import Outcome


class OutcomeRepositoryInterface(ABC):
    """
    Abstract interface for Outcome repository operations.
    Infrastructure layer must implement these methods.
    """

    @abstractmethod
    def save(self, outcome: Outcome) -> Outcome:
        """
        Save an outcome entity.
        
        Args:
            outcome: Outcome entity to save
            
        Returns:
            Outcome: Saved outcome with updated ID
            
        Raises:
            ValueError: If business rules are violated
        """
        pass

    @abstractmethod
    def get_by_id(self, outcome_id: int) -> Optional[Outcome]:
        """
        Retrieve an outcome by its ID.
        
        Args:
            outcome_id: Unique identifier of the outcome
            
        Returns:
            Outcome or None if not found
        """
        pass

    @abstractmethod
    def get_by_outcome_id(self, outcome_id: str) -> Optional[Outcome]:
        """
        Retrieve an outcome by its outcome_id field.
        
        Args:
            outcome_id: Outcome identifier (e.g., 'O-001')
            
        Returns:
            Outcome or None if not found
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Outcome]:
        """
        Retrieve all outcomes.
        
        Returns:
            List of all outcomes
        """
        pass

    @abstractmethod
    def get_by_project_id(self, project_id: int) -> List[Outcome]:
        """
        Get outcomes by project ID.
        
        Args:
            project_id: Project ID to filter by
            
        Returns:
            List of outcomes for specified project
        """
        pass

    @abstractmethod
    def delete(self, outcome_id: int) -> bool:
        """
        Delete an outcome by ID.
        
        Args:
            outcome_id: ID of outcome to delete
            
        Returns:
            True if deletion successful, False otherwise
        """
        pass

    @abstractmethod
    def update(self, outcome: Outcome) -> Outcome:
        """
        Update an existing outcome.
        
        Args:
            outcome: Outcome entity with updated data
            
        Returns:
            Updated outcome entity
            
        Raises:
            ValueError: If business rules are violated
        """
        pass

    @abstractmethod
    def search(self, query: str) -> List[Outcome]:
        """
        Search outcomes by query string.
        
        Args:
            query: Search query
            
        Returns:
            List of matching outcomes
        """
        pass

    @abstractmethod
    def get_by_outcome_type(self, outcome_type: str) -> List[Outcome]:
        """
        Get outcomes by type.
        
        Args:
            outcome_type: Outcome type to filter by
            
        Returns:
            List of outcomes of specified type
        """
        pass

    @abstractmethod
    def get_by_commercialization_status(self, status: str) -> List[Outcome]:
        """
        Get outcomes by commercialization status.
        
        Args:
            status: Commercialization status to filter by
            
        Returns:
            List of outcomes with specified status
        """
        pass

    @abstractmethod
    def get_certified_outcomes(self) -> List[Outcome]:
        """
        Get all certified outcomes.
        
        Returns:
            List of outcomes with quality certification
        """
        pass

    @abstractmethod
    def get_outcomes_with_artifacts(self) -> List[Outcome]:
        """
        Get outcomes that have artifact links.
        
        Returns:
            List of outcomes with artifact links
        """
        pass

    @abstractmethod
    def get_tangible_deliverables(self) -> List[Outcome]:
        """
        Get tangible deliverable outcomes (CAD, PCB, Prototype).
        
        Returns:
            List of tangible outcome deliverables
        """
        pass

    @abstractmethod
    def get_documentation_outcomes(self) -> List[Outcome]:
        """
        Get documentation outcomes (Reports, Business Plans).
        
        Returns:
            List of documentation outcomes
        """
        pass

    @abstractmethod
    def get_ready_for_commercialization(self) -> List[Outcome]:
        """
        Get outcomes ready for commercialization.
        
        Returns:
            List of outcomes that meet commercialization criteria
        """
        pass

    @abstractmethod
    def get_demoed_outcomes(self) -> List[Outcome]:
        """
        Get outcomes that have been demoed.
        
        Returns:
            List of outcomes with 'Demoed' status
        """
        pass

    @abstractmethod
    def get_market_linked_outcomes(self) -> List[Outcome]:
        """
        Get outcomes that are market linked.
        
        Returns:
            List of outcomes with 'Market Linked' status
        """
        pass

    @abstractmethod
    def get_launched_outcomes(self) -> List[Outcome]:
        """
        Get outcomes that have been launched.
        
        Returns:
            List of outcomes with 'Launched' status
        """
        pass