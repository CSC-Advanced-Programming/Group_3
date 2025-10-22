"""
Enhanced integration tests for Project business rules using fake repository.
Demonstrates more realistic testing scenarios with repository patterns.
"""
import pytest
from core.domain.entities.project import Project
from core.tests.fakes.fake_project_repo import FakeProjectRepository, fake_project_repo


class TestProjectBusinessRulesIntegration:
    """Integration tests for all Project business rules using fake repository."""

    def test_required_associations_rule_with_repository(self, fake_project_repo: FakeProjectRepository):
        """Test Required Associations rule through repository operations."""
        # Test 1: Invalid project creation raises error at entity level
        with pytest.raises(ValueError) as exc:
            Project(
                program_id=None,
                facility_id=1,
                title="Invalid Project",
                description="Missing program",
                nature_of_project="Research"
            )
        assert "Project.ProgramId and Project.FacilityId are required." in str(exc.value)
        
        # Test 2: Valid project with both associations
        valid_project = Project(
            program_id=1,
            facility_id=2,
            title="Valid Project",
            description="Has both associations",
            nature_of_project="Research"
        )
        
        saved_project = fake_project_repo.save(valid_project)
        assert saved_project.id is not None
        assert saved_project.program_id == 1
        assert saved_project.facility_id == 2

    def test_name_uniqueness_rule_with_repository(self, fake_project_repo: FakeProjectRepository):
        """Test Name Uniqueness rule through repository operations."""
        # Create first project
        project1 = Project(
            program_id=1,
            facility_id=1,
            title="Unique Project",
            description="First project",
            nature_of_project="Research"
        )
        saved_project1 = fake_project_repo.save(project1)
        
        # Try to create second project with same title in same program
        project2 = Project(
            program_id=1,  # Same program
            facility_id=2,
            title="Unique Project",  # Same title
            description="Second project",
            nature_of_project="Prototype"
        )
        
        with pytest.raises(ValueError) as exc:
            fake_project_repo.save(project2)
        assert "A project with this name already exists in this program." in str(exc.value)
        
        # Same title in different program should be allowed
        project3 = Project(
            program_id=2,  # Different program
            facility_id=2,
            title="Unique Project",  # Same title
            description="Third project",
            nature_of_project="Applied"
        )
        
        saved_project3 = fake_project_repo.save(project3)
        assert saved_project3.id is not None

    def test_facility_compatibility_rule_with_repository(self, fake_project_repo: FakeProjectRepository):
        """Test Facility Compatibility rule through repository operations."""
        # Set up facility capabilities
        facility_id = 1
        fake_project_repo.set_facility_capabilities(facility_id, ["CNC", "PCB", "3D printing"])
        
        # Create project with compatible requirements
        compatible_project = Project(
            program_id=1,
            facility_id=facility_id,
            title="Compatible Project",
            description="Project description",
            nature_of_project="Research",
            innovation_focus="CNC, PCB",
            testing_requirements=""
        )
        
        saved_project = fake_project_repo.save(compatible_project)
        
        # Validate compatibility - should pass
        fake_project_repo.validate_facility_compatibility_for_project(saved_project)
        
        # Create project with incompatible requirements
        incompatible_project = Project(
            program_id=1,
            facility_id=facility_id,
            title="Incompatible Project",
            description="Project description",
            nature_of_project="Research",
            innovation_focus="CNC, Advanced AI",  # AI not available
            testing_requirements=""
        )
        
        saved_incompatible = fake_project_repo.save(incompatible_project)
        
        # Validate compatibility - should fail
        with pytest.raises(ValueError) as exc:
            fake_project_repo.validate_facility_compatibility_for_project(saved_incompatible)
        assert "Project requirements not compatible with facility capabilities." in str(exc.value)

    def test_repository_filtering_and_queries(self, fake_project_repo: FakeProjectRepository):
        """Test repository filtering capabilities."""
        # Create projects in different programs and facilities
        projects_data = [
            (1, 1, "Alpha Project", "Research"),
            (1, 2, "Beta Project", "Prototype"),
            (2, 1, "Gamma Project", "Applied"),
            (2, 2, "Delta Project", "Research")
        ]
        
        saved_projects = []
        for program_id, facility_id, title, nature in projects_data:
            project = Project(
                program_id=program_id,
                facility_id=facility_id,
                title=title,
                description=f"Description for {title}",
                nature_of_project=nature
            )
            saved_projects.append(fake_project_repo.save(project))
        
        # Test filtering by program
        program1_projects = fake_project_repo.get_by_program_id(1)
        assert len(program1_projects) == 2
        assert all(p.program_id == 1 for p in program1_projects)
        
        # Test filtering by facility
        facility1_projects = fake_project_repo.get_by_facility_id(1)
        assert len(facility1_projects) == 2
        assert all(p.facility_id == 1 for p in facility1_projects)
        
        # Test getting all titles in program for uniqueness checking
        program1_titles = fake_project_repo.get_all_titles_in_program(1)
        assert "Alpha Project" in program1_titles
        assert "Beta Project" in program1_titles
        assert len(program1_titles) == 2

    def test_project_lifecycle_with_business_rules(self, fake_project_repo: FakeProjectRepository):
        """Test a complete project lifecycle respecting business rules."""
        # Step 1: Create project with required associations
        project = Project(
            program_id=1,
            facility_id=1,
            title="Lifecycle Project",
            description="Complete lifecycle test",
            nature_of_project="Research"
        )
        
        saved_project = fake_project_repo.save(project)
        project_id = saved_project.id
        assert project_id is not None
        
        # Step 2: Validate name uniqueness (get existing titles)
        existing_titles = fake_project_repo.get_all_titles_in_program(1)
        assert "Lifecycle Project" in existing_titles
        
        # Step 3: Try to create duplicate - should fail
        duplicate_project = Project(
            program_id=1,
            facility_id=2,
            title="Lifecycle Project",
            description="Duplicate title",
            nature_of_project="Prototype"
        )
        
        with pytest.raises(ValueError):
            fake_project_repo.save(duplicate_project)
        
        # Step 4: Set up facility capabilities and test compatibility
        fake_project_repo.set_facility_capabilities(1, ["CNC", "PCB", "3D printing"])
        
        # Update project with technical requirements
        saved_project.innovation_focus = "CNC, 3D printing"
        saved_project.testing_requirements = "PCB"
        updated_project = fake_project_repo.update(saved_project)
        
        # Validate facility compatibility
        fake_project_repo.validate_facility_compatibility_for_project(updated_project)
        
        # Step 5: Test repository state
        all_projects = fake_project_repo.get_all()
        assert len(all_projects) == 1
        assert all_projects[0].title == "Lifecycle Project"

    def test_business_rule_validation_methods(self, fake_project_repo: FakeProjectRepository):
        """Test the repository's business rule validation helper methods."""
        # Create a test project
        project = Project(
            program_id=1,
            facility_id=1,
            title="Validation Test Project",
            description="Testing validation methods",
            nature_of_project="Research"
        )
        
        saved_project = fake_project_repo.save(project)
        
        # Test name uniqueness validation
        fake_project_repo.validate_name_uniqueness_for_project(saved_project)  # Should pass
        
        # Test facility compatibility validation (no capabilities set = empty list)
        fake_project_repo.validate_facility_compatibility_for_project(saved_project)  # Should pass (no requirements)
        
        # Set facility capabilities and test again
        fake_project_repo.set_facility_capabilities(1, ["CNC"])
        fake_project_repo.validate_facility_compatibility_for_project(saved_project)  # Should still pass