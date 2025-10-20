"""
Tests for the Facility entity's deletion constraint business rule.
"""

import pytest
from core.domain.entities.facility import Facility
from core.tests.fakes.fake_facility_repo import FakeFacilityRepository, fake_facility_repo

class TestFacilityDeletionConstraint:
    """Tests the rule: Facilities cannot be deleted if they have related records."""

    def test_deletion_fails_if_services_exist(self, fake_facility_repo: FakeFacilityRepository):
        facility = fake_facility_repo.save(Facility(name="Test", location="Here", facility_type="Lab"))
        fake_facility_repo.set_dependencies(facility.id, services=True)

        with pytest.raises(ValueError) as excinfo:
            fake_facility_repo.delete(facility.id)
        assert str(excinfo.value) == "Facility has dependent records (Services/Equipment/Projects)."

    def test_deletion_fails_if_equipment_exists(self, fake_facility_repo: FakeFacilityRepository):
        facility = fake_facility_repo.save(Facility(name="Test", location="Here", facility_type="Lab"))
        fake_facility_repo.set_dependencies(facility.id, equipment=True)

        with pytest.raises(ValueError) as excinfo:
            fake_facility_repo.delete(facility.id)
        assert str(excinfo.value) == "Facility has dependent records (Services/Equipment/Projects)."

    def test_deletion_fails_if_projects_exist(self, fake_facility_repo: FakeFacilityRepository):
        facility = fake_facility_repo.save(Facility(name="Test", location="Here", facility_type="Lab"))
        fake_facility_repo.set_dependencies(facility.id, projects=True)

        with pytest.raises(ValueError) as excinfo:
            fake_facility_repo.delete(facility.id)
        assert str(excinfo.value) == "Facility has dependent records (Services/Equipment/Projects)."

    def test_deletion_succeeds_when_no_dependencies_exist(self, fake_facility_repo: FakeFacilityRepository):
        facility = fake_facility_repo.save(Facility(name="Test", location="Here", facility_type="Lab"))
        
        try:
            deleted = fake_facility_repo.delete(facility.id)
        except ValueError:
            pytest.fail("Deletion should succeed when no dependencies exist.")

        assert deleted is True
        assert fake_facility_repo.get_by_id(facility.id) is None
