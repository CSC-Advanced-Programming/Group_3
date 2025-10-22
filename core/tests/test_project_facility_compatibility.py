import pytest
from core.domain.entities.project import Project


def test_validate_facility_compatibility_raises_when_incompatible():
    project_requirements = ["CNC", "PCB"]
    facility_capabilities = ["CNC"]
    with pytest.raises(ValueError) as exc:
        Project.validate_facility_compatibility(project_requirements, facility_capabilities)
    assert "Project requirements not compatible with facility capabilities." in str(exc.value)


def test_validate_facility_compatibility_passes_when_compatible():
    project_requirements = ["CNC", "PCB"]
    facility_capabilities = ["CNC", "PCB", "materials testing"]
    # should not raise
    Project.validate_facility_compatibility(project_requirements, facility_capabilities)


def test_get_technical_requirements_and_has_compatible_facility_true():
    p = Project(innovation_focus="CNC, IoT", testing_requirements="PCB, materials testing", program_id=1, facility_id=1, title="T", description="D", nature_of_project="Research")
    reqs = p.get_technical_requirements()
    assert sorted(reqs) == sorted(["CNC", "IoT", "PCB", "materials testing"])

    facility_caps = ["CNC", "IoT", "PCB", "materials testing"]
    assert p.has_compatible_facility(facility_caps)


def test_has_compatible_facility_false_when_missing_capability():
    p = Project(innovation_focus="CNC", testing_requirements="PCB", program_id=1, facility_id=1, title="T", description="D", nature_of_project="Research")
    facility_caps = ["CNC"]
    assert not p.has_compatible_facility(facility_caps)
