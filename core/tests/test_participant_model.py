from django.test import TestCase
from django.core.exceptions import ValidationError
from core.models import Participant
from core.tests.fakes.participant_factory import build_participant, create_participant


class ParticipantModelTest(TestCase):
    """
    Tests for the Participant model.
    Each test follows the AAA pattern and maps directly to business rules from Table 1.6.
    """

    # --------------------------------------------------------------
    # Business Rule 1: Required Fields
    # The FullName, Email, and Affiliation must always be provided.
    # --------------------------------------------------------------
    def test_participant_requires_full_name_email_and_affiliation(self):
        """BR1: Participant must have FullName, Email, and Affiliation."""
        
        # 🅰️ Arrange
        participant = Participant(
            full_name="",  # missing
            email="",  # missing
            affiliation=""  # missing
        )

        # 🅰️ Act & Assert
        with self.assertRaises(ValidationError) as context:
            participant.full_clean()
        
        # Verify the error messages match the specification
        errors = context.exception.message_dict
        self.assertIn('full_name', errors)
        self.assertIn('email', errors)
        self.assertIn('affiliation', errors)

    def test_participant_requires_full_name(self):
        """BR1: FullName is required."""
        
        # 🅰️ Arrange
        participant = Participant(
            full_name="",
            email="test@example.com",
            affiliation="CS"
        )

        # 🅰️ Act & Assert
        with self.assertRaises(ValidationError) as context:
            participant.full_clean()
        
        errors = context.exception.message_dict
        self.assertIn('full_name', errors)
        self.assertIn("Participant.FullName, Participant.Email, and Participant.Affiliation are required", 
                      str(errors['full_name']))

    def test_participant_requires_email(self):
        """BR1: Email is required."""
        
        # 🅰️ Arrange
        participant = Participant(
            full_name="John Doe",
            email="",
            affiliation="CS"
        )

        # 🅰️ Act & Assert
        with self.assertRaises(ValidationError) as context:
            participant.full_clean()
        
        errors = context.exception.message_dict
        self.assertIn('email', errors)

    def test_participant_requires_affiliation(self):
        """BR1: Affiliation is required."""
        
        # 🅰️ Arrange
        participant = Participant(
            full_name="John Doe",
            email="john@example.com",
            affiliation=""
        )

        # 🅰️ Act & Assert
        with self.assertRaises(ValidationError) as context:
            participant.full_clean()
        
        errors = context.exception.message_dict
        self.assertIn('affiliation', errors)
        self.assertIn("Participant.FullName, Participant.Email, and Participant.Affiliation are required", 
                      str(errors['affiliation']))

    # --------------------------------------------------------------
    # Business Rule 2: Email Uniqueness
    # Email must be unique (case-insensitive) across all Participants.
    # --------------------------------------------------------------
    def test_participant_email_must_be_unique_case_insensitive(self):
        """BR2: Email must be unique (case-insensitive) across all Participants."""
        
        # 🅰️ Arrange
        Participant.objects.create(
            full_name="John Doe",
            email="john@example.com",
            affiliation="CS"
        )

        # 🅰️ Act
        duplicate = Participant(
            full_name="Jane Doe",
            email="JOHN@example.com",  # same email, different case
            affiliation="SE"
        )

        # 🅰️ Assert
        with self.assertRaises(ValidationError) as context:
            duplicate.full_clean()
        
        errors = context.exception.message_dict
        self.assertIn('email', errors)
        self.assertIn("Participant.Email already exists", str(errors['email']))

    def test_participant_email_uniqueness_allows_same_participant(self):
        """BR2: Email uniqueness check should allow updating the same participant."""
        
        # 🅰️ Arrange
        participant = Participant.objects.create(
            full_name="John Doe",
            email="john@example.com",
            affiliation="CS"
        )

        # 🅰️ Act - Update the same participant
        participant.full_name = "John D. Doe"
        
        # 🅰️ Assert - Should not raise ValidationError
        try:
            participant.full_clean()
            participant.save()
        except ValidationError:
            self.fail("Should allow updating the same participant with the same email")

    # --------------------------------------------------------------
    # Business Rule 3: Specialization Requirement
    # CrossSkillTrained can only be true if Specialization is set.
    # --------------------------------------------------------------
    def test_cross_skill_trained_requires_specialization(self):
        """BR3: CrossSkillTrained can only be true if Specialization is set."""
        
        # 🅰️ Arrange
        participant = Participant(
            full_name="Jane Doe",
            email="jane@example.com",
            affiliation="Engineering",
            specialization=None,  # No specialization
            cross_skill_trained=True  # But cross-skill flag is set
        )

        # 🅰️ Act & Assert
        with self.assertRaises(ValidationError) as context:
            participant.full_clean()
        
        errors = context.exception.message_dict
        self.assertIn('cross_skill_trained', errors)
        self.assertIn("Cross-skill flag requires Specialization", str(errors['cross_skill_trained']))

    def test_cross_skill_trained_with_empty_specialization_raises(self):
        """BR3: CrossSkillTrained requires non-empty Specialization."""
        
        # 🅰️ Arrange
        participant = Participant(
            full_name="Jane Doe",
            email="jane@example.com",
            affiliation="Engineering",
            specialization="",  # Empty specialization
            cross_skill_trained=True
        )

        # 🅰️ Act & Assert
        with self.assertRaises(ValidationError) as context:
            participant.full_clean()
        
        errors = context.exception.message_dict
        self.assertIn('cross_skill_trained', errors)

    def test_cross_skill_trained_with_specialization_valid(self):
        """BR3: CrossSkillTrained is valid when Specialization is set."""
        
        # 🅰️ Arrange & Act
        participant = Participant.objects.create(
            full_name="Jane Doe",
            email="jane@example.com",
            affiliation="Engineering",
            specialization="Software",
            cross_skill_trained=True
        )

        # 🅰️ Assert
        self.assertTrue(participant.cross_skill_trained)
        self.assertEqual(participant.specialization, "Software")

    def test_cross_skill_trained_false_without_specialization_valid(self):
        """BR3: CrossSkillTrained=False is valid even without Specialization."""
        
        # 🅰️ Arrange & Act
        participant = Participant.objects.create(
            full_name="Bob Smith",
            email="bob@example.com",
            affiliation="CS",
            specialization=None,
            cross_skill_trained=False
        )

        # 🅰️ Assert
        self.assertFalse(participant.cross_skill_trained)
        self.assertIsNone(participant.specialization)

    # --------------------------------------------------------------
    # Business Rule 4: Auto-generated ID
    # Saving a Participant without ID should generate 'PT-001'.
    # --------------------------------------------------------------
    def test_participant_id_auto_generated(self):
        """BR4: Participant without ID should auto-generate PT-001."""
        
        # 🅰️ Arrange
        participant = Participant(
            full_name="First Participant",
            email="first@example.com",
            affiliation="CS"
        )

        # 🅰️ Act
        participant.save()

        # 🅰️ Assert
        self.assertEqual(participant.participant_id, "PT-001")

    # --------------------------------------------------------------
    # Business Rule 5: Sequential ID Generation
    # IDs should increment (PT-001 → PT-002 → PT-003 ...).
    # --------------------------------------------------------------
    def test_participant_id_increments(self):
        """BR5: Each new Participant ID should increment sequentially."""
        
        # 🅰️ Arrange
        Participant.objects.create(
            full_name="First Participant",
            email="first@example.com",
            affiliation="CS"
        )

        # 🅰️ Act
        second = Participant.objects.create(
            full_name="Second Participant",
            email="second@example.com",
            affiliation="SE"
        )

        # 🅰️ Assert
        self.assertEqual(second.participant_id, "PT-002")

    # --------------------------------------------------------------
    # Business Rule 6: Manual ID Preservation
    # If an ID is manually set, it should not be changed.
    # --------------------------------------------------------------
    def test_manual_participant_id_respected(self):
        """BR6: Manually provided Participant ID must remain unchanged."""
        
        # 🅰️ Arrange
        participant = Participant(
            full_name="Custom Participant",
            email="custom@example.com",
            affiliation="Engineering",
            participant_id="PT-999"
        )

        # 🅰️ Act
        participant.save()

        # 🅰️ Assert
        self.assertEqual(participant.participant_id, "PT-999")

    # --------------------------------------------------------------
    # Business Rule 7: Valid Affiliation Choices
    # Test all valid affiliations are accepted.
    # --------------------------------------------------------------
    def test_valid_affiliations_accepted(self):
        """BR7: All valid affiliations should be accepted."""
        
        valid_affiliations = ['CS', 'SE', 'Engineering', 'Other']
        
        for idx, affiliation in enumerate(valid_affiliations):
            # 🅰️ Arrange & Act
            participant = Participant.objects.create(
                full_name=f"Participant {idx}",
                email=f"participant{idx}@example.com",
                affiliation=affiliation
            )
            
            # 🅰️ Assert
            self.assertEqual(participant.affiliation, affiliation)

    # --------------------------------------------------------------
    # Business Rule 8: Valid Specialization Choices
    # Test all valid specializations are accepted.
    # --------------------------------------------------------------
    def test_valid_specializations_accepted(self):
        """BR8: All valid specializations should be accepted."""
        
        valid_specializations = ['Software', 'Hardware', 'Business']
        
        for idx, specialization in enumerate(valid_specializations):
            # 🅰️ Arrange & Act
            participant = Participant.objects.create(
                full_name=f"Specialist {idx}",
                email=f"specialist{idx}@example.com",
                affiliation="CS",
                specialization=specialization
            )
            
            # 🅰️ Assert
            self.assertEqual(participant.specialization, specialization)

    # --------------------------------------------------------------
    # Business Rule 9: Valid Institution Choices
    # Test all valid institutions are accepted.
    # --------------------------------------------------------------
    def test_valid_institutions_accepted(self):
        """BR9: All valid institutions should be accepted."""
        
        valid_institutions = ['SCIT', 'CEDAT', 'UniPod', 'UIRI', 'Lwera']
        
        for idx, institution in enumerate(valid_institutions):
            # 🅰️ Arrange & Act
            participant = Participant.objects.create(
                full_name=f"Member {idx}",
                email=f"member{idx}@example.com",
                affiliation="CS",
                institution=institution
            )
            
            # 🅰️ Assert
            self.assertEqual(participant.institution, institution)

    # --------------------------------------------------------------
    # Business Rule 10: String Representation
    # The __str__ method should return the full_name.
    # --------------------------------------------------------------
    def test_str_returns_full_name(self):
        """BR10: String representation should return the full_name."""
        
        # 🅰️ Arrange & Act
        participant = Participant.objects.create(
            full_name="John Doe",
            email="john@example.com",
            affiliation="CS"
        )
        
        # 🅰️ Assert
        self.assertEqual(str(participant), "John Doe")

    # --------------------------------------------------------------
    # Business Rule 11: Email Format Validation
    # Email field should validate proper email format.
    # --------------------------------------------------------------
    def test_invalid_email_format_raises(self):
        """BR11: Email must be in valid email format."""
        
        # 🅰️ Arrange
        participant = Participant(
            full_name="John Doe",
            email="not-an-email",  # Invalid format
            affiliation="CS"
        )

        # 🅰️ Act & Assert
        with self.assertRaises(ValidationError):
            participant.full_clean()

    # --------------------------------------------------------------
    # Business Rule 12: Optional Specialization
    # Specialization can be null/blank when cross_skill_trained is False.
    # --------------------------------------------------------------
    def test_specialization_optional_when_not_cross_skilled(self):
        """BR12: Specialization is optional when not cross-skilled."""
        
        # 🅰️ Arrange & Act
        participant = Participant.objects.create(
            full_name="Basic Participant",
            email="basic@example.com",
            affiliation="Other",
            specialization=None,
            cross_skill_trained=False
        )

        # 🅰️ Assert
        self.assertIsNone(participant.specialization)
        self.assertFalse(participant.cross_skill_trained)



