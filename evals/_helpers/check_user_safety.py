#!/usr/bin/env python3
"""
check_user_safety.py, workflow anti-perte d'usager.

Mesure les signaux d'undertriggering / overtriggering par skill. Inspire des
sections "Iteration based on feedback" (page 17) et "Skill triggers too often"
(page 25) du guide Anthropic.

Pour chaque skill, on calcule :

  1. **Score triggering moyen** : moyenne du score de match entre les phrases
     test du skill et ses triggers (description + Triggers:). Un score moyen
     bas signale un undertriggering : la description manque de mots-cles
     proches du langage utilisateur.

  2. **Pass rate triggering par skill** : pour les phrases test ciblees sur
     ce skill, combien sont correctement routees vers lui (top-1 + marge de
     confiance). < 80 % = signal undertriggering.

  3. **Score moyen anti-triggers** : pour les phrases anti-triggers (qui ne
     doivent declencher AUCUN skill), combien le skill matche par erreur. Un
     score eleve signale un overtriggering : la description est trop large.

  4. **Couverture des paraphrases** : nb de phrases test par skill (le guide
     recommande >= 10 phrases variees par skill, page 15).

Resultat : un rapport avec les skills a risque d'undertriggering OU
d'overtriggering, et des suggestions concretes (mots-cles a ajouter,
anti-triggers a creer, etc).

Usage : python3 evals/_helpers/check_user_safety.py
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
EVALS = ROOT / "evals"

MIN_TESTS_PER_SKILL = 10
MIN_PASS_RATE = 0.80
OVERTRIGGER_SCORE_THRESHOLD = 2

# Memes stopwords + acronymes que run_evals.py
STOPWORDS = {
    "alors", "aussi", "avec", "avoir", "ceci", "cela", "cette", "comme",
    "dans", "donc", "elle", "encore", "etre", "être", "faire", "leur",
    "mais", "mieux", "même", "nous", "pour", "quel", "quelle", "quels",
    "quelles", "sans", "selon", "sont", "tout", "tous", "toute", "toutes",
    "très", "vous", "votre", "lance", "fait", "donne", "génère", "genere",
    "génerer", "produire", "with", "from", "this", "that", "have", "what", "your",
    "société", "societe", "entreprise", "entreprises", "pme/tpe", "skill",
    "française", "francaise", "françaises", "francaises", "cabinets", "cabinet",
    "skills", "bundle", "compte", "utiliser", "utilisez", "question", "questions",
    "détail", "detail", "produit", "produite",
    "niveau", "type", "types", "module", "modules", "gestion", "exercice",
}

BUSINESS_ACRONYMS = {
    "fec", "pcg", "cga", "nep", "dsn", "ias", "ifrs", "gaap",
    "is", "tva", "cir", "cii", "cvae", "cet", "cfe", "deb", "des",
    "bic", "bnc", "ba", "plf", "tvs", "ice",
    "dso", "dpo", "dio", "ccc", "bfr", "ebe", "ofr", "ffcf",
    "npv", "irr", "roi", "roe", "roce", "ebit", "ebitda", "wacc", "ltv", "cac",
    "arr", "mrr", "arpu", "nrr", "grr", "trs", "oee", "nps", "abc",
    "coso", "erm", "bcp", "rgpd", "lcbft", "nop", "acpr", "amf",
    "pge", "mlt", "ipo", "lbo", "vc", "pe", "sri", "bspce", "aga", "bsa",
    "tpe", "pme", "eti", "etb",
    "ghg", "gri", "tcfd", "sbti", "esg", "dma", "efrag", "csrd", "esrs",
    "ag", "kyc", "kpi", "kpis", "ca", "rnv", "rns", "pdg", "dg", "daf",
    "cfo", "cso", "dgfip", "urssaf", "drfip", "cac3", "ca3",
}


def tokenize(text: str) -> set[str]:
    text_lower = text.lower()
    long_words = set(re.findall(r"\b[a-zàâéèêëîïôùûüÿç0-9-]{4,}\b", text_lower))
    all_words_23 = set(re.findall(r"\b[a-zàâéèêëîïôùûüÿç0-9]{2,3}\b", text_lower))
    short_acronyms = all_words_23 & BUSINESS_ACRONYMS
    return (long_words | short_acronyms) - STOPWORDS


def extract_triggers(skill_md: Path) -> set[str]:
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return set()
    fm = yaml.safe_load(m.group(1)) or {}
    desc = fm.get("description", "")
    if isinstance(desc, list):
        desc = " ".join(str(x) for x in desc)
    return tokenize(desc)


def load_skills() -> dict[str, set[str]]:
    skills: dict[str, set[str]] = {}
    for d in sorted(ROOT.iterdir()):
        if d.is_dir() and d.name.startswith("cfo-"):
            md = d / "SKILL.md"
            if md.exists():
                skills[d.name] = extract_triggers(md)
    return skills


def load_triggering_tests() -> dict[str, Any]:
    p = EVALS / "triggering-tests.json"
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    skills = load_skills()
    triggering = load_triggering_tests()
    tests = triggering.get("tests", [])
    anti_triggers = triggering.get("anti_triggers", [])

    # 1. Compter les tests par skill
    tests_per_skill: dict[str, list[dict]] = defaultdict(list)
    for t in tests:
        tests_per_skill[t["expected_skill"]].append(t)

    # 2. Pour chaque skill, mesurer le pass rate
    print("=" * 70)
    print("WORKFLOW ANTI-PERTE D'USAGER")
    print("=" * 70)
    print()
    print("1/ Couverture phrases test (>= 10 par skill recommande page 15)")
    print()

    skills_undertested = []
    for skill in sorted(skills.keys()):
        n = len(tests_per_skill.get(skill, []))
        marker = "OK" if n >= MIN_TESTS_PER_SKILL else "WARN"
        print(f"  [{marker}] {skill:<32} {n} phrases")
        if n < MIN_TESTS_PER_SKILL:
            skills_undertested.append((skill, n))

    print()
    print("2/ Score triggering moyen par skill (signal undertriggering si bas)")
    print()

    skill_scores: dict[str, list[int]] = defaultdict(list)
    pass_per_skill: dict[str, tuple[int, int]] = {}
    for skill in sorted(skills.keys()):
        passed = 0
        total = 0
        for t in tests_per_skill.get(skill, []):
            phrase_tokens = tokenize(t["phrase"])
            scores = {n: len(phrase_tokens & toks) for n, toks in skills.items()}
            ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            top1, top1_score = ranked[0]
            top2_score = ranked[1][1] if len(ranked) > 1 else 0
            skill_scores[skill].append(scores.get(skill, 0))
            confident = (top2_score == 0) or (top1_score / max(top2_score, 1) >= 1.5)
            if top1 == skill and confident and top1_score > 0:
                passed += 1
            total += 1
        pass_per_skill[skill] = (passed, total)

    skills_under = []
    for skill in sorted(skills.keys()):
        scores = skill_scores.get(skill, [])
        avg = sum(scores) / len(scores) if scores else 0
        passed, total = pass_per_skill[skill]
        rate = (passed / total) if total else 0
        marker = "OK" if rate >= MIN_PASS_RATE and avg >= 2 else "WARN"
        print(f"  [{marker}] {skill:<32} avg_score={avg:.1f} pass={passed}/{total} ({rate*100:.0f}%)")
        if rate < MIN_PASS_RATE or avg < 2:
            skills_under.append((skill, avg, rate))

    print()
    print("3/ Score moyen sur anti-triggers (signal overtriggering si haut)")
    print()

    skills_over = []
    for skill in sorted(skills.keys()):
        triggers = skills[skill]
        max_score = 0
        avg_score = 0.0
        if anti_triggers:
            scores = []
            for at in anti_triggers:
                phrase = at if isinstance(at, str) else at.get("phrase", "")
                if not phrase:
                    continue
                t_tokens = tokenize(phrase)
                s = len(t_tokens & triggers)
                scores.append(s)
                max_score = max(max_score, s)
            avg_score = sum(scores) / len(scores) if scores else 0
        marker = "OK" if max_score < OVERTRIGGER_SCORE_THRESHOLD else "WARN"
        print(f"  [{marker}] {skill:<32} max={max_score} avg={avg_score:.1f}")
        if max_score >= OVERTRIGGER_SCORE_THRESHOLD:
            skills_over.append((skill, max_score))

    print()
    print("=" * 70)
    print("DIAGNOSTIC")
    print("=" * 70)
    print()
    if not skills_undertested and not skills_under and not skills_over:
        print("✓ Aucun signal d'undertriggering ni overtriggering detecte.")
        print(f"user_safety_ok={len(skills)}")
        return 0

    if skills_undertested:
        print("⚠ Skills sous-testes (< 10 phrases) - risque d'undertriggering en prod :")
        for skill, n in skills_undertested:
            print(f"    - {skill} : seulement {n} phrases test")
        print("  → Action : ajouter des phrases utilisateur paraphrasees dans triggering-tests.json")
        print()

    if skills_under:
        print("⚠ Skills avec faible pass rate ou score trigger - risque utilisateur perdu :")
        for skill, avg, rate in skills_under:
            print(f"    - {skill} : avg_score={avg:.1f} pass_rate={rate*100:.0f}%")
        print("  → Action : enrichir 'description' et 'Triggers:' avec mots-cles du langage utilisateur")
        print()

    if skills_over:
        print("⚠ Skills qui matchent des anti-triggers - risque sur-declenchement :")
        for skill, max_score in skills_over:
            print(f"    - {skill} : max score {max_score} sur anti-triggers")
        print("  → Action : description trop generique, retirer les mots-cles trop larges")
        print()

    print(f"user_safety_warnings={len(skills_undertested) + len(skills_under) + len(skills_over)}")
    return 0  # Warnings ne sont pas bloquants en CI


if __name__ == "__main__":
    sys.exit(main())
