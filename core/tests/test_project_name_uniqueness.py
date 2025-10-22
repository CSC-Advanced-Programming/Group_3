import pytest
from core.domain.entities.project import Project


def test_validate_name_uniqueness_raises_for_duplicate_title_in_program():
    existing_titles = ["Alpha Project", "Beta Project"]
    with pytest.raises(ValueError) as exc:
        Project.validate_name_uniqueness("Alpha Project", program_id=1, existing_titles_in_program=existing_titles)
    assert "A project with this name already exists in this program." in str(exc.value)


def test_validate_name_uniqueness_passes_for_new_title():
    existing_titles = ["Alpha Project", "Beta Project"]
    # should not raise
    Project.validate_name_uniqueness("Gamma Project", program_id=1, existing_titles_in_program=existing_titles)


def test_validate_name_uniqueness_case_sensitive_check():
    existing_titles = ["Alpha Project"]
    # The domain method does a straightforward membership check; ensure exact match raises
    with pytest.raises(ValueError):
        Project.validate_name_uniqueness("Alpha Project", program_id=1, existing_titles_in_program=existing_titles)
