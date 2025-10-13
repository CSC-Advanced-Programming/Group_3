"""
Django ORM implementation of OutcomeRepositoryInterface.
"""
from typing import List, Optional
from django.db.models import Q
from core.application.interfaces.outcome_repository import OutcomeRepositoryInterface
from core.domain.entities.outcome import Outcome
from core.infrastructure.models.django_models import DjangoOutcome


class DjangoOutcomeRepository(OutcomeRepositoryInterface):
    """
    Django ORM implementation of Outcome repository.
    """

    def _to_entity(self, django_outcome: DjangoOutcome) -> Outcome:
        """Convert Django model to domain entity."""
        return Outcome(
            id=django_outcome.id,
            outcome_id=django_outcome.outcome_id,
            project_id=django_outcome.project_id,
            title=django_outcome.title,
            description=django_outcome.description,
            artifact_link=django_outcome.artifact_link,
            outcome_type=django_outcome.outcome_type,
            quality_certification=django_outcome.quality_certification,
            commercialization_status=django_outcome.commercialization_status,
            created_at=django_outcome.created_at,
            updated_at=django_outcome.updated_at
        )

    def _to_django_model(self, outcome: Outcome, django_outcome: Optional[DjangoOutcome] = None) -> DjangoOutcome:
        """Convert domain entity to Django model."""
        if django_outcome is None:
            django_outcome = DjangoOutcome()
        
        if outcome.id:
            django_outcome.id = outcome.id
        django_outcome.outcome_id = outcome.outcome_id
        django_outcome.project_id = outcome.project_id
        django_outcome.title = outcome.title
        django_outcome.description = outcome.description
        django_outcome.artifact_link = outcome.artifact_link
        django_outcome.outcome_type = outcome.outcome_type
        django_outcome.quality_certification = outcome.quality_certification
        django_outcome.commercialization_status = outcome.commercialization_status
        
        return django_outcome

    def save(self, outcome: Outcome) -> Outcome:
        """Save an outcome entity."""
        # Convert to Django model and save
        django_outcome = self._to_django_model(outcome)
        django_outcome.save()
        
        # Convert back to entity and return
        return self._to_entity(django_outcome)

    def get_by_id(self, outcome_id: int) -> Optional[Outcome]:
        """Retrieve an outcome by its ID."""
        try:
            django_outcome = DjangoOutcome.objects.select_related('project').get(id=outcome_id)
            return self._to_entity(django_outcome)
        except DjangoOutcome.DoesNotExist:
            return None

    def get_by_outcome_id(self, outcome_id: str) -> Optional[Outcome]:
        """Retrieve an outcome by its outcome_id field."""
        try:
            django_outcome = DjangoOutcome.objects.select_related('project').get(outcome_id=outcome_id)
            return self._to_entity(django_outcome)
        except DjangoOutcome.DoesNotExist:
            return None

    def get_all(self) -> List[Outcome]:
        """Retrieve all outcomes."""
        django_outcomes = DjangoOutcome.objects.select_related('project').all()
        return [self._to_entity(do) for do in django_outcomes]

    def get_by_project_id(self, project_id: int) -> List[Outcome]:
        """Get outcomes by project ID."""
        django_outcomes = DjangoOutcome.objects.select_related('project').filter(project_id=project_id)
        return [self._to_entity(do) for do in django_outcomes]

    def delete(self, outcome_id: int) -> bool:
        """Delete an outcome by ID."""
        try:
            django_outcome = DjangoOutcome.objects.get(id=outcome_id)
            django_outcome.delete()
            return True
        except DjangoOutcome.DoesNotExist:
            return False

    def update(self, outcome: Outcome) -> Outcome:
        """Update an existing outcome."""
        if not outcome.id:
            raise ValueError("Outcome ID is required for update")
        
        try:
            django_outcome = DjangoOutcome.objects.get(id=outcome.id)
            django_outcome = self._to_django_model(outcome, django_outcome)
            django_outcome.save()
            return self._to_entity(django_outcome)
        except DjangoOutcome.DoesNotExist:
            raise ValueError(f"Outcome with ID {outcome.id} not found")

    def search(self, query: str) -> List[Outcome]:
        """Search outcomes by query string."""
        django_outcomes = DjangoOutcome.objects.select_related('project').filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(outcome_type__icontains=query) |
            Q(quality_certification__icontains=query) |
            Q(commercialization_status__icontains=query)
        )
        return [self._to_entity(do) for do in django_outcomes]

    def get_by_outcome_type(self, outcome_type: str) -> List[Outcome]:
        """Get outcomes by type."""
        django_outcomes = DjangoOutcome.objects.select_related('project').filter(outcome_type__iexact=outcome_type)
        return [self._to_entity(do) for do in django_outcomes]

    def get_by_commercialization_status(self, status: str) -> List[Outcome]:
        """Get outcomes by commercialization status."""
        django_outcomes = DjangoOutcome.objects.select_related('project').filter(commercialization_status__iexact=status)
        return [self._to_entity(do) for do in django_outcomes]

    def get_certified_outcomes(self) -> List[Outcome]:
        """Get all certified outcomes."""
        django_outcomes = DjangoOutcome.objects.select_related('project').exclude(
            Q(quality_certification__isnull=True) | Q(quality_certification__exact='')
        )
        return [self._to_entity(do) for do in django_outcomes]

    def get_outcomes_with_artifacts(self) -> List[Outcome]:
        """Get outcomes that have artifact links."""
        django_outcomes = DjangoOutcome.objects.select_related('project').exclude(
            Q(artifact_link__isnull=True) | Q(artifact_link__exact='')
        )
        return [self._to_entity(do) for do in django_outcomes]

    def get_tangible_deliverables(self) -> List[Outcome]:
        """Get tangible deliverable outcomes (CAD, PCB, Prototype)."""
        django_outcomes = DjangoOutcome.objects.select_related('project').filter(
            outcome_type__in=['CAD', 'PCB', 'Prototype']
        )
        return [self._to_entity(do) for do in django_outcomes]

    def get_documentation_outcomes(self) -> List[Outcome]:
        """Get documentation outcomes (Reports, Business Plans)."""
        django_outcomes = DjangoOutcome.objects.select_related('project').filter(
            outcome_type__in=['Report', 'Business Plan']
        )
        return [self._to_entity(do) for do in django_outcomes]

    def get_ready_for_commercialization(self) -> List[Outcome]:
        """Get outcomes ready for commercialization."""
        # Use the business logic from the entity
        all_outcomes = self.get_all()
        return [outcome for outcome in all_outcomes if outcome.is_ready_for_commercialization()]

    def get_demoed_outcomes(self) -> List[Outcome]:
        """Get outcomes that have been demoed."""
        django_outcomes = DjangoOutcome.objects.select_related('project').filter(commercialization_status__iexact='Demoed')
        return [self._to_entity(do) for do in django_outcomes]

    def get_market_linked_outcomes(self) -> List[Outcome]:
        """Get outcomes that are market linked."""
        django_outcomes = DjangoOutcome.objects.select_related('project').filter(commercialization_status__iexact='Market Linked')
        return [self._to_entity(do) for do in django_outcomes]

    def get_launched_outcomes(self) -> List[Outcome]:
        """Get outcomes that have been launched."""
        django_outcomes = DjangoOutcome.objects.select_related('project').filter(commercialization_status__iexact='Launched')
        return [self._to_entity(do) for do in django_outcomes]