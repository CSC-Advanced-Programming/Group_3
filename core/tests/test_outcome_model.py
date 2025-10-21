from django.test import TestCase
from django.core.exceptions import ValidationError
from core.models import Outcome, Project


class OutcomeModelTest(TestCase):
    """Tests for the Outcome model and its business rules."""

    def test_outcome_id_auto_generated(self):
        """BR: Saving an Outcome without ID should generate 'O-001'."""
        outcome = Outcome.objects.create(title="First")
        self.assertEqual(outcome.outcome_id, "O-001")

    def test_outcome_id_increments(self):
        """BR: Each new Outcome ID should increment sequentially."""
        Outcome.objects.create(title="One")
        second = Outcome.objects.create(title="Two")
        self.assertEqual(second.outcome_id, "O-002")

    def test_manual_outcome_id_respected(self):
        """BR: Manually provided Outcome ID must remain unchanged."""
        outcome = Outcome(title="Manual", outcome_id="O-999")
        outcome.save()
        self.assertEqual(outcome.outcome_id, "O-999")

    def test_artifact_link_invalid_url_raises(self):
        """Artifact link must be a valid URL (URLField validation)."""
        outcome = Outcome(title="Bad URL", artifact_link="not-a-url")
        with self.assertRaises(ValidationError):
            outcome.full_clean()

    def test_outcome_type_invalid_choice_raises(self):
        """Outcome type must be one of the allowed choices."""
        outcome = Outcome(title="Bad Type", outcome_type="Unknown")
        with self.assertRaises(ValidationError):
            outcome.full_clean()

    def test_commercialization_status_invalid_choice_raises(self):
        """Commercialization status must be within allowed choices if set."""
        outcome = Outcome(title="Bad Status", commercialization_status="NotAStatus")
        with self.assertRaises(ValidationError):
            outcome.full_clean()

    def test_project_nullable_allows_none(self):
        """An Outcome can be saved without linking to a Project."""
        outcome = Outcome.objects.create(title="No Project", project=None)
        self.assertIsNone(outcome.project)

    def test_str_returns_title(self):
        outcome = Outcome.objects.create(title="Outcome Title")
        self.assertEqual(str(outcome), "Outcome Title")
