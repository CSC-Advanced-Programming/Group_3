from django.test import TestCase
from django.urls import reverse
from core.models import Program

class ProgramViewsTest(TestCase):
    def setUp(self):
        self.program = Program.objects.create(
            name="Smart Farming",
            description="IoT in agriculture",
            national_alignment="NDPIII",
            focus_areas="IoT",
            phases="Prototyping"
        )

    def test_program_list_view(self):
        """Program list view should show existing programs"""
        url = reverse("program_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Smart Farming")

    def test_program_detail_view(self):
        """Detail view should show a program and its projects"""
        url = reverse("program_detail", args=[self.program.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Smart Farming")

    def test_program_create_view(self):
        """POST should create a new program"""
        url = reverse("program_create")
        response = self.client.post(url, {
            "name": "Healthcare AI",
            "description": "Diagnostics AI",
            "national_alignment": "Roadmap",
            "focus_areas": "automation",
            "phases": "Cross-Skilling"
        })
        self.assertEqual(response.status_code, 302)  # redirect on success
        self.assertTrue(Program.objects.filter(name="Healthcare AI").exists())

    def test_program_update_view(self):
        """POST should update an existing program"""
        url = reverse("program_update", args=[self.program.pk])
        response = self.client.post(url, {
            "name": "Updated Farming",
            "description": "Updated description",
            "national_alignment": "4IR goals",
            "focus_areas": "renewable energy",
            "phases": "Commercialization"
        })
        self.assertEqual(response.status_code, 302)
        self.program.refresh_from_db()
        self.assertEqual(self.program.name, "Updated Farming")

    def test_program_delete_view(self):
        """POST should delete a program"""
        url = reverse("program_delete", args=[self.program.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Program.objects.filter(pk=self.program.pk).exists())
