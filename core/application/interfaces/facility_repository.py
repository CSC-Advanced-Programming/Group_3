"""
Repository interface for Facility entity.
Defines the contract for Facility data access operations.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from core.domain.entities.facility import Facility


class FacilityRepositoryInterface(ABC):
    """
    Abstract interface for Facility repository operations.
    Infrastructure layer must implement these methods.
    """

    @abstractmethod
    def save(self, facility: Facility) -> Facility:
        """
        Save a facility entity.
        
        Args:
            facility: Facility entity to save
            
        Returns:
            Facility: Saved facility with updated ID
            
        Raises:
            ValueError: If business rules are violated
        """
        pass

    @abstractmethod
    def get_by_id(self, facility_id: int) -> Optional[Facility]:
        """
        Retrieve a facility by its ID.
        
        Args:
            facility_id: Unique identifier of the facility
            
        Returns:
            Facility or None if not found
        """
        pass

    @abstractmethod
    def get_by_facility_id(self, facility_id: str) -> Optional[Facility]:
        """
        Retrieve a facility by its facility_id field.
        
        Args:
            facility_id: Facility identifier (e.g., 'F-001')
            
        Returns:
            Facility or None if not found
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Facility]:
        """
        Retrieve all facilities.
        
        Returns:
            List of all facilities
        """
        pass

    @abstractmethod
    def get_by_name_and_location(self, name: str, location: str) -> Optional[Facility]:
        """
        Retrieve a facility by name and location combination.
        
        Args:
            name: Facility name
            location: Facility location
            
        Returns:
            Facility or None if not found
        """
        pass

    @abstractmethod
    def exists_by_name_and_location(self, name: str, location: str, exclude_id: Optional[int] = None) -> bool:
        """
        Check if a facility with given name and location exists.
        
        Args:
            name: Facility name
            location: Facility location
            exclude_id: Optional ID to exclude from check (for updates)
            
        Returns:
            True if facility exists, False otherwise
        """
        pass

    @abstractmethod
    def get_all_name_location_combinations(self, exclude_id: Optional[int] = None) -> List[Tuple[str, str]]:
        """
        Get all name-location combinations for uniqueness validation.
        
        Args:
            exclude_id: Optional ID to exclude (for updates)
            
        Returns:
            List of (name, location) tuples
        """
        pass

    @abstractmethod
    def has_services(self, facility_id: int) -> bool:
        """
        Check if facility has associated services.
        
        Args:
            facility_id: Facility ID to check
            
        Returns:
            True if facility has services, False otherwise
        """
        pass

    @abstractmethod
    def has_equipment(self, facility_id: int) -> bool:
        """
        Check if facility has associated equipment.
        
        Args:
            facility_id: Facility ID to check
            
        Returns:
            True if facility has equipment, False otherwise
        """
        pass

    @abstractmethod
    def has_projects(self, facility_id: int) -> bool:
        """
        Check if facility has associated projects.
        
        Args:
            facility_id: Facility ID to check
            
        Returns:
            True if facility has projects, False otherwise
        """
        pass

    @abstractmethod
    def delete(self, facility_id: int) -> bool:
        """
        Delete a facility by ID.
        
        Args:
            facility_id: ID of facility to delete
            
        Returns:
            True if deletion successful, False otherwise
            
        Raises:
            ValueError: If facility has dependent records
        """
        pass

    @abstractmethod
    def update(self, facility: Facility) -> Facility:
        """
        Update an existing facility.
        
        Args:
            facility: Facility entity with updated data
            
        Returns:
            Updated facility entity
            
        Raises:
            ValueError: If business rules are violated
        """
        pass

    @abstractmethod
    def search(self, query: str) -> List[Facility]:
        """
        Search facilities by query string.
        
        Args:
            query: Search query
            
        Returns:
            List of matching facilities
        """
        pass

    @abstractmethod
    def get_by_facility_type(self, facility_type: str) -> List[Facility]:
        """
        Get facilities by type.
        
        Args:
            facility_type: Facility type to filter by
            
        Returns:
            List of facilities of specified type
        """
        pass

    @abstractmethod
    def get_by_partner_organization(self, organization: str) -> List[Facility]:
        """
        Get facilities by partner organization.
        
        Args:
            organization: Partner organization to filter by
            
        Returns:
            List of facilities operated by specified organization
        """
        pass

    @abstractmethod
    def get_by_capability(self, capability: str) -> List[Facility]:
        """
        Get facilities that have a specific capability.
        
        Args:
            capability: Capability to search for
            
        Returns:
            List of facilities with specified capability
        """
        pass

    @abstractmethod
    def get_by_location(self, location: str) -> List[Facility]:
        """
        Get facilities by location.
        
        Args:
            location: Location to filter by
            
        Returns:
            List of facilities at specified location
        """
        pass