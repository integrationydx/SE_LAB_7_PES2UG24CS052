import math

MAX_WEEKLY_HOURS = 168  # hours in a week


def _to_finite_float(token):
    """Convert a string to a finite float, or return None if impossible."""
    try:
        value = float(token.strip())
    except (ValueError, OverflowError):
        return None
    if not math.isfinite(value):  # rejects nan, inf, -inf
        return None
    return value


def parse_enrolment(text):
    """Parse 'age_group:hours' -> (Age Group, hours). Returns None on invalid input."""
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    age_group = parts[0].strip()
    if not age_group:
        return None
    hours = _to_finite_float(parts[1])
    if hours is None or hours < 0 or hours > MAX_WEEKLY_HOURS:
        return None
    return age_group.title(), hours


def hours_average(hours_csv):
    """Average of comma-separated whole-number weekly hours. Returns None on invalid input."""
    if not isinstance(hours_csv, str):
        return None
    values = []
    for token in hours_csv.split(','):
        try:
            value = int(token.strip())
        except ValueError:
            return None
        if value < 0 or value > MAX_WEEKLY_HOURS:
            return None
        values.append(value)
    if not values:
        return None
    return round(sum(values) / len(values), 2)


def payable_fee(text):
    """Parse 'fee|discount' -> fee incl. 18% tax minus discount, never below 0.
    Returns None on invalid input."""
    if not isinstance(text, str):
        return None
    parts = text.split('|')
    if len(parts) != 2:
        return None
    fee = _to_finite_float(parts[0])
    discount = _to_finite_float(parts[1])
    if fee is None or discount is None or fee < 0 or discount < 0:
        return None
    total = fee * 1.18 - discount
    if not math.isfinite(total):
        return None
    return round(max(total, 0), 2)


def main():
    print("==== Running parse_enrolment ====")
    user_input = input("Enter age group:hours (e.g. toddler:25): ")
    result = parse_enrolment(user_input)
    print("Age Group and Hours:", result if result is not None else "Invalid input")

    print("\n==== Running hours_average ====")
    user_input = input("Enter weekly hours as CSV (e.g. 20,25,30): ")
    result = hours_average(user_input)
    print("Average Hours:", result if result is not None else "Invalid input")

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 3000|250): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
