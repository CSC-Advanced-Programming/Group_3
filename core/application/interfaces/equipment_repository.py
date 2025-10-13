"""
Repository interface for Equipment entity.
Defines the contract for Equipment data access operations.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.entities.equipment import Equipment


class EquipmentRepositoryInterface(ABC):
    """
    Abstract interface for Equipment repository operations.
    Infrastructure layer must implement these methods.
    """

    @abstractmethod
    def save(self, equipment: Equipment) -> Equipment:
        """
        Save an equipment entity.
        
        Args:
            equipment: Equipment entity to save
            
        Returns:
            Equipment: Saved equipment with updated ID
            
        Raises:
            ValueError: If business rules are violated
        """
        pass

    @abstractmethod
    def get_by_id(self, equipment_id: int) -> Optional[Equipment]:
        """
        Retrieve equipment by its ID.
        
        Args:
            equipment_id: Unique identifier of the equipment
            
        Returns:
            Equipment or None if not found
        """
        pass

    @abstractmethod
    def get_by_equipment_id(self, equipment_id: str) -> Optional[Equipment]:
        """
        Retrieve equipment by its equipment_id field.
        
        Args:
            equipment_id: Equipment identifier (e.g., 'EQ-001')
            
        Returns:
            Equipment or None if not found
        """
        pass

    @abstractmethod
    def get_by_inventory_code(self, inventory_code: str) -> Optional[Equipment]:
        """
        Retrieve equipment by its inventory code.
        
        Args:
            inventory_code: Equipment inventory code
            
        Returns:
            Equipment or None if not found
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Equipment]:
        """
        Retrieve all equipment.
        
        Returns:
            List of all equipment
        """
        pass

    @abstractmethod
    def get_by_facility_id(self, facility_id: int) -> List[Equipment]:
        """
        Get equipment by facility ID.
        
        Args:
            facility_id: Facility ID to filter by
            
        Returns:
            List of equipment in specified facility
        """
        pass

    @abstractmethod
    def exists_by_inventory_code(self, inventory_code: str, exclude_id: Optional[int] = None) -> bool:
        """
        Check if equipment with given inventory code exists.
        
        Args:
            inventory_code: Inventory code to check
            exclude_id: Optional ID to exclude from check (for updates)
            
        Returns:
            True if equipment with inventory code exists, False otherwise
        """
        pass

    @abstractmethod
    def get_all_inventory_codes(self, exclude_id: Optional[int] = None) -> List[str]:
        """
        Get all inventory codes for uniqueness validation.
        
        Args:
            exclude_id: Optional ID to exclude (for updates)
            
        Returns:
            List of all inventory codes
        """
        pass

    @abstractmethod
    def is_referenced_by_active_project(self, equipment_id: int) -> bool:
        """
        Check if equipment is referenced by any active project.
        
        Args:
            equipment_id: Equipment ID to check
            
        Returns:
            True if equipment is referenced by active project, False otherwise
        """
        pass

    @abstractmethod
    def delete(self, equipment_id: int) -> bool:
        """
        Delete equipment by ID.
        
        Args:
            equipment_id: ID of equipment to delete
            
        Returns:
            True if deletion successful, False otherwise
            
        Raises:
            ValueError: If equipment is referenced by active project
        """
        pass

    @abstractmethod
    def update(self, equipment: Equipment) -> Equipment:
        """
        Update an existing equipment.
        
        Args:
            equipment: Equipment entity with updated data
            
        Returns:
            Updated equipment entity
            
        Raises:
            ValueError: If business rules are violated
        """
        pass

    @abstractmethod
    def search(self, query: str) -> List[Equipment]:
        """
        Search equipment by query string.
        
        Args:
            query: Search query
            
        Returns:
            List of matching equipment
        """
        pass

    @abstractmethod
    def get_by_capability(self, capability: str) -> List[Equipment]:
        """
        Get equipment that has a specific capability.
        
        Args:
            capability: Capability to search for
            
        Returns:
            List of equipment with specified capability
        """
        pass

    @abstractmethod
    def get_by_usage_domain(self, domain: str) -> List[Equipment]:
        """
        Get equipment by usage domain.
        
        Args:
            domain: Usage domain to filter by
            
        Returns:
            List of equipment for specified domain
        """
        pass

    @abstractmethod
    def get_by_support_phase(self, phase: str) -> List[Equipment]:
        """
        Get equipment by support phase.
        
        Args:
            phase: Support phase to filter by
            
        Returns:
            List of equipment supporting specified phase
        """
        pass

    @abstractmethod
    def get_electronics_equipment(self) -> List[Equipment]:
        """
        Get all electronics equipment.
        
        Returns:
            List of equipment with Electronics usage domain
        """
        pass

    @abstractmethod
    def get_equipment_for_project_requirements(self, capabilities: List[str], domains: List[str]) -> List[Equipment]:
        """
        Get equipment that can support project requirements.
        
        Args:
            capabilities: Required capabilities
            domains: Required usage domains
            
        Returns:
            List of compatible equipment
        """
        pass