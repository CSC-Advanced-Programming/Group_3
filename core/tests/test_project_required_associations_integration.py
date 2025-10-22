"""
Enhanced integration tests for Project Required Associations business rule.
Uses fake repository to test more realistic scenarios.
"""
import pytest
from core.domain.entities.project import Project
from core.tests.fakes.fake_project_repo import FakeProjectRepository, fake_project_repo


class TestProjectRequiredAssociationsIntegration:
    """Integration tests for Project Required Associations rule using fake repository."""

    def test_save_project_without_program_raises_error(self, fake_project_repo: FakeProjectRepository):
        """Test that creating a project without program_id raises ValueError."""
        with pytest.raises(ValueError) as exc:
            Project(
                program_id=None,  # Missing program
                facility_id=1,
                title="Test Project",
                description="Test description",
                nature_of_project="Research"
            )
        assert "Project.ProgramId and Project.FacilityId are required." in str(exc.value)

    def test_save_project_without_facility_raises_error(self, fake_project_repo: FakeProjectRepository):
        """Test that creating a project without facility_id raises ValueError."""
        with pytest.raises(ValueError) as exc:
            Project(
                program_id=1,
                facility_id=None,  # Missing facility
                title="Test Project",
                description="Test description",
                nature_of_project="Research"
            )
        assert "Project.ProgramId and Project.FacilityId are required." in str(exc.value)

    def test_save_project_with_both_associations_succeeds(self, fake_project_repo: FakeProjectRepository):
        """Test that saving a project with both associations succeeds."""
        project = Project(
            program_id=1,
            facility_id=2,
            title="Valid Project",
            description="Valid description",
            nature_of_project="Research"
        )
        
        saved_project = fake_project_repo.save(project)
        
        assert saved_project.id is not None
        assert saved_project.program_id == 1
        assert saved_project.facility_id == 2
        assert saved_project.title == "Valid Project"

    def test_update_project_to_remove_program_association_raises_error(self, fake_project_repo: FakeProjectRepository):
        """Test that updating a project to remove program association raises error."""
        # Create and save valid project
        project = Project(
            program_id=1,
            facility_id=2,
            title="Valid Project",
            description="Valid description",
            nature_of_project="Research"
        )
        saved_project = fake_project_repo.save(project)
        
        # Try to update with missing program_id
        saved_project.program_id = None
        
        with pytest.raises(ValueError) as exc:
            fake_project_repo.update(saved_project)
        assert "Project.ProgramId and Project.FacilityId are required." in str(exc.value)

    def test_update_project_to_remove_facility_association_raises_error(self, fake_project_repo: FakeProjectRepository):
        """Test that updating a project to remove facility association raises error."""
        # Create and save valid project
        project = Project(
            program_id=1,
            facility_id=2,
            title="Valid Project",
            description="Valid description",
            nature_of_project="Research"
        )
        saved_project = fake_project_repo.save(project)
        
        # Try to update with missing facility_id
        saved_project.facility_id = None
        
        with pytest.raises(ValueError) as exc:
            fake_project_repo.update(saved_project)
        assert "Project.ProgramId and Project.FacilityId are required." in str(exc.value)

    def test_update_project_with_valid_associations_succeeds(self, fake_project_repo: FakeProjectRepository):
        """Test that updating a project with valid associations succeeds."""
        # Create and save valid project
        project = Project(
            program_id=1,
            facility_id=2,
            title="Valid Project",
            description="Valid description",
            nature_of_project="Research"
        )
        saved_project = fake_project_repo.save(project)
        
        # Update with different but still valid associations
        saved_project.program_id = 3
        saved_project.facility_id = 4
        saved_project.description = "Updated description"
        
        updated_project = fake_project_repo.update(saved_project)
        
        assert updated_project.program_id == 3
        assert updated_project.facility_id == 4
        assert updated_project.description == "Updated description"

    def test_get_projects_by_program_and_facility(self, fake_project_repo: FakeProjectRepository):
        """Test repository methods for filtering by associations."""
        # Create projects with different associations
        project1 = Project(
            program_id=1, facility_id=1, title="Project A",
            description="Desc A", nature_of_project="Research"
        )
        project2 = Project(
            program_id=1, facility_id=2, title="Project B",
            description="Desc B", nature_of_project="Prototype"
        )
        project3 = Project(
            program_id=2, facility_id=1, title="Project C",
            description="Desc C", nature_of_project="Applied"
        )
        
        fake_project_repo.save(project1)
        fake_project_repo.save(project2)
        fake_project_repo.save(project3)
        
        # Test filtering by program
        program1_projects = fake_project_repo.get_by_program_id(1)
        assert len(program1_projects) == 2
        assert all(p.program_id == 1 for p in program1_projects)
        
        # Test filtering by facility
        facility1_projects = fake_project_repo.get_by_facility_id(1)
        assert len(facility1_projects) == 2
        assert all(p.facility_id == 1 for p in facility1_projects)