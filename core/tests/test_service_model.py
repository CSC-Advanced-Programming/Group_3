from django.test import TestCase
from django.core.exceptions import ValidationError
from core.models import Service, Facility

class ServiceModelTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.facility = Facility.objects.create(
            name="Test Facility",
            capabilities="CNC",
            facility_type="Lab"
        )

    def test_service_id_auto_generated(self):
        """Test that service_id is auto-generated with correct format"""
        service = Service.objects.create(
            facility=self.facility,
            name="Test Service",
            description="Test Description",
            category="Machining",
            skill_type="Hardware"
        )
        self.assertTrue(service.service_id.startswith('S-'))
        
    def test_service_categories(self):
        """Test service categories are validated correctly"""
        service = Service.objects.create(
            name="Test Service",
            category="Machining"
        )
        self.assertEqual(service.category, "Machining")
        
        service.category = "Invalid Category"
        with self.assertRaises(ValidationError):
            service.full_clean()

    def test_skill_types(self):
        """Test skill types are validated correctly"""
        service = Service.objects.create(
            name="Test Service",
            skill_type="Hardware"
        )
        self.assertEqual(service.skill_type, "Hardware")
        
        service.skill_type = "Invalid Type"
        with self.assertRaises(ValidationError):
            service.full_clean()

    def test_service_with_facility(self):
        """Test service can be associated with a facility"""
        service = Service.objects.create(
            facility=self.facility,
            name="Test Service",
            category="Testing"
        )
        self.assertEqual(service.facility, self.facility)
        self.assertEqual(self.facility.services.first(), service)

    def test_service_str_representation(self):
        """Test the string representation of the service"""
        service = Service.objects.create(
            name="Test Service"
        )
        self.assertEqual(str(service), "Test Service")

    def test_optional_fields(self):
        """Test that optional fields can be null/blank"""
        service = Service.objects.create(
            name="Test Service"
        )
        self.assertIsNone(service.description)
        self.assertIsNone(service.category)
        self.assertIsNone(service.skill_type)