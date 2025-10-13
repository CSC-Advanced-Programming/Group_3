"""
Repository interface for Participant entity.
Defines the contract for Participant data access operations.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.participant import Participant


class ParticipantRepositoryInterface(ABC):
    """
    Abstract interface for Participant repository operations.
    Infrastructure layer must implement these methods.
    """

    @abstractmethod
    def save(self, participant: Participant) -> Participant:
        """
        Save a participant entity.
        
        Args:
            participant: Participant entity to save
            
        Returns:
            Participant: Saved participant with updated ID
            
        Raises:
            ValueError: If business rules are violated
        """
        pass

    @abstractmethod
    def get_by_id(self, participant_id: int) -> Optional[Participant]:
        """
        Retrieve a participant by its ID.
        
        Args:
            participant_id: Unique identifier of the participant
            
        Returns:
            Participant or None if not found
        """
        pass

    @abstractmethod
    def get_by_participant_id(self, participant_id: str) -> Optional[Participant]:
        """
        Retrieve a participant by its participant_id field.
        
        Args:
            participant_id: Participant identifier (e.g., 'PT-001')
            
        Returns:
            Participant or None if not found
        """
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Participant]:
        """
        Retrieve a participant by email.
        
        Args:
            email: Participant email
            
        Returns:
            Participant or None if not found
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Participant]:
        """
        Retrieve all participants.
        
        Returns:
            List of all participants
        """
        pass

    @abstractmethod
    def exists_by_email(self, email: str, exclude_id: Optional[int] = None) -> bool:
        """
        Check if a participant with given email exists.
        
        Args:
            email: Email to check
            exclude_id: Optional ID to exclude from check (for updates)
            
        Returns:
            True if participant with email exists, False otherwise
        """
        pass

    @abstractmethod
    def get_all_emails(self, exclude_id: Optional[int] = None) -> List[str]:
        """
        Get all participant emails for uniqueness validation.
        
        Args:
            exclude_id: Optional ID to exclude (for updates)
            
        Returns:
            List of all participant emails
        """
        pass

    @abstractmethod
    def delete(self, participant_id: int) -> bool:
        """
        Delete a participant by ID.
        
        Args:
            participant_id: ID of participant to delete
            
        Returns:
            True if deletion successful, False otherwise
        """
        pass

    @abstractmethod
    def update(self, participant: Participant) -> Participant:
        """
        Update an existing participant.
        
        Args:
            participant: Participant entity with updated data
            
        Returns:
            Updated participant entity
            
        Raises:
            ValueError: If business rules are violated
        """
        pass

    @abstractmethod
    def search(self, query: str) -> List[Participant]:
        """
        Search participants by query string.
        
        Args:
            query: Search query
            
        Returns:
            List of matching participants
        """
        pass

    @abstractmethod
    def get_by_affiliation(self, affiliation: str) -> List[Participant]:
        """
        Get participants by affiliation.
        
        Args:
            affiliation: Affiliation to filter by
            
        Returns:
            List of participants with specified affiliation
        """
        pass

    @abstractmethod
    def get_by_specialization(self, specialization: str) -> List[Participant]:
        """
        Get participants by specialization.
        
        Args:
            specialization: Specialization to filter by
            
        Returns:
            List of participants with specified specialization
        """
        pass

    @abstractmethod
    def get_by_institution(self, institution: str) -> List[Participant]:
        """
        Get participants by institution.
        
        Args:
            institution: Institution to filter by
            
        Returns:
            List of participants from specified institution
        """
        pass

    @abstractmethod
    def get_cross_skill_trained(self) -> List[Participant]:
        """
        Get all cross-skill trained participants.
        
        Returns:
            List of cross-skill trained participants
        """
        pass

    @abstractmethod
    def get_by_technical_background(self) -> List[Participant]:
        """
        Get participants with technical background.
        
        Returns:
            List of participants with technical specialization/affiliation
        """
        pass

    @abstractmethod
    def get_by_business_background(self) -> List[Participant]:
        """
        Get participants with business background.
        
        Returns:
            List of participants with business specialization
        """
        pass

    @abstractmethod
    def get_available_for_project(self, required_specialization: str) -> List[Participant]:
        """
        Get participants available for a project requiring specific skills.
        
        Args:
            required_specialization: Required specialization
            
        Returns:
            List of participants who can contribute to the project
        """
        pass