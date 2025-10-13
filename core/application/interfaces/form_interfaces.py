"""Form interfaces for the application layer."""
from typing import Any, Dict, Optional, Protocol, runtime_checkable


@runtime_checkable
class FormInterface(Protocol):
    """Protocol for forms."""
    
    def is_valid(self) -> bool:
        """Check if the form data is valid."""
        ...

    def get_errors(self) -> Dict[str, Any]:
        """Get form validation errors."""
        ...

    def save(self, commit: bool = True) -> Any:
        """Save form data and return the created/updated object."""
        ...

    def get_initial_data(self) -> Dict[str, Any]:
        """Get initial form data."""
        ...


@runtime_checkable
class ProjectFormInterface(FormInterface, Protocol):
    """Protocol for project forms."""
    
    def get_programs(self):
        """Get available programs."""
        ...

    def get_facilities(self):
        """Get available facilities."""
        ...


@runtime_checkable
class EquipmentFormInterface(FormInterface, Protocol):
    """Protocol for equipment forms."""
    
    def get_facilities(self):
        """Get available facilities."""
        ...


@runtime_checkable
class ServiceFormInterface(FormInterface, Protocol):
    """Protocol for service forms."""
    
    def get_facilities(self):
        """Get available facilities."""
        ...


@runtime_checkable
class ProjectParticipantFormInterface(FormInterface, Protocol):
    """Protocol for project participant forms."""
    
    def get_projects(self):
        """Get available projects."""
        ...

    def get_participants(self):
        """Get available participants."""
        ...