class ParticipantFactoryTests(TestCase):

    def test_required_fields_raise_validation_error(self):
        # build unsaved participant missing required fields
        p = build_participant(full_name="", email="", affiliation="")
        with self.assertRaises(ValidationError) as ctx:
            p.full_clean()
        errors = ctx.exception.message_dict
        self.assertIn('full_name', errors)
        self.assertIn('email', errors)
        self.assertIn('affiliation', errors)

    def test_email_case_insensitive_uniqueness_validated(self):
        # create first participant
        create_participant(full_name="John Doe", email="john@example.com", affiliation="CS")

        # duplicate with different case
        duplicate = build_participant(full_name="Jane Doe", email="JOHN@example.com", affiliation="SE")
        with self.assertRaises(ValidationError) as ctx:
            duplicate.full_clean()
        errors = ctx.exception.message_dict
        self.assertIn('email', errors)
        self.assertIn('Participant.Email already exists', str(errors['email']))

    def test_cross_skill_requires_specialization(self):
        # cross_skill_trained True without specialization should fail
        p = build_participant(cross_skill_trained=True, specialization=None)
        with self.assertRaises(ValidationError) as ctx:
            p.full_clean()
        errors = ctx.exception.message_dict
        self.assertIn('cross_skill_trained', errors)
        self.assertIn('Cross-skill flag requires Specialization', str(errors['cross_skill_trained']))

    def test_cross_skill_with_specialization_passes(self):
        p = create_participant(cross_skill_trained=True, specialization="Software")
        # saved, should have valid cross-skill status
        self.assertTrue(p.cross_skill_trained)
        self.assertEqual(p.specialization, "Software")