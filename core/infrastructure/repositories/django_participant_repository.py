"""
Django ORM implementation of ParticipantRepositoryInterface.
"""
from typing import List, Optional
from django.db.models import Q
from core.application.interfaces.participant_repository import ParticipantRepositoryInterface
from core.domain.entities.participant import Participant
from core.infrastructure.models.django_models import DjangoParticipant


class DjangoParticipantRepository(ParticipantRepositoryInterface):
    """
    Django ORM implementation of Participant repository.
    """

    def _to_entity(self, django_participant: DjangoParticipant) -> Participant:
        """Convert Django model to domain entity."""
        return Participant(
            id=django_participant.id,
            participant_id=django_participant.participant_id,
            full_name=django_participant.full_name,
            email=django_participant.email,
            affiliation=django_participant.affiliation,
            specialization=django_participant.specialization,
            cross_skill_trained=django_participant.cross_skill_trained,
            institution=django_participant.institution,
            created_at=django_participant.created_at,
            updated_at=django_participant.updated_at
        )

    def _to_django_model(self, participant: Participant, django_participant: Optional[DjangoParticipant] = None) -> DjangoParticipant:
        """Convert domain entity to Django model."""
        if django_participant is None:
            django_participant = DjangoParticipant()
        
        if participant.id:
            django_participant.id = participant.id
        django_participant.participant_id = participant.participant_id
        django_participant.full_name = participant.full_name
        django_participant.email = participant.email
        django_participant.affiliation = participant.affiliation
        django_participant.specialization = participant.specialization
        django_participant.cross_skill_trained = participant.cross_skill_trained
        django_participant.institution = participant.institution
        
        return django_participant

    def save(self, participant: Participant) -> Participant:
        """Save a participant entity."""
        # Validate business rules
        existing_emails = self.get_all_emails(exclude_id=participant.id)
        Participant.validate_email_uniqueness(participant.email, existing_emails)
        
        # Convert to Django model and save
        django_participant = self._to_django_model(participant)
        django_participant.save()
        
        # Convert back to entity and return
        return self._to_entity(django_participant)

    def get_by_id(self, participant_id: int) -> Optional[Participant]:
        """Retrieve a participant by its ID."""
        try:
            django_participant = DjangoParticipant.objects.get(id=participant_id)
            return self._to_entity(django_participant)
        except DjangoParticipant.DoesNotExist:
            return None

    def get_by_participant_id(self, participant_id: str) -> Optional[Participant]:
        """Retrieve a participant by its participant_id field."""
        try:
            django_participant = DjangoParticipant.objects.get(participant_id=participant_id)
            return self._to_entity(django_participant)
        except DjangoParticipant.DoesNotExist:
            return None

    def get_by_email(self, email: str) -> Optional[Participant]:
        """Retrieve a participant by email."""
        try:
            django_participant = DjangoParticipant.objects.get(email__iexact=email)
            return self._to_entity(django_participant)
        except DjangoParticipant.DoesNotExist:
            return None

    def get_all(self) -> List[Participant]:
        """Retrieve all participants."""
        django_participants = DjangoParticipant.objects.all()
        return [self._to_entity(dp) for dp in django_participants]

    def exists_by_email(self, email: str, exclude_id: Optional[int] = None) -> bool:
        """Check if a participant with given email exists."""
        queryset = DjangoParticipant.objects.filter(email__iexact=email)
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return queryset.exists()

    def get_all_emails(self, exclude_id: Optional[int] = None) -> List[str]:
        """Get all participant emails for uniqueness validation."""
        queryset = DjangoParticipant.objects.all()
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        return list(queryset.values_list('email', flat=True))

    def delete(self, participant_id: int) -> bool:
        """Delete a participant by ID."""
        try:
            django_participant = DjangoParticipant.objects.get(id=participant_id)
            django_participant.delete()
            return True
        except DjangoParticipant.DoesNotExist:
            return False

    def update(self, participant: Participant) -> Participant:
        """Update an existing participant."""
        if not participant.id:
            raise ValueError("Participant ID is required for update")
        
        # Validate business rules
        existing_emails = self.get_all_emails(exclude_id=participant.id)
        Participant.validate_email_uniqueness(participant.email, existing_emails)
        
        try:
            django_participant = DjangoParticipant.objects.get(id=participant.id)
            django_participant = self._to_django_model(participant, django_participant)
            django_participant.save()
            return self._to_entity(django_participant)
        except DjangoParticipant.DoesNotExist:
            raise ValueError(f"Participant with ID {participant.id} not found")

    def search(self, query: str) -> List[Participant]:
        """Search participants by query string."""
        django_participants = DjangoParticipant.objects.filter(
            Q(full_name__icontains=query) |
            Q(email__icontains=query) |
            Q(affiliation__icontains=query) |
            Q(specialization__icontains=query) |
            Q(institution__icontains=query)
        )
        return [self._to_entity(dp) for dp in django_participants]

    def get_by_affiliation(self, affiliation: str) -> List[Participant]:
        """Get participants by affiliation."""
        django_participants = DjangoParticipant.objects.filter(affiliation__iexact=affiliation)
        return [self._to_entity(dp) for dp in django_participants]

    def get_by_specialization(self, specialization: str) -> List[Participant]:
        """Get participants by specialization."""
        django_participants = DjangoParticipant.objects.filter(specialization__iexact=specialization)
        return [self._to_entity(dp) for dp in django_participants]

    def get_by_institution(self, institution: str) -> List[Participant]:
        """Get participants by institution."""
        django_participants = DjangoParticipant.objects.filter(institution__iexact=institution)
        return [self._to_entity(dp) for dp in django_participants]

    def get_cross_skill_trained(self) -> List[Participant]:
        """Get all cross-skill trained participants."""
        django_participants = DjangoParticipant.objects.filter(cross_skill_trained=True)
        return [self._to_entity(dp) for dp in django_participants]

    def get_by_technical_background(self) -> List[Participant]:
        """Get participants with technical background."""
        django_participants = DjangoParticipant.objects.filter(
            Q(specialization__icontains='Software') |
            Q(specialization__icontains='Hardware') |
            Q(specialization__icontains='Engineering') |
            Q(affiliation__icontains='CS') |
            Q(affiliation__icontains='SE') |
            Q(affiliation__icontains='Engineering')
        )
        return [self._to_entity(dp) for dp in django_participants]

    def get_by_business_background(self) -> List[Participant]:
        """Get participants with business background."""
        django_participants = DjangoParticipant.objects.filter(specialization__icontains='Business')
        return [self._to_entity(dp) for dp in django_participants]

    def get_available_for_project(self, required_specialization: str) -> List[Participant]:
        """Get participants available for a project requiring specific skills."""
        # Get participants with matching specialization or cross-skill trained
        django_participants = DjangoParticipant.objects.filter(
            Q(specialization__iexact=required_specialization) |
            Q(cross_skill_trained=True)
        )
        return [self._to_entity(dp) for dp in django_participants]