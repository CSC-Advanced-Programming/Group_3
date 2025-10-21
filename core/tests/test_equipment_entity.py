import pytest
from core.domain.entities.equipment import Equipment


def test_init_missing_facility_id_raises():
    with pytest.raises(ValueError) as exc:
        Equipment(facility_id=None, name="Drill", inventory_code="INV-001")
    assert "Equipment.FacilityId" in str(exc.value)


def test_init_missing_name_raises():
    with pytest.raises(ValueError):
        Equipment(facility_id=1, name="   ", inventory_code="INV-002")


def test_init_missing_inventory_code_raises():
    with pytest.raises(ValueError):
        Equipment(facility_id=1, name="Lathe", inventory_code="  ")


def test_electronics_requires_prototyping_or_testing_raises():
    with pytest.raises(ValueError):
        Equipment(facility_id=1, name="Oscilloscope", inventory_code="OSC-1", usage_domain="Electronics", support_phase="Commercialization")


def test_electronics_with_valid_support_passes():
    e = Equipment(facility_id=1, name="Scope", inventory_code="OSC-2", usage_domain="Electronics", support_phase="Prototyping")
    assert e.supports_electronics_properly()


def test_validate_uniqueness_duplicate_raises():
    with pytest.raises(ValueError):
        Equipment.validate_uniqueness("INV-001", ["INV-001", "INV-002"])


def test_validate_uniqueness_non_duplicate_passes():
    # should not raise
    Equipment.validate_uniqueness("INV-123", ["INV-001"])


def test_validate_delete_guard_raises_when_referenced():
    with pytest.raises(ValueError):
        Equipment.validate_delete_guard(True)


def test_capabilities_list_parsing_empty_returns_empty():
    e = Equipment(facility_id=1, name="Tool", inventory_code="T-1")
    assert e.capabilities_list == []


def test_capabilities_list_parsing_multiple():
    e = Equipment(facility_id=1, name="Tool", inventory_code="T-2", capabilities="CNC, PCB fabrication,  materials testing")
    assert e.capabilities_list == ["CNC", "PCB fabrication", "materials testing"]


def test_usage_domain_list_parsing():
    e = Equipment(facility_id=1, name="Tool", inventory_code="T-3", usage_domain="Electronics, Mechanical", support_phase="Prototyping")
    assert e.usage_domain_list == ["Electronics", "Mechanical"]


def test_has_capability_true_false():
    e = Equipment(facility_id=1, name="Tool", inventory_code="T-4", capabilities="CNC,Testing")
    assert e.has_capability("CNC")
    assert not e.has_capability("Welding")


def test_can_be_used_in_domain_true_false():
    e = Equipment(facility_id=1, name="Tool", inventory_code="T-5", usage_domain="IoT,Electronics", support_phase="Testing")
    assert e.can_be_used_in_domain("Electronics")
    assert not e.can_be_used_in_domain("Mechanical")


def test_supports_phase_case_insensitive():
    e = Equipment(facility_id=1, name="Tool", inventory_code="T-6", support_phase="Testing")
    assert e.supports_phase("testing")


def test_is_in_facility_true_false():
    e = Equipment(facility_id=42, name="Tool", inventory_code="T-7")
    assert e.is_in_facility(42)
    assert not e.is_in_facility(7)


def test_add_capability_adds_and_no_duplicate():
    e = Equipment(facility_id=1, name="Tool", inventory_code="T-8", capabilities="CNC")
    e.add_capability("PCB fabrication")
    assert "PCB fabrication" in e.capabilities_list
    # adding existing should not duplicate
    e.add_capability("CNC")
    assert e.capabilities_list.count("CNC") == 1


def test_add_capability_empty_raises():
    e = Equipment(facility_id=1, name="Tool", inventory_code="T-9", capabilities="")
    with pytest.raises(ValueError):
        e.add_capability("")


def test_remove_capability_removes():
    e = Equipment(facility_id=1, name="Tool", inventory_code="T-10", capabilities="A,B,C")
    e.remove_capability("B")
    assert "B" not in e.capabilities_list


def test_add_usage_domain_adds():
    e = Equipment(facility_id=1, name="Tool", inventory_code="T-11", usage_domain="Mechanical")
    e.add_usage_domain("Electronics")
    assert "Electronics" in e.usage_domain_list


def test_add_usage_domain_empty_raises():
    e = Equipment(facility_id=1, name="Tool", inventory_code="T-12")
    with pytest.raises(ValueError):
        e.add_usage_domain("")


def test_remove_usage_domain():
    e = Equipment(facility_id=1, name="Tool", inventory_code="T-13", usage_domain="IoT,Electronics", support_phase="Prototyping")
    e.remove_usage_domain("IoT")
    assert "IoT" not in e.usage_domain_list


def test_supports_electronics_properly_true_when_non_electronics():
    e = Equipment(facility_id=1, name="Tool", inventory_code="T-14", usage_domain="Mechanical", support_phase="Commercialization")
    assert e.supports_electronics_properly()


def test_can_be_used_for_electronics_true_when_electronics_and_support_ok():
    e = Equipment(facility_id=1, name="Tool", inventory_code="T-15", usage_domain="Electronics,IoT", support_phase="Testing")
    assert e.can_be_used_for_electronics()


def test_str_returns_name_and_inventory_code():
    e = Equipment(facility_id=1, name="Mill", inventory_code="M-01")
    assert str(e) == "Mill (M-01)"
