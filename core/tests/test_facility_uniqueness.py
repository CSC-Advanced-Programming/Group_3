"""
Tests for the Facility entity's uniqueness (name + location) business rule.
"""

import pytest
from core.domain.entities.facility import Facility
from core.tests.fakes.fake_facility_repo import FakeFacilityRepository, fake_facility_repo

class TestFacilityUniqueness:
    """Tests the rule: The combination of Name + Location must be unique."""

    def test_facility_creation_fails_for_duplicate_name_location(self, fake_facility_repo: FakeFacilityRepository):
        # Arrange: Create an initial facility
        facility1 = Facility(name="UIRI Lab", location="Kampala", facility_type="Lab")
        fake_facility_repo.save(facility1)

        # Act & Assert: Try to create another with the same name and location
        facility2 = Facility(name="UIRI Lab", location="Kampala", facility_type="Workshop")
        with pytest.raises(ValueError) as excinfo:
            fake_facility_repo.save(facility2)
        assert str(excinfo.value) == "A facility with this name already exists at this location."

    def test_facility_update_to_existing_name_location_fails(self, fake_facility_repo: FakeFacilityRepository):
        # Arrange
        fake_facility_repo.save(Facility(name="Existing Name", location="Existing Location", facility_type="Lab"))
        facility_to_update = fake_facility_repo.save(Facility(name="Original Name", location="Original Location", facility_type="Lab"))

        # Act & Assert
        facility_to_update.name = "Existing Name"
        facility_to_update.location = "Existing Location"

        with pytest.raises(ValueError) as excinfo:
            fake_facility_repo.update(facility_to_update)
        
        assert str(excinfo.value) == "A facility with this name already exists at this location."

    def test_facility_update_with_same_name_location_succeeds(self, fake_facility_repo: FakeFacilityRepository):
        # Arrange
        facility = fake_facility_repo.save(Facility(name="My Lab", location="My Town", facility_type="Lab"))

        # Act
        try:
            facility.description = "Updated description"
            fake_facility_repo.update(facility)
        except ValueError:
            pytest.fail("Updating a facility with its own name/location should not fail uniqueness check.")

        # Assert
        updated_facility = fake_facility_repo.get_by_id(facility.id)
        assert updated_facility.description == "Updated description"
