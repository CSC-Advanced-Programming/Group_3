from django.test import TestCase
from django.core.exceptions import ValidationError
from core.models import Equipment, Facility

class EquipmentModelTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.facility = Facility.objects.create(
            name="Test Facility",
            capabilities="CNC",
            facility_type="Lab"
        )

    def test_equipment_id_auto_generated(self):
        """Test that equipment_id is auto-generated with correct format"""
        equipment = Equipment.objects.create(
            facility=self.facility,
            name="Test Equipment",
            capabilities="Testing Capability",
            usage_domain="Electronics",
            support_phase="Training"
        )
        self.assertTrue(equipment.equipment_id.startswith('E-'))

    def test_usage_domain_validation(self):
        """Test usage domain choices are validated"""
        equipment = Equipment.objects.create(
            name="Test Equipment",
            usage_domain="Electronics"
        )
        self.assertEqual(equipment.usage_domain, "Electronics")
        
        equipment.usage_domain = "Invalid Domain"
        with self.assertRaises(ValidationError):
            equipment.full_clean()

    def test_support_phase_validation(self):
        """Test support phase choices are validated"""
        equipment = Equipment.objects.create(
            name="Test Equipment",
            support_phase="Training"
        )
        self.assertEqual(equipment.support_phase, "Training")
        
        equipment.support_phase = "Invalid Phase"
        with self.assertRaises(ValidationError):
            equipment.full_clean()

    def test_equipment_with_facility(self):
        """Test equipment can be associated with a facility"""
        equipment = Equipment.objects.create(
            facility=self.facility,
            name="Test Equipment"
        )
        self.assertEqual(equipment.facility, self.facility)
        self.assertEqual(self.facility.equipment.first(), equipment)

    def test_equipment_str_representation(self):
        """Test the string representation of the equipment"""
        equipment = Equipment.objects.create(
            name="Test Equipment"
        )
        self.assertEqual(str(equipment), "Test Equipment")

    def test_optional_fields(self):
        """Test that optional fields can be null/blank"""
        equipment = Equipment.objects.create(
            name="Test Equipment"
        )
        self.assertIsNone(equipment.capabilities)
        self.assertIsNone(equipment.description)
        self.assertIsNone(equipment.inventory_code)
        self.assertIsNone(equipment.usage_domain)
        self.assertIsNone(equipment.support_phase)