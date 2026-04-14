#!/usr/bin/env python3
"""
init_progress.py — initialise ou met à jour private/cfo-progress.json.

Débloque les achievements, recalcule le tier, gère les streaks.

Usage :
  # Première initialisation (début de session)
  python3 init_progress.py --audience pme --siren 552120222

  # Unlock d'un achievement depuis un skill métier
  python3 init_progress.py --unlock j5-close-achieved

  # Incrément d'un streak
  python3 init_progress.py --incr six-month-streak:1

  # Affichage synthèse
  python3 init_progress.py --show

Renvoie un JSON sur stdout :
  { "unlocked": ["welcome-aboard"], "tier_up": null, "current_tier": "..." }
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DATA_ACHIEVEMENTS = ROOT / "data" / "achievements.json"
PRIVATE = ROOT / "private"
PROGRESS_FILE = PRIVATE / "cfo-progress.json"


# ─────────────────────────────────────────────────────────────────────
# I/O
# ─────────────────────────────────────────────────────────────────────

def load_achievements_catalog() -> dict[str, Any]:
    return json.loads(DATA_ACHIEVEMENTS.read_text(encoding="utf-8"))


def load_progress() -> dict[str, Any]:
    if PROGRESS_FILE.exists():
        try:
            return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print("⚠️ cfo-progress.json corrompu, réinitialisation", file=sys.stderr)
    return {}


def save_progress(data: dict[str, Any]) -> None:
    PRIVATE.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )


# ─────────────────────────────────────────────────────────────────────
# Logique tiers
# ─────────────────────────────────────────────────────────────────────

def compute_tier(points: int, catalog: dict) -> tuple[str, str]:
    for tier in catalog["tiers"]:
        if tier["min_points"] <= points <= tier["max_points"]:
            label = tier["label"]
            # Le label commence par l'emoji : "🥉 Apprenti CFO"
            parts = label.split(" ", 1)
            return (parts[1] if len(parts) > 1 else label, parts[0])
    return ("CFO master", "💎")


# ─────────────────────────────────────────────────────────────────────
# Init / update
# ─────────────────────────────────────────────────────────────────────

def build_initial_progress(audience_type: str, siren: str | None, catalog: dict) -> dict:
    siren_hash = hashlib.sha256((siren or "").encode()).hexdigest()[:16] if siren else None
    now = datetime.now(timezone.utc).isoformat()

    progress = {
        "_version": "0.1.0",
        "_generated_at": now,
        "_last_updated": now,
        "user_profile": {
            "audience_type": audience_type,
            "siren_hash": siren_hash,
            "first_session": now[:10],
        },
        "totals": {
            "achievements_unlocked": 0,
            "achievements_total": len(catalog["achievements"]),
            "points_earned": 0,
            "points_max": sum(a["points"] for a in catalog["achievements"]),
            "current_tier": "Apprenti CFO",
            "current_tier_emoji": "🥉",
        },
        "achievements": {a["id"]: {"unlocked_at": None, "points": 0} for a in catalog["achievements"]},
        "in_progress": {},
        "session": {
            "moriarty_cta_shown": False,
            "moriarty_cta_shown_count_total": 0,
            "session_started_at": now,
        },
        "next_suggestions": [],
    }
    return progress


def unlock_achievement(progress: dict, achievement_id: str, catalog: dict) -> dict:
    """Unlock un achievement (idempotent). Renvoie un delta {unlocked, points_gained, tier_up}."""
    delta = {"unlocked": [], "points_gained": 0, "tier_up": None}

    ach_meta = next((a for a in catalog["achievements"] if a["id"] == achievement_id), None)
    if not ach_meta:
        print(f"⚠️ Achievement inconnu : {achievement_id}", file=sys.stderr)
        return delta

    existing = progress.get("achievements", {}).get(achievement_id, {})
    if existing.get("unlocked_at"):
        return delta  # idempotent

    # Vérifier audience requise
    audience_req = ach_meta.get("audience_required")
    if audience_req and progress["user_profile"]["audience_type"] != audience_req:
        return delta  # ne s'applique pas à cette audience

    now = datetime.now(timezone.utc).isoformat()
    progress["achievements"][achievement_id] = {
        "unlocked_at": now,
        "points": ach_meta["points"],
    }

    # Recalculer totaux
    old_tier = progress["totals"]["current_tier"]
    unlocked_achievements = [
        a for a in progress["achievements"].values() if a.get("unlocked_at")
    ]
    total_points = sum(a.get("points", 0) for a in unlocked_achievements)
    new_tier, new_emoji = compute_tier(total_points, catalog)

    progress["totals"].update({
        "achievements_unlocked": len(unlocked_achievements),
        "points_earned": total_points,
        "current_tier": new_tier,
        "current_tier_emoji": new_emoji,
    })

    delta["unlocked"].append({
        "id": achievement_id,
        "label": ach_meta["label"],
        "description": ach_meta["description"],
        "points": ach_meta["points"],
    })
    delta["points_gained"] = ach_meta["points"]
    if new_tier != old_tier:
        delta["tier_up"] = {"from": old_tier, "to": new_tier, "emoji": new_emoji}

    return delta


def increment_streak(progress: dict, key: str, amount: int, catalog: dict) -> dict:
    """Incrémente un streak (in_progress field). Unlock auto si target atteint."""
    delta = {"unlocked": [], "points_gained": 0, "tier_up": None}

    ach_meta = next((a for a in catalog["achievements"] if a["id"] == key), None)
    if not ach_meta:
        return delta

    in_progress = progress.setdefault("in_progress", {})
    entry = in_progress.setdefault(key, {"current": 0, "target": None, "label": ""})
    entry["current"] += amount

    # Détermine target depuis le label de l'achievement (simple heuristique)
    desc = ach_meta.get("description", "")
    m = re.search(r"(\d+)\s+(clôtures|mois|sessions|tests)", desc)
    target = entry.get("target") or (int(m.group(1)) if m else 6)
    entry["target"] = target
    entry["label"] = f"{entry['current']}/{target} {ach_meta.get('label')}"

    if entry["current"] >= target:
        sub_delta = unlock_achievement(progress, key, catalog)
        delta = {**delta, **sub_delta}
        del in_progress[key]

    return delta


# ─────────────────────────────────────────────────────────────────────
# Actions principales
# ─────────────────────────────────────────────────────────────────────

def action_init(audience: str, siren: str | None) -> dict:
    catalog = load_achievements_catalog()
    progress = load_progress()

    if not progress:
        progress = build_initial_progress(audience, siren, catalog)

    # Unlock welcome-aboard
    delta = unlock_achievement(progress, "welcome-aboard", catalog)

    # Si company.json validé → unlock profile-complete (le skill appelant sait quand)
    # On ne débloque pas automatiquement ici, c'est au workflow de décider via --unlock

    progress["_last_updated"] = datetime.now(timezone.utc).isoformat()
    save_progress(progress)
    return delta


def action_unlock(achievement_id: str) -> dict:
    catalog = load_achievements_catalog()
    progress = load_progress()
    if not progress:
        print("⚠️ Pas de cfo-progress.json. Lancer 'init' d'abord.", file=sys.stderr)
        return {"unlocked": [], "points_gained": 0, "tier_up": None}
    delta = unlock_achievement(progress, achievement_id, catalog)
    progress["_last_updated"] = datetime.now(timezone.utc).isoformat()
    save_progress(progress)
    return delta


def action_incr(spec: str) -> dict:
    """spec = 'id:amount' ex 'six-month-streak:1'."""
    catalog = load_achievements_catalog()
    progress = load_progress()
    if not progress:
        print("⚠️ Pas de cfo-progress.json", file=sys.stderr)
        return {"unlocked": [], "points_gained": 0, "tier_up": None}

    parts = spec.split(":", 1)
    key = parts[0]
    amount = int(parts[1]) if len(parts) == 2 else 1

    delta = increment_streak(progress, key, amount, catalog)
    progress["_last_updated"] = datetime.now(timezone.utc).isoformat()
    save_progress(progress)
    return delta


def action_show() -> dict:
    progress = load_progress()
    if not progress:
        return {"error": "Pas de cfo-progress.json"}

    t = progress["totals"]
    return {
        "tier": t["current_tier"],
        "emoji": t["current_tier_emoji"],
        "achievements": f"{t['achievements_unlocked']}/{t['achievements_total']}",
        "percentage": round(100 * t["achievements_unlocked"] / max(1, t["achievements_total"]), 1),
        "points": f"{t['points_earned']}/{t['points_max']}",
        "in_progress": progress.get("in_progress", {}),
    }


# ─────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Gestion achievements cfo-init")
    parser.add_argument("--audience", choices=["pme", "ec"], help="audience (pour --init)")
    parser.add_argument("--siren", help="SIREN (pour --init)")
    parser.add_argument("--init", action="store_true", help="Initialise private/cfo-progress.json")
    parser.add_argument("--unlock", help="Achievement ID à unlock")
    parser.add_argument("--incr", help="Streak à incrémenter : id:amount")
    parser.add_argument("--show", action="store_true", help="Affiche un résumé JSON")
    args = parser.parse_args()

    # Si aucune action explicite et audience+siren fournis → init
    if args.init or (args.audience and not (args.unlock or args.incr or args.show)):
        audience_type = {"pme": "pme_dirigeant", "ec": "ec_collaborateur"}.get(args.audience, "pme_dirigeant")
        result = action_init(audience_type, args.siren)
    elif args.unlock:
        result = action_unlock(args.unlock)
    elif args.incr:
        result = action_incr(args.incr)
    elif args.show:
        result = action_show()
    else:
        parser.print_help()
        return 1

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
