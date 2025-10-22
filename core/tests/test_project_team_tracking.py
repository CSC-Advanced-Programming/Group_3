import pytest
from core.domain.entities.project import Project


def test_validate_team_tracking_raises_when_no_team():
    with pytest.raises(ValueError) as exc:
        Project.validate_team_tracking(False)
    assert "Project must have at least one team member assigned." in str(exc.value)


def test_validate_team_tracking_passes_when_has_team():
    # should not raise
    Project.validate_team_tracking(True)
