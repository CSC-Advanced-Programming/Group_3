"""
Comprehensive unit tests for Project entity business rules.
Tests all Project domain logic in a single file for better organization.
"""
import pytest
from core.domain.entities.project import Project


class TestProjectEntity:
    """Unit tests for Project entity covering all business rules."""

    # ========================================================================
    # Required Associations Rule Tests
    # ========================================================================
    
    def test_project_missing_program_id_raises(self):
        """Test Required Associations: Missing program_id raises error."""
        with pytest.raises(ValueError) as exc:
            Project(program_id=None, facility_id=1, title="Test Project", description="Desc", nature_of_project="Research")
        assert "Project.ProgramId and Project.FacilityId are required." in str(exc.value)

    def test_project_missing_facility_id_raises(self):
        """Test Required Associations: Missing facility_id raises error."""
        with pytest.raises(ValueError) as exc:
            Project(program_id=1, facility_id=None, title="Test Project", description="Desc", nature_of_project="Research")
        assert "Project.ProgramId and Project.FacilityId are required." in str(exc.value)

    def test_project_with_both_associations_passes(self):
        """Test Required Associations: Valid associations succeed."""
        p = Project(program_id=2, facility_id=3, title="Valid Project", description="Desc", nature_of_project="Research")
        assert p.has_required_associations() is True
        assert p.is_assigned_to_program(2)
        assert p.is_assigned_to_facility(3)

    # ========================================================================
    # Team Tracking Rule Tests
    # ========================================================================
    
    def test_validate_team_tracking_raises_when_no_team(self):
        """Test Team Tracking: No team members raises error."""
        with pytest.raises(ValueError) as exc:
            Project.validate_team_tracking(False)
        assert "Project must have at least one team member assigned." in str(exc.value)

    def test_validate_team_tracking_passes_when_has_team(self):
        """Test Team Tracking: Having team members passes."""
        # should not raise
        Project.validate_team_tracking(True)

    # ========================================================================
    # Outcome Validation Rule Tests
    # ========================================================================
    
    def test_validate_outcome_validation_raises_when_completed_and_no_outcomes(self):
        """Test Outcome Validation: Completed projects without outcomes raise error."""
        with pytest.raises(ValueError) as exc:
            Project.validate_outcome_validation("Completed", False)
        assert "Completed projects must have at least one documented outcome." in str(exc.value)

    def test_validate_outcome_validation_passes_when_completed_and_has_outcomes(self):
        """Test Outcome Validation: Completed projects with outcomes pass."""
        # should not raise
        Project.validate_outcome_validation("completed", True)

    def test_validate_outcome_validation_passes_when_not_completed_and_no_outcomes(self):
        """Test Outcome Validation: Non-completed projects without outcomes pass."""
        # should not raise
        Project.validate_outcome_validation("in progress", False)

    # ========================================================================
    # Name Uniqueness Rule Tests
    # ========================================================================
    
    def test_validate_name_uniqueness_raises_for_duplicate_title_in_program(self):
        """Test Name Uniqueness: Duplicate title in same program raises error."""
        existing_titles = ["Alpha Project", "Beta Project"]
        with pytest.raises(ValueError) as exc:
            Project.validate_name_uniqueness("Alpha Project", program_id=1, existing_titles_in_program=existing_titles)
        assert "A project with this name already exists in this program." in str(exc.value)

    def test_validate_name_uniqueness_passes_for_new_title(self):
        """Test Name Uniqueness: New title in program passes."""
        existing_titles = ["Alpha Project", "Beta Project"]
        # should not raise
        Project.validate_name_uniqueness("Gamma Project", program_id=1, existing_titles_in_program=existing_titles)

    def test_validate_name_uniqueness_case_sensitive_check(self):
        """Test Name Uniqueness: Exact match validation."""
        existing_titles = ["Alpha Project"]
        # The domain method does a straightforward membership check; ensure exact match raises
        with pytest.raises(ValueError):
            Project.validate_name_uniqueness("Alpha Project", program_id=1, existing_titles_in_program=existing_titles)

    # ========================================================================
    # Facility Compatibility Rule Tests
    # ========================================================================
    
    def test_validate_facility_compatibility_raises_when_incompatible(self):
        """Test Facility Compatibility: Incompatible requirements raise error."""
        project_requirements = ["CNC", "PCB"]
        facility_capabilities = ["CNC"]
        with pytest.raises(ValueError) as exc:
            Project.validate_facility_compatibility(project_requirements, facility_capabilities)
        assert "Project requirements not compatible with facility capabilities." in str(exc.value)

    def test_validate_facility_compatibility_passes_when_compatible(self):
        """Test Facility Compatibility: Compatible requirements pass."""
        project_requirements = ["CNC", "PCB"]
        facility_capabilities = ["CNC", "PCB", "materials testing"]
        # should not raise
        Project.validate_facility_compatibility(project_requirements, facility_capabilities)

    def test_get_technical_requirements_and_has_compatible_facility_true(self):
        """Test Facility Compatibility: Technical requirements extraction and compatibility check."""
        p = Project(innovation_focus="CNC, IoT", testing_requirements="PCB, materials testing", program_id=1, facility_id=1, title="T", description="D", nature_of_project="Research")
        reqs = p.get_technical_requirements()
        assert sorted(reqs) == sorted(["CNC", "IoT", "PCB", "materials testing"])

        facility_caps = ["CNC", "IoT", "PCB", "materials testing"]
        assert p.has_compatible_facility(facility_caps)

    def test_has_compatible_facility_false_when_missing_capability(self):
        """Test Facility Compatibility: Missing capability returns false."""
        p = Project(innovation_focus="CNC", testing_requirements="PCB", program_id=1, facility_id=1, title="T", description="D", nature_of_project="Research")
        facility_caps = ["CNC"]
        assert not p.has_compatible_facility(facility_caps)

    # ========================================================================
    # Additional Project Entity Helper Methods Tests
    # ========================================================================
    
    def test_innovation_focus_list_parsing_empty_returns_empty(self):
        """Test innovation focus list parsing with empty focus."""
        p = Project(program_id=1, facility_id=1, title="T", description="D", nature_of_project="Research")
        assert p.innovation_focus_list == []

    def test_innovation_focus_list_parsing_multiple(self):
        """Test innovation focus list parsing with multiple focuses."""
        p = Project(innovation_focus="AI, IoT,  Blockchain", program_id=1, facility_id=1, title="T", description="D", nature_of_project="Research")
        assert p.innovation_focus_list == ["AI", "IoT", "Blockchain"]

    def test_is_prototype_stage_case_insensitive(self):
        """Test prototype stage checking is case insensitive."""
        p = Project(prototype_stage="Prototype", program_id=1, facility_id=1, title="T", description="D", nature_of_project="Research")
        assert p.is_prototype_stage("prototype")
        assert p.is_prototype_stage("PROTOTYPE")
        assert not p.is_prototype_stage("mvp")

    def test_is_nature_of_case_insensitive(self):
        """Test nature checking is case insensitive."""
        p = Project(nature_of_project="Research", program_id=1, facility_id=1, title="T", description="D")
        assert p.is_nature_of("research")
        assert p.is_nature_of("RESEARCH")
        assert not p.is_nature_of("prototype")

    def test_has_innovation_focus_true_false(self):
        """Test innovation focus checking."""
        p = Project(innovation_focus="AI, IoT", program_id=1, facility_id=1, title="T", description="D", nature_of_project="Research")
        assert p.has_innovation_focus("AI")
        assert p.has_innovation_focus("IoT")
        assert not p.has_innovation_focus("Blockchain")

    def test_add_innovation_focus_adds_and_no_duplicate(self):
        """Test adding innovation focus prevents duplicates."""
        p = Project(innovation_focus="AI", program_id=1, facility_id=1, title="T", description="D", nature_of_project="Research")
        p.add_innovation_focus("IoT")
        assert "IoT" in p.innovation_focus_list
        # adding existing should not duplicate
        p.add_innovation_focus("AI")
        assert p.innovation_focus_list.count("AI") == 1

    def test_add_innovation_focus_empty_raises(self):
        """Test adding empty innovation focus raises error."""
        p = Project(program_id=1, facility_id=1, title="T", description="D", nature_of_project="Research")
        with pytest.raises(ValueError):
            p.add_innovation_focus("")

    def test_remove_innovation_focus_removes(self):
        """Test removing innovation focus."""
        p = Project(innovation_focus="AI, IoT, Blockchain", program_id=1, facility_id=1, title="T", description="D", nature_of_project="Research")
        p.remove_innovation_focus("IoT")
        assert "IoT" not in p.innovation_focus_list
        assert "AI" in p.innovation_focus_list
        assert "Blockchain" in p.innovation_focus_list

    def test_has_testing_requirements_true_false(self):
        """Test testing requirements checking."""
        p1 = Project(testing_requirements="PCB testing", program_id=1, facility_id=1, title="T1", description="D", nature_of_project="Research")
        assert p1.has_testing_requirements()
        
        p2 = Project(testing_requirements="", program_id=1, facility_id=1, title="T2", description="D", nature_of_project="Research")
        assert not p2.has_testing_requirements()

    def test_has_commercialization_plan_true_false(self):
        """Test commercialization plan checking."""
        p1 = Project(commercialization_plan="Market launch plan", program_id=1, facility_id=1, title="T1", description="D", nature_of_project="Research")
        assert p1.has_commercialization_plan()
        
        p2 = Project(commercialization_plan="", program_id=1, facility_id=1, title="T2", description="D", nature_of_project="Research")
        assert not p2.has_commercialization_plan()

    def test_str_returns_title(self):
        """Test string representation returns title."""
        p = Project(title="My Project", program_id=1, facility_id=1, description="D", nature_of_project="Research")
        assert str(p) == "My Project"

    # ========================================================================
    # Project Entity Basic Validation Tests
    # ========================================================================
    
    def test_project_missing_title_raises(self):
        """Test basic validation: Missing title raises error."""
        with pytest.raises(ValueError) as exc:
            Project(program_id=1, facility_id=1, title="", description="D", nature_of_project="Research")
        assert "Project title cannot be empty" in str(exc.value)

    def test_project_missing_description_raises(self):
        """Test basic validation: Missing description raises error."""
        with pytest.raises(ValueError) as exc:
            Project(program_id=1, facility_id=1, title="T", description="", nature_of_project="Research")
        assert "Project description cannot be empty" in str(exc.value)

    def test_project_missing_nature_raises(self):
        """Test basic validation: Missing nature raises error."""
        with pytest.raises(ValueError) as exc:
            Project(program_id=1, facility_id=1, title="T", description="D", nature_of_project="")
        assert "Project nature cannot be empty" in str(exc.value)