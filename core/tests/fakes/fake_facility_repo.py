"""
Fake repository and pytest fixture for Facility domain tests.
"""

import pytest
from typing import List, Dict, Optional, Tuple

from core.domain.entities.facility import Facility
from core.application.interfaces.facility_repository import FacilityRepositoryInterface

class FakeFacilityRepository(FacilityRepositoryInterface):
    """
    A fake repository for facilities that stores data in-memory.
    Simulates database constraints and behaviors for testing purposes.
    """

    def __init__(self) -> None:
        self._facilities: Dict[int, Facility] = {}
        self._next_id = 1
        self._dependencies: Dict[str, Dict[int, bool]] = {
            "services": {},
            "equipment": {},
            "projects": {}
        }

    def save(self, facility: Facility) -> Facility:
        is_update = facility.id is not None
        
        # Intrinsic validation is handled by the entity's __post_init__
        facility._validate()

        # Uniqueness validation (context-dependent)
        exclude_id = facility.id if is_update else None
        if self.exists_by_name_and_location(facility.name, facility.location, exclude_id):
            raise ValueError("A facility with this name already exists at this location.")

        # Capabilities validation (context-dependent)
        if is_update:
            facility.validate_capabilities_requirement(
                has_services=self.has_services(facility.id),
                has_equipment=self.has_equipment(facility.id)
            )

        if not is_update:
            facility.id = self._next_id
            self._next_id += 1
        
        self._facilities[facility.id] = facility
        return facility

    def update(self, facility: Facility) -> Facility:
        if facility.id is None or facility.id not in self._facilities:
            raise ValueError("Facility not found for update.")
        return self.save(facility)

    def get_by_id(self, facility_id: int) -> Optional[Facility]:
        return self._facilities.get(facility_id)

    def exists_by_name_and_location(self, name: str, location: str, exclude_id: Optional[int] = None) -> bool:
        for f_id, facility in self._facilities.items():
            if f_id == exclude_id:
                continue
            if facility.name == name and facility.location == location:
                return True
        return False

    def has_services(self, facility_id: int) -> bool:
        return self._dependencies["services"].get(facility_id, False)

    def has_equipment(self, facility_id: int) -> bool:
        return self._dependencies["equipment"].get(facility_id, False)

    def has_projects(self, facility_id: int) -> bool:
        return self._dependencies["projects"].get(facility_id, False)

    def delete(self, facility_id: int) -> bool:
        if facility_id not in self._facilities:
            return False

        Facility.validate_deletion_constraints(
            has_services=self.has_services(facility_id),
            has_equipment=self.has_equipment(facility_id),
            has_projects=self.has_projects(facility_id)
        )
        
        del self._facilities[facility_id]
        return True

    def set_dependencies(self, facility_id: int, services: bool = False, equipment: bool = False, projects: bool = False):
        self._dependencies["services"][facility_id] = services
        self._dependencies["equipment"][facility_id] = equipment
        self._dependencies["projects"][facility_id] = projects

    # --- Unused abstract methods ---
    def get_by_facility_id(self, facility_id: str) -> Optional[Facility]: pass
    def get_all(self) -> List[Facility]: pass
    def get_by_name_and_location(self, name: str, location: str) -> Optional[Facility]: pass
    def get_all_name_location_combinations(self, exclude_id: Optional[int] = None) -> List[Tuple[str, str]]: pass
    def search(self, query: str) -> List[Facility]: pass
    def get_by_facility_type(self, facility_type: str) -> List[Facility]: pass
    def get_by_partner_organization(self, organization: str) -> List[Facility]: pass
    def get_by_capability(self, capability: str) -> List[Facility]: pass
    def get_by_location(self, location: str) -> List[Facility]: pass

@pytest.fixture
def fake_facility_repo() -> FakeFacilityRepository:
    """Provides a fresh instance of the fake repository for each test."""
    return FakeFacilityRepository()
