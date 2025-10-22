import pytest
from core.domain.entities.project import Project


def test_project_missing_program_id_raises():
    with pytest.raises(ValueError) as exc:
        Project(program_id=None, facility_id=1, title="Test Project", description="Desc", nature_of_project="Research")
    assert "Project.ProgramId and Project.FacilityId are required." in str(exc.value)


def test_project_missing_facility_id_raises():
    with pytest.raises(ValueError) as exc:
        Project(program_id=1, facility_id=None, title="Test Project", description="Desc", nature_of_project="Research")
    assert "Project.ProgramId and Project.FacilityId are required." in str(exc.value)


def test_project_with_both_associations_passes():
    # should not raise
    p = Project(program_id=2, facility_id=3, title="Valid Project", description="Desc", nature_of_project="Research")
    assert p.has_required_associations() is True
    assert p.is_assigned_to_program(2)
    assert p.is_assigned_to_facility(3)
