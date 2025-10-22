from typing import Dict, Any
from django.utils.crypto import get_random_string
from core.models import Participant


def default_participant_data(**overrides) -> Dict[str, Any]:
    """Return a dict with default participant data, allow overrides."""
    base = {
        "full_name": "Test User",
        "email": f"{get_random_string(8)}@example.com",
        "affiliation": "CS",
        "specialization": None,
        "cross_skill_trained": False,
        "institution": "SCIT",
    }
    base.update(overrides)
    return base


def build_participant(**overrides) -> Participant:
    """Return an unsaved Participant instance (call .save() to persist)."""
    data = default_participant_data(**overrides)
    return Participant(**data)


def create_participant(**overrides) -> Participant:
    """Create and save a Participant in the test database and return it."""
    data = default_participant_data(**overrides)
    return Participant.objects.create(**data)
