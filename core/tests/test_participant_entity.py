# core/tests/test_participant_entity.py
import pytest
from core.domain.entities.participant import Participant

# ---------- Validation / construction ----------
def test_init_missing_full_name_raises():
    with pytest.raises(ValueError) as exc:
        Participant(full_name="", email="a@example.com", affiliation="Org")
    assert "Participant.FullName" in str(exc.value)

def test_init_missing_email_raises():
    with pytest.raises(ValueError):
        Participant(full_name="John Doe", email="   ", affiliation="Org")

def test_init_missing_affiliation_raises():
    with pytest.raises(ValueError):
        Participant(full_name="John Doe", email="a@example.com", affiliation="")

def test_init_invalid_email_format_raises():
    with pytest.raises(ValueError) as exc:
        Participant(full_name="John Doe", email="not-an-email", affiliation="Org")
    assert "Participant email format is invalid" in str(exc.value)

def test_init_cross_skill_true_requires_specialization_raises():
    with pytest.raises(ValueError) as exc:
        Participant(full_name="Jane Doe", email="jane@example.com", affiliation="Org", cross_skill_trained=True, specialization="")
    assert "Cross-skill flag requires Specialization" in str(exc.value)

# ---------- Email uniqueness and update ----------
def test_validate_email_uniqueness_raises_for_duplicate_case_insensitive():
    existing = ["foo@EXAMPLE.com", "other@example.com"]
    with pytest.raises(ValueError):
        Participant.validate_email_uniqueness("Foo@example.COM", existing)

def test_validate_email_uniqueness_passes_for_unique():
    existing = ["a@b.com"]
    # should not raise
    Participant.validate_email_uniqueness("new@domain.com", existing)

def test_update_email_invalid_raises():
    p = Participant(full_name="John Doe", email="john@example.com", affiliation="Org")
    with pytest.raises(ValueError):
        p.update_email("bad-email")

def test_update_email_valid_updates_value():
    p = Participant(full_name="John Doe", email="john@example.com", affiliation="Org")
    p.update_email("new.address+tag@example.co")
    assert p.email == "new.address+tag@example.co"

# ---------- Name extraction ----------
def test_first_and_last_name_normal():
    p = Participant(full_name="John Michael Doe", email="a@b.com", affiliation="Org")
    assert p.first_name == "John"
    assert p.last_name == "Doe"

def test_first_name_single_name_returns_name_last_empty():
    p = Participant(full_name="Cher", email="c@d.com", affiliation="Org")
    assert p.first_name == "Cher"
    assert p.last_name == ""

def test_first_last_empty_full_name_returns_empty():
    # defensive: set after init (init normally prevents empty)
    p = Participant(full_name="Valid Name", email="v@x.com", affiliation="Org")
    p.full_name = ""
    assert p.first_name == ""
    assert p.last_name == ""

# ---------- Case-insensitive helpers ----------
def test_is_affiliated_with_case_insensitive_true():
    p = Participant(full_name="A", email="a@b.com", affiliation="ACME")
    assert p.is_affiliated_with("acme")

def test_has_specialization_case_insensitive():
    p = Participant(full_name="A", email="a@b.com", affiliation="Org", specialization="SoFtWaRe")
    assert p.has_specialization("software")

def test_is_from_institution_case_insensitive():
    p = Participant(full_name="A", email="a@b.com", affiliation="Org", institution="MIT")
    assert p.is_from_institution("mit")

# ---------- Cross-skill flag and related helpers ----------
def test_mark_as_cross_skill_trained_without_specialization_raises():
    p = Participant(full_name="A", email="a@b.com", affiliation="Org", specialization="")
    with pytest.raises(ValueError):
        p.mark_as_cross_skill_trained()

def test_mark_as_cross_skill_trained_with_specialization_sets_flag():
    p = Participant(full_name="A", email="a@b.com", affiliation="Org", specialization="Network")
    p.mark_as_cross_skill_trained()
    assert p.cross_skill_trained is True

def test_can_be_cross_skill_trained_true_when_specialization_present():
    p = Participant(full_name="A", email="a@b.com", affiliation="Org", specialization="Net")
    assert p.can_be_cross_skill_trained()

def test_can_be_cross_skill_trained_false_when_no_specialization():
    p = Participant(full_name="A", email="a@b.com", affiliation="Org", specialization="")
    assert not p.can_be_cross_skill_trained()

def test_has_valid_cross_skill_status_true_if_not_cross_skill():
    p = Participant(full_name="A", email="a@b.com", affiliation="Org", specialization="")
    assert p.has_valid_cross_skill_status()

