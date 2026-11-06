import math

from hypothesis import given, strategies as st
from daycare_fees import parse_enrolment, hours_average, payable_fee


# ---------- parse_enrolment ----------
@given(st.text() | st.none())
def test_parse_enrolment_no_crash(s):
    try:
        parse_enrolment(s)
    except Exception as e:
        assert False, f"parse_enrolment crashed with: {e}"


@given(st.one_of(st.none(), st.integers(), st.floats(), st.binary(), st.lists(st.integers())))
def test_parse_enrolment_non_string_no_crash(s):
    try:
        parse_enrolment(s)
    except Exception as e:
        assert False, f"parse_enrolment crashed with: {e}"


@given(st.text() | st.none())
def test_parse_enrolment_output_shape(s):
    result = parse_enrolment(s)
    if result is not None:
        age_group, hours = result
        assert isinstance(age_group, str) and age_group != ""
        assert math.isfinite(hours) and 0 <= hours <= 168


@given(st.text(alphabet=st.characters(whitelist_categories=("Lu", "Ll")), min_size=1),
       st.integers(min_value=0, max_value=168))
def test_parse_enrolment_valid_roundtrip(age, hours):
    result = parse_enrolment(f"{age}:{hours}")
    assert result == (age.strip().title(), float(hours))


# ---------- hours_average ----------
@given(st.text() | st.none())
def test_hours_average_no_crash(s):
    try:
        hours_average(s)
    except Exception as e:
        assert False, f"hours_average crashed with: {e}"


@given(st.one_of(st.none(), st.integers(), st.floats(), st.binary(), st.lists(st.integers())))
def test_hours_average_non_string_no_crash(s):
    try:
        hours_average(s)
    except Exception as e:
        assert False, f"hours_average crashed with: {e}"


@given(st.lists(st.integers(min_value=0, max_value=168), min_size=1))
def test_hours_average_within_min_max(values):
    result = hours_average(",".join(map(str, values)))
    assert result is not None
    assert min(values) <= result <= max(values)


# ---------- payable_fee ----------
@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
    try:
        payable_fee(s)
    except Exception as e:
        assert False, f"payable_fee crashed with: {e}"


@given(st.one_of(st.none(), st.integers(), st.floats(), st.binary(), st.lists(st.integers())))
def test_payable_fee_non_string_no_crash(s):
    try:
        payable_fee(s)
    except Exception as e:
        assert False, f"payable_fee crashed with: {e}"


@given(st.text() | st.none())
def test_payable_fee_never_negative_or_nan(s):
    result = payable_fee(s)
    if result is not None:
        assert math.isfinite(result) and result >= 0


@given(st.floats(min_value=0, max_value=1e9), st.floats(min_value=0, max_value=1e9))
def test_payable_fee_valid_inputs(fee, discount):
    result = payable_fee(f"{fee!r}|{discount!r}")
    assert result is not None
    assert result >= 0
