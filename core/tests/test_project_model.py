from django.test import TestCase
from django.core.exceptions import ValidationError
from core.models import Project, Program, Facility

class ProjectModelTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.program = Program.objects.create(
            name="Test Program",
            description="Test Description",
            national_alignment="NDPIII",
            focus_areas="IoT",
            phases="Prototyping"
        )
        
        self.facility = Facility.objects.create(
            name="Test Facility",
            capabilities="CNC",
            facility_type="Lab"
        )

    def test_project_id_auto_generated(self):
        """Test that project_id is auto-generated with correct format"""
        project = Project.objects.create(
            program=self.program,
            facility=self.facility,
            title="Test Project",
            description="Test Description",
            nature_of_project="Research"
        )
        self.assertTrue(project.project_id.startswith('P-'))
        self.assertEqual(len(project.project_id), 5)  # P-001 format

    def test_project_id_increments(self):
        """Test that project_id increments correctly"""
        project1 = Project.objects.create(
            title="First Project",
            description="Description 1",
            nature_of_project="Research"
        )
        project2 = Project.objects.create(
            title="Second Project",
            description="Description 2",
            nature_of_project="Research"
        )
        first_id_num = int(project1.project_id.split('-')[1])
        second_id_num = int(project2.project_id.split('-')[1])
        self.assertEqual(second_id_num, first_id_num + 1)

    def test_project_defaults(self):
        """Test default values are set correctly"""
        project = Project.objects.create()
        self.assertEqual(project.title, 'New Project')
        self.assertEqual(project.description, 'Project description')
        self.assertEqual(project.nature_of_project, 'Research')

    def test_project_with_minimum_fields(self):
        """Test project can be created with minimum required fields"""
        project = Project.objects.create(
            title="Minimal Project"
        )
        self.assertTrue(isinstance(project, Project))
        self.assertEqual(project.title, "Minimal Project")

    def test_project_str_representation(self):
        """Test the string representation of the project"""
        project = Project.objects.create(
            title="Test Project"
        )
        self.assertEqual(str(project), "Test Project")

    def test_project_prototype_stage_choices(self):
        """Test that prototype_stage only accepts valid choices"""
        project = Project.objects.create(
            title="Test Project",
            prototype_stage="Concept"
        )
        self.assertEqual(project.prototype_stage, "Concept")
        
        project.prototype_stage = "Invalid Stage"
        with self.assertRaises(ValidationError):
            project.full_clean()