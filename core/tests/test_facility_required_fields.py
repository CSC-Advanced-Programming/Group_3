"""
Tests for the Facility entity's required fields business rule.
"""

import pytest
from core.domain.entities.facility import Facility
from core.tests.fakes.fake_facility_repo import FakeFacilityRepository, fake_facility_repo


class TestFacilityRequiredFields:
    """Tests the rule: Name, Location, and FacilityType are mandatory."""

    def test_facility_creation_fails_when_name_is_missing(self, fake_facility_repo: FakeFacilityRepository):
        with pytest.raises(ValueError) as excinfo:
            Facility(name=None, location="Kampala", facility_type="Lab")
        assert str(excinfo.value) == "Facility.Name, Facility.Location, and Facility.FacilityType are required."

    def test_facility_creation_fails_when_name_is_empty(self, fake_facility_repo: FakeFacilityRepository):
        with pytest.raises(ValueError) as excinfo:
            Facility(name="  ", location="Kampala", facility_type="Lab")
        assert str(excinfo.value) == "Facility.Name, Facility.Location, and Facility.FacilityType are required."

    def test_facility_creation_fails_when_location_is_missing(self, fake_facility_repo: FakeFacilityRepository):
        with pytest.raises(ValueError) as excinfo:
            Facility(name="Makerere CoCIS", location="", facility_type="Lab")
        assert str(excinfo.value) == "Facility.Name, Facility.Location, and Facility.FacilityType are required."

    def test_facility_creation_fails_when_facility_type_is_missing(self, fake_facility_repo: FakeFacilityRepository):
        with pytest.raises(ValueError) as excinfo:
            Facility(name="Makerere CoCIS", location="Kampala", facility_type=None)
        assert str(excinfo.value) == "Facility.Name, Facility.Location, and Facility.FacilityType are required."

    def test_valid_facility_creation_succeeds(self, fake_facility_repo: FakeFacilityRepository):
        # Arrange & Act
        try:
            facility = Facility(
                name="CEDAT Lab",
                location="Makerere",
                facility_type="Lab"
            )
            saved_facility = fake_facility_repo.save(facility)
        except ValueError:
            pytest.fail("Valid facility creation should not raise a ValueError.")

        # Assert
        assert saved_facility.id is not None
        assert saved_facility.name == "CEDAT Lab"
