import pytest
from core.domain.entities.project import Project


def test_validate_outcome_validation_raises_when_completed_and_no_outcomes():
    with pytest.raises(ValueError) as exc:
        Project.validate_outcome_validation("Completed", False)
    assert "Completed projects must have at least one documented outcome." in str(exc.value)


def test_validate_outcome_validation_passes_when_completed_and_has_outcomes():
    # should not raise
    Project.validate_outcome_validation("completed", True)


def test_validate_outcome_validation_passes_when_not_completed_and_no_outcomes():
    # should not raise
    Project.validate_outcome_validation("in progress", False)
