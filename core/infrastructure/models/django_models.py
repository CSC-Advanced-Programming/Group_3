"""
This module imports and re-exports the models from the core app's models.py.
This allows the infrastructure layer to use the models while maintaining separation of concerns.
"""
from core.models import (
    Program,
    Facility,
    Project,
    Equipment,
    Service,
    Participant,
    ProjectParticipant,
    Outcome,
    NATIONAL_ALIGNMENT_CHOICES,
    FOCUS_AREAS_CHOICES,
    PHASES_CHOICES,
    PARTNER_ORGANIZATION_CHOICES,
    FACILITY_TYPE_CHOICES,
    CAPABILITIES_CHOICES
)

__all__ = [
    'Program',
    'Facility',
    'Project',
    'Equipment',
    'Service',
    'Participant',
    'ProjectParticipant',
    'Outcome',
    'NATIONAL_ALIGNMENT_CHOICES',
    'FOCUS_AREAS_CHOICES', 
    'PHASES_CHOICES',
    'PARTNER_ORGANIZATION_CHOICES',
    'FACILITY_TYPE_CHOICES',
    'CAPABILITIES_CHOICES'
]