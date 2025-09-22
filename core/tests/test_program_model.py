from django.test import TestCase
from core.models import Program

class ProgramModelTest(TestCase):
    def test_program_id_auto_generated(self):
        """Saving a Program without program_id should generate Pg-001"""
        program = Program.objects.create(
            name="AI Program",
            description="AI and ML research",
            national_alignment="NDPIII",
            focus_areas="IoT",
            phases="Prototyping"
        )
        self.assertEqual(program.program_id, "Pg-001")

    def test_program_id_increments(self):
        """Subsequent programs should increment the program_id"""
        Program.objects.create(
            name="First Program",
            description="Test 1",
            national_alignment="NDPIII",
            focus_areas="IoT",
            phases="Cross-Skilling"
        )
        second = Program.objects.create(
            name="Second Program",
            description="Test 2",
            national_alignment="Roadmap",
            focus_areas="automation",
            phases="Collaboration"
        )
        self.assertEqual(second.program_id, "Pg-002")

    def test_manual_program_id_respected(self):
        """If program_id is manually provided, it should not be overridden"""
        program = Program.objects.create(
            name="Custom Program",
            description="Manual ID test",
            national_alignment="NDPIII",
            focus_areas="IoT",
            phases="Technical Skills",
            program_id="Pg-999"
        )
        self.assertEqual(program.program_id, "Pg-999")
