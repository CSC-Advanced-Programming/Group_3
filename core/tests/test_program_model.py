from django.test import TestCase
from django.core.exceptions import ValidationError
from core.models import Program, Project

class ProgramModelTest(TestCase):
    """
    Tests for the Program model.
    Each test follows the AAA pattern and maps directly to business rules.
    """

    # --------------------------------------------------------------
    # Business Rule 1: Required Fields
    # The Name and Description must always be provided.
    # --------------------------------------------------------------
    def test_program_requires_name_and_description(self):
        """BR1: Program must have both name and description."""
        
        # 🅰️ Arrange
        program = Program(
            name="",  # missing
            description="",  # missing
            national_alignment="NDPIII",
            focus_areas="IoT",
            phases="Prototyping"
        )

        # 🅰️ Act & Assert
        # Using full_clean() to trigger model field validation
        with self.assertRaises(ValidationError):
            program.full_clean()

    # --------------------------------------------------------------
    # Business Rule 2: Uniqueness
    # Program name must be unique (case-insensitive).
    # --------------------------------------------------------------
    def test_program_name_must_be_unique(self):
        """BR2: Program name must be unique (case-insensitive)."""
        
        # 🅰️ Arrange
        Program.objects.create(
            name="Smart Farming",
            description="IoT in agriculture",
            national_alignment="NDPIII",
            focus_areas="IoT",
            phases="Prototyping"
        )

        # 🅰️ Act
        duplicate = Program(
            name="smart farming",  # same name, different case
            description="Duplicate entry",
            national_alignment="NDPIII",
            focus_areas="IoT",
            phases="Cross-Skilling"
        )

        # 🅰️ Assert
        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    # --------------------------------------------------------------
    # Business Rule 3: National Alignment
    # When FocusAreas is set, NationalAlignment must also be valid.
    # --------------------------------------------------------------
    def test_focus_areas_require_national_alignment(self):
        """BR3: FocusAreas require valid NationalAlignment."""
        
        # 🅰️ Arrange
        program = Program(
            name="Unaligned Program",
            description="Focus area without national alignment",
            national_alignment=None,  # missing
            focus_areas="IoT",
            phases="Technical Skills"
        )

        # 🅰️ Act & Assert
        with self.assertRaises(ValidationError):
            program.full_clean()

    # --------------------------------------------------------------
    # Business Rule 4: Lifecycle Protection
    # Programs cannot be deleted if they have associated Projects.
    # --------------------------------------------------------------
    def test_program_with_projects_cannot_be_deleted(self):
        """BR4: Program cannot be deleted if Projects are linked."""
        
        # 🅰️ Arrange
        program = Program.objects.create(
            name="Main Program",
            description="Program linked to project",
            national_alignment="NDPIII",
            focus_areas="IoT",
            phases="Prototyping"
        )
        Project.objects.create(
            title="Linked Project",
            description="Testing lifecycle protection",
            program=program
        )

        # 🅰️ Act & Assert
        with self.assertRaises(ValidationError):
            program.delete()

    # --------------------------------------------------------------
    # Business Rule 5: Auto-generated ID
    # Saving a Program without ID should generate 'Pg-001'.
    # --------------------------------------------------------------
    def test_program_id_auto_generated(self):
        """BR5: Program without ID should auto-generate Pg-001."""
        
        # 🅰️ Arrange
        program = Program(
            name="AI Program",
            description="AI and ML research",
            national_alignment="NDPIII",
            focus_areas="IoT",
            phases="Prototyping"
        )

        # 🅰️ Act
        program.save()

        # 🅰️ Assert
        self.assertEqual(program.program_id, "Pg-001")

    # --------------------------------------------------------------
    # Business Rule 6: Sequential ID Generation
    # IDs should increment (Pg-001 → Pg-002 → Pg-003 ...).
    # --------------------------------------------------------------
    def test_program_id_increments(self):
        """BR6: Each new Program ID should increment sequentially."""
        
        # 🅰️ Arrange
        Program.objects.create(
            name="First Program",
            description="Test 1",
            national_alignment="NDPIII",
            focus_areas="IoT",
            phases="Cross-Skilling"
        )

        # 🅰️ Act
        second = Program.objects.create(
            name="Second Program",
            description="Test 2",
            national_alignment="NDPIII",
            focus_areas="automation",
            phases="Collaboration"
        )

        # 🅰️ Assert
        self.assertEqual(second.program_id, "Pg-002")

    # --------------------------------------------------------------
    # Business Rule 7: Manual ID Preservation
    # If an ID is manually set, it should not be changed.
    # --------------------------------------------------------------
    def test_manual_program_id_respected(self):
        """BR7: Manually provided Program ID must remain unchanged."""
        
        # 🅰️ Arrange
        program = Program(
            name="Custom Program",
            description="Manual ID test",
            national_alignment="NDPIII",
            focus_areas="IoT",
            phases="Technical Skills",
            program_id="Pg-999"
        )

        # 🅰️ Act
        program.save()

        # 🅰️ Assert
        self.assertEqual(program.program_id, "Pg-999")