def test_has_valid_cross_skill_status_true_if_cross_skill_and_specialization():
    p = Participant(full_name="A", email="a@b.com", affiliation="Org", specialization="Software", cross_skill_trained=True)
    assert p.has_valid_cross_skill_status()

def test_has_valid_cross_skill_status_false_after_setting_cross_skill_without_specialization():
    p = Participant(full_name="A", email="a@b.com", affiliation="Org", specialization="")
    # mutate after init to simulate incorrect state
    p.cross_skill_trained = True
    assert not p.has_valid_cross_skill_status()

# ---------- Contribution and profile ----------
def test_can_contribute_direct_specialization_match():
    p = Participant(full_name="A", email="a@b.com", affiliation="Org", specialization="software")
    assert p.can_contribute_to_project("Software")

def test_can_contribute_if_cross_skill_trained():
    # Participant must have a specialization when cross_skill_trained=True
    p = Participant(full_name="A", email="a@b.com", affiliation="Org", specialization="General", cross_skill_trained=True)
    assert p.can_contribute_to_project("any-specialization")

def test_cannot_contribute_without_match_or_cross_skill():
    p = Participant(full_name="A", email="a@b.com", affiliation="Org", specialization="biology", cross_skill_trained=False)
    assert not p.can_contribute_to_project("software")

def test_get_participant_profile_cross_skilled():
    p = Participant(full_name="Jane Doe", email="jane@x.com", affiliation="Org", specialization="Software", institution="U", cross_skill_trained=True)
    profile = p.get_participant_profile()
    assert "Jane Doe" in profile
    assert "Cross-skilled" in profile
    assert "Software" in profile
    assert "U" in profile

def test_get_participant_profile_specialized():
    p = Participant(full_name="Jim", email="jim@x.com", affiliation="Org", specialization="Hardware", institution="Y", cross_skill_trained=False)
    profile = p.get_participant_profile()
    assert "Specialized" in profile

# ---------- Background detection ----------
def test_has_technical_background_by_specialization():
    p = Participant(full_name="A", email="a@b.com", affiliation="Org", specialization="Software Engineering")
    assert p.has_technical_background()

def test_has_technical_background_by_affiliation():
    p = Participant(full_name="A", email="a@b.com", affiliation="Engineering Dept", specialization="")
    assert p.has_technical_background()

def test_has_business_background_true_false():
    p1 = Participant(full_name="Biz", email="b@b.com", affiliation="Org", specialization="Business Analyst")
    assert p1.has_business_background()
    p2 = Participant(full_name="NotBiz", email="n@b.com", affiliation="Org", specialization="Software")
    assert not p2.has_business_background()

# ---------- Search ----------
def test_matches_search_criteria_full_name():
    p = Participant(full_name="Unique Name", email="u@x.com", affiliation="Org", specialization="X", institution="I")
    assert p.matches_search_criteria("unique")

def test_matches_search_criteria_email():
    p = Participant(full_name="N", email="searchme@example.com", affiliation="Org", specialization="X", institution="I")
    assert p.matches_search_criteria("searchme@EXAMPLE")

def test_matches_search_criteria_affiliation():
    p = Participant(full_name="N", email="n@x.com", affiliation="AlphaOrg", specialization="X", institution="I")
    assert p.matches_search_criteria("alpha")

def test_matches_search_criteria_specialization():
    p = Participant(full_name="N", email="n@x.com", affiliation="Org", specialization="Data Science", institution="I")
    assert p.matches_search_criteria("science")

def test_matches_search_criteria_institution():
    p = Participant(full_name="N", email="n@x.com", affiliation="Org", specialization="X", institution="UniX")
    assert p.matches_search_criteria("unix")

def test_matches_search_criteria_case_insensitive_no_match():
    p = Participant(full_name="N", email="n@x.com", affiliation="Org", specialization="X", institution="I")
    assert not p.matches_search_criteria("no-such-term")

# ---------- String representation ----------
def test_str_returns_full_name():
    p = Participant(full_name="Full Name", email="a@b.com", affiliation="Org")
    assert str(p) == "Full Name"

# ---------- Whitespace handling ----------
def test_whitespace_full_name_valid():
    p = Participant(full_name="  John Doe  ", email="j@x.com", affiliation="Org")
    assert p.first_name == "John"
    assert p.last_name == "Doe"

# ---------- Email regex edge example ----------
def test_email_regex_accepts_subdomain_and_long_tld():
    p = Participant(full_name="X", email="user@mail.example.co", affiliation="Org")
    assert p.email == "user@mail.example.co"