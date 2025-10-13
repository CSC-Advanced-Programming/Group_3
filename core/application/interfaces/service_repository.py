"""
Repository interface for Service entity.
Defines the contract for Service data access operations.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.service import Service


class ServiceRepositoryInterface(ABC):
    """
    Abstract interface for Service repository operations.
    Infrastructure layer must implement these methods.
    """

    @abstractmethod
    def save(self, service: Service) -> Service:
        """
        Save a service entity.
        
        Args:
            service: Service entity to save
            
        Returns:
            Service: Saved service with updated ID
            
        Raises:
            ValueError: If business rules are violated
        """
        pass

    @abstractmethod
    def get_by_id(self, service_id: int) -> Optional[Service]:
        """
        Retrieve a service by its ID.
        
        Args:
            service_id: Unique identifier of the service
            
        Returns:
            Service or None if not found
        """
        pass

    @abstractmethod
    def get_by_service_id(self, service_id: str) -> Optional[Service]:
        """
        Retrieve a service by its service_id field.
        
        Args:
            service_id: Service identifier (e.g., 'S-001')
            
        Returns:
            Service or None if not found
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Service]:
        """
        Retrieve all services.
        
        Returns:
            List of all services
        """
        pass

    @abstractmethod
    def get_by_facility_id(self, facility_id: int) -> List[Service]:
        """
        Get services by facility ID.
        
        Args:
            facility_id: Facility ID to filter by
            
        Returns:
            List of services in specified facility
        """
        pass

    @abstractmethod
    def exists_by_name_in_facility(self, name: str, facility_id: int, exclude_id: Optional[int] = None) -> bool:
        """
        Check if a service with given name exists in a facility.
        
        Args:
            name: Service name
            facility_id: Facility ID to check within
            exclude_id: Optional ID to exclude from check (for updates)
            
        Returns:
            True if service with name exists in facility, False otherwise
        """
        pass

    @abstractmethod
    def get_all_names_in_facility(self, facility_id: int, exclude_id: Optional[int] = None) -> List[str]:
        """
        Get all service names in a facility for uniqueness validation.
        
        Args:
            facility_id: Facility ID to get names from
            exclude_id: Optional ID to exclude (for updates)
            
        Returns:
            List of service names in the facility
        """
        pass

    @abstractmethod
    def is_used_by_project_testing(self, service_id: int) -> bool:
        """
        Check if service is used by any project testing requirements.
        
        Args:
            service_id: Service ID to check
            
        Returns:
            True if service is used by project testing, False otherwise
        """
        pass

    @abstractmethod
    def delete(self, service_id: int) -> bool:
        """
        Delete a service by ID.
        
        Args:
            service_id: ID of service to delete
            
        Returns:
            True if deletion successful, False otherwise
            
        Raises:
            ValueError: If service is used by project testing requirements
        """
        pass

    @abstractmethod
    def update(self, service: Service) -> Service:
        """
        Update an existing service.
        
        Args:
            service: Service entity with updated data
            
        Returns:
            Updated service entity
            
        Raises:
            ValueError: If business rules are violated
        """
        pass

    @abstractmethod
    def search(self, query: str) -> List[Service]:
        """
        Search services by query string.
        
        Args:
            query: Search query
            
        Returns:
            List of matching services
        """
        pass

    @abstractmethod
    def get_by_category(self, category: str) -> List[Service]:
        """
        Get services by category.
        
        Args:
            category: Service category to filter by
            
        Returns:
            List of services in specified category
        """
        pass

    @abstractmethod
    def get_by_skill_type(self, skill_type: str) -> List[Service]:
        """
        Get services by skill type.
        
        Args:
            skill_type: Skill type to filter by
            
        Returns:
            List of services for specified skill type
        """
        pass

    @abstractmethod
    def get_by_phase(self, phase: str) -> List[Service]:
        """
        Get services relevant for a specific project phase.
        
        Args:
            phase: Project phase to filter by
            
        Returns:
            List of services relevant for specified phase
        """
        pass

    @abstractmethod
    def get_for_skill_development(self, skill: str) -> List[Service]:
        """
        Get services that can support development of a specific skill.
        
        Args:
            skill: Skill to develop
            
        Returns:
            List of services supporting skill development
        """
        pass