"""Form factory for creating form instances."""
from typing import Type, Optional, Any, Dict

from core.application.interfaces.form_interfaces import (
    FormInterface,
    ProjectFormInterface,
    EquipmentFormInterface,
    ServiceFormInterface,
    ProjectParticipantFormInterface
)
from core.infrastructure.forms.django_forms import (
    DjangoProjectForm,
    DjangoEquipmentForm,
    DjangoServiceForm,
    DjangoParticipantForm,
    DjangoProjectParticipantForm,
    DjangoOutcomeForm
)


class FormFactory:
    """Factory for creating form instances."""

    @staticmethod
    def create_project_form(data: Optional[Dict] = None, instance: Optional[Any] = None) -> ProjectFormInterface:
        """Create a project form instance."""
        return DjangoProjectForm(data=data, instance=instance)

    @staticmethod
    def create_equipment_form(data: Optional[Dict] = None, instance: Optional[Any] = None) -> EquipmentFormInterface:
        """Create an equipment form instance."""
        return DjangoEquipmentForm(data=data, instance=instance)

    @staticmethod
    def create_service_form(data: Optional[Dict] = None, instance: Optional[Any] = None) -> ServiceFormInterface:
        """Create a service form instance."""
        return DjangoServiceForm(data=data, instance=instance)

    @staticmethod
    def create_participant_form(data: Optional[Dict] = None, instance: Optional[Any] = None) -> FormInterface:
        """Create a participant form instance."""
        return DjangoParticipantForm(data=data, instance=instance)

    @staticmethod
    def create_project_participant_form(data: Optional[Dict] = None, instance: Optional[Any] = None) -> ProjectParticipantFormInterface:
        """Create a project participant form instance."""
        return DjangoProjectParticipantForm(data=data, instance=instance)

    @staticmethod
    def create_outcome_form(data: Optional[Dict] = None, instance: Optional[Any] = None) -> FormInterface:
        """Create an outcome form instance."""
        return DjangoOutcomeForm(data=data, instance=instance)