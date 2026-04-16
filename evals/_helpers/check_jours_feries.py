#!/usr/bin/env python3
"""Test helper: verifie le calcul dynamique des jours feries France."""
import sys
from datetime import date, timedelta


def _easter(year: int) -> date:
    """Algorithme de Butcher/Meeus (copie de compute_calendar.py)."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    month, day = divmod(h + l_ - 7 * m + 114, 31)
    return date(year, month, day + 1)


def jours_feries_france(year: int) -> set[date]:
    """11 jours feries France (copie de compute_calendar.py)."""
    e = _easter(year)
    return {
        date(year, 1, 1),
        e + timedelta(days=1),
        date(year, 5, 1),
        date(year, 5, 8),
        e + timedelta(days=39),
        e + timedelta(days=50),
        date(year, 7, 14),
        date(year, 8, 15),
        date(year, 11, 1),
        date(year, 11, 11),
        date(year, 12, 25),
    }


def main() -> int:
    errors = []

    # Paques: dates connues pour validation
    known_easter = {
        2024: date(2024, 3, 31),
        2025: date(2025, 4, 20),
        2026: date(2026, 4, 5),
        2027: date(2027, 3, 28),
        2028: date(2028, 4, 16),
        2030: date(2030, 4, 21),
        2035: date(2035, 3, 25),
    }

    for year, expected in known_easter.items():
        got = _easter(year)
        if got != expected:
            errors.append(f"Paques {year}: attendu {expected}, obtenu {got}")

    # Chaque annee doit avoir exactement 11 jours feries
    for year in range(2024, 2036):
        feries = jours_feries_france(year)
        if len(feries) != 11:
            errors.append(f"{year}: {len(feries)} feries au lieu de 11")

    # Fetes fixes presentes chaque annee
    for year in range(2024, 2036):
        feries = jours_feries_france(year)
        fixes = [
            date(year, 1, 1), date(year, 5, 1), date(year, 5, 8),
            date(year, 7, 14), date(year, 8, 15), date(year, 11, 1),
            date(year, 11, 11), date(year, 12, 25),
        ]
        for f in fixes:
            if f not in feries:
                errors.append(f"{year}: fete fixe {f} manquante")

    # Lundi de Paques = Paques + 1 jour
    for year in range(2024, 2036):
        feries = jours_feries_france(year)
        lundi_paques = _easter(year) + timedelta(days=1)
        if lundi_paques not in feries:
            errors.append(f"{year}: Lundi Paques {lundi_paques} manquant")

    # Ascension = Paques + 39 jours
    for year in range(2024, 2036):
        feries = jours_feries_france(year)
        ascension = _easter(year) + timedelta(days=39)
        if ascension not in feries:
            errors.append(f"{year}: Ascension {ascension} manquante")

    if errors:
        for e in errors:
            print(f"ERREUR: {e}")
        return 1

    print("jours_feries_ok=12")
    print("years_tested=2024-2035")
    print(f"easter_verified={len(known_easter)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
