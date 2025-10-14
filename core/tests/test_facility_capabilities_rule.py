"""
Tests for the Facility entity's capabilities business rule.
"""

import pytest
from core.domain.entities.facility import Facility
from core.tests.fakes.fake_facility_repo import FakeFacilityRepository, fake_facility_repo

class TestFacilityCapabilitiesRule:
    """Tests the rule: Capabilities must be populated if Services/Equipment exist."""

    def test_update_fails_if_services_exist_and_capabilities_are_empty(self, fake_facility_repo: FakeFacilityRepository):
        facility = fake_facility_repo.save(Facility(name="Test", location="Here", facility_type="Lab", capabilities="CNC"))
        fake_facility_repo.set_dependencies(facility.id, services=True)

        facility.capabilities = ""

        with pytest.raises(ValueError) as excinfo:
            fake_facility_repo.update(facility)
        assert str(excinfo.value) == "Facility.Capabilities must be populated when Services/Equipment exist."

    def test_update_fails_if_equipment_exists_and_capabilities_are_empty(self, fake_facility_repo: FakeFacilityRepository):
        facility = fake_facility_repo.save(Facility(name="Test", location="Here", facility_type="Lab", capabilities="CNC"))
        fake_facility_repo.set_dependencies(facility.id, equipment=True)

        facility.capabilities = "  "  # Test with whitespace

        with pytest.raises(ValueError) as excinfo:
            fake_facility_repo.update(facility)
        assert str(excinfo.value) == "Facility.Capabilities must be populated when Services/Equipment exist."

    def test_update_succeeds_if_dependencies_exist_and_capabilities_are_populated(self, fake_facility_repo: FakeFacilityRepository):
        facility = fake_facility_repo.save(Facility(name="Test", location="Here", facility_type="Lab", capabilities="Initial"))
        fake_facility_repo.set_dependencies(facility.id, services=True)

        try:
            facility.capabilities = "CNC, PCB Fabrication"
            updated_facility = fake_facility_repo.update(facility)
        except ValueError:
            pytest.fail("Update should succeed when capabilities are populated.")

        assert updated_facility.capabilities == "CNC, PCB Fabrication"

    def test_update_succeeds_if_no_dependencies_and_capabilities_are_empty(self, fake_facility_repo: FakeFacilityRepository):
        facility = fake_facility_repo.save(Facility(name="Test", location="Here", facility_type="Lab", capabilities="Initial"))
        
        try:
            facility.capabilities = ""
            updated_facility = fake_facility_repo.update(facility)
        except ValueError:
            pytest.fail("Update should succeed when no dependencies exist, even with empty capabilities.")

        assert updated_facility.capabilities == ""
