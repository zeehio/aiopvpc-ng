"""ESIOS API handler for HomeAssistant. PVPC tariff periods."""

from __future__ import annotations

from datetime import datetime, timedelta

_HOURS_P2 = (8, 9, 14, 15, 16, 17, 22, 23)
_HOURS_P2_CYM = (8, 9, 10, 15, 16, 17, 18, 23)
# TODO review 'festivos nacionales no sustituibles de fecha fija', + 6/1
# obtained from `holidays` library,
# - with weekend days disabled (already full P3)
# - no 'translated' holidays
# - no 'Jueves Santo' as special day


def _tariff_period_key(local_ts: datetime, zone_ceuta_melilla: bool) -> str:
    """Return period key (P1/P2/P3) for current hour."""
    day = local_ts.date()

    fixed_holidays = [
        (1, 1),  # 1 de enero
        (1, 6),  # 6 de enero
        (5, 1),  # 1 de mayo
        (8, 15),  # 15 de agosto
        (10, 12),  # 12 de octubre
        (11, 1),  # 1 de noviembre
        (12, 6),  # 6 de diciembre
        (12, 8),  # 8 de diciembre
        (12, 25),  # 25 de diciembre
    ]

    is_national_holiday = (day.month, day.day) in fixed_holidays

    if is_national_holiday or day.isoweekday() >= 6 or local_ts.hour < 8:
        return "P3"
    if zone_ceuta_melilla and local_ts.hour in _HOURS_P2_CYM:
        return "P2"
    if not zone_ceuta_melilla and local_ts.hour in _HOURS_P2:
        return "P2"
    return "P1"


def get_current_and_next_tariff_periods(
    local_ts: datetime, zone_ceuta_melilla: bool
) -> tuple[str, str, timedelta]:
    """Get tariff periods for PVPC 2.0TD."""
    current_period = _tariff_period_key(local_ts, zone_ceuta_melilla)
    delta = timedelta(hours=1)
    while (
        next_period := _tariff_period_key(local_ts + delta, zone_ceuta_melilla)
    ) == current_period:
        delta += timedelta(hours=1)
    return current_period, next_period, delta
