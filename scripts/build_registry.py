#!/usr/bin/env python3
"""
build_registry.py — Generation du registre canonique des exigences.

Pipeline Spec-Driven (arbitre architecture 2026-11-28) :
  specs (frontmatter exigences:)  +  arbitrages.json  ->  registry_exigences.json

- Les SPC-*.md sont la declaration humaine (source).
- arbitrages.json porte les decisions actees (divergences spec <-> registre) :
  abrogations, requalifications, renommages, conservations.
- Le registre genere est l'index machine qui fait foi, versionne a chaque pose.

Usage :
  python3 scripts/build_registry.py --version 2.9 [--dry-run] \
      [--specs-dir 01-Principes_Spécifications] \
      [--arbitrations arbitrages.json] \
      [--compare 01-Principes_Spécifications/registry_exigences.json] \
      [--output 01-Principes_Spécifications/registry_exigences.json]

En --dry-run : ecrit dans /tmp/registry_dryrun.json et affiche le rapport,
aucun fichier du repo n est modifie. En --compare : diff qualifie contre le
registre courant (EXG nouvelles / disparues / champ modifie).
"""

import argparse
import difflib
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("ERREUR : module pyyaml requis (conda install pyyaml).")

EXG_KEYS = ("id", "uid")
DEFAULT_SPEC_GLOB = "SPC-*.md"


def parse_spec(path: Path) -> dict:
    """Extrait le frontmatter YAML d une spec SPC-*.md."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    try:
        return yaml.safe_load(text[3:end]) or {}
    except yaml.YAMLError as e:
        print(f"  ⚠️ YAML INVALIDE dans {path.name} (spec ignoree — "
              f"quoter les valeurs contenant un deux-points) : {e}")
        return None


def collect_exigences(specs_dir: Path) -> list:
    """Recolte toutes les exigences declares en spec, avec leur spec source."""
    items, seen, invalides = [], {}, []
    for spec_path in sorted(specs_dir.rglob(DEFAULT_SPEC_GLOB)):
        fm = parse_spec(spec_path)
        if fm is None:
            invalides.append(spec_path.name)
            continue
        for ex in fm.get("exigences") or []:
            uid = None
            for k in EXG_KEYS:
                if ex.get(k):
                    uid = str(ex[k]).strip()   # casse declaree PRESERVEE (convention registre)
                    break
            if not uid:
                continue
            entry = dict(ex)
            entry["id"] = uid
            entry.pop("uid", None)
            if not entry.get("phase") and fm.get("phase_code"):
                entry["phase"] = fm["phase_code"]
            entry["spec_source"] = fm.get("reference") or f"{spec_path.parent.name}/{spec_path.name}"
            entry["_spec"] = f"{spec_path.parent.name}/{spec_path.name}"
            key = uid.upper()
            if key in seen:
                prev = seen[key]
                if _diff_fields(prev, entry):
                    print(f"  ⚠️ DOUBLON {uid} : {_spec2} vs {entry['_spec']}")
            seen[key] = entry
            items.append(entry)
    if invalides:
        print(f"  ⚠️ {len(invalides)} spec(s) au YAML invalide ignoree(s) : "
              f"{', '.join(invalides)}")
        print("     -> leurs exigences ne seront PAS au registre : corriger le frontmatter.")
    return items


def _diff_fields(a: dict, b: dict) -> bool:
    keys = ("critere", "recette", "titre", "phase", "domaine", "core", "test")
    return any(str(a.get(k)) != str(b.get(k)) for k in keys)


def apply_arbitrations(exigences: list, arbitrations: list,
                       current_entries: dict = None) -> list:
    """Applique les decisions : abrogee -> retiree ; champ -> override ;
    conservee -> reinsertion de l entree du registre courant (portage sans spec vivante)."""
    by_uid = {e["id"]: e for e in exigences}
    for arb in arbitrations:
        uid_key = str(arb.get("uid", "")).strip().upper()
        uid = next((e["id"] for e in exigences if e["id"].upper() == uid_key), uid_key)
        decision = arb.get("decision")
        if decision == "abrogee":
            exigences = [e for e in exigences if e["id"] != uid]
            print(f"  ⚖️  ABROGEE   : {uid} ({arb.get('date','?')} — {arb.get('motif','')})")
            continue
        if decision == "conservee":
            if current_entries and uid_key in current_entries and not any(
                    e["id"].upper() == uid_key for e in exigences):
                entry = dict(current_entries[uid_key])
                exigences.append(entry)
                print(f"  📌 CONSERVEE  : {uid} — entree REINSEREE depuis le registre courant "
                      f"({arb.get('date','?')} — {arb.get('motif','')})")
            else:
                print(f"  📌 CONSERVEE  : {uid} ({arb.get('date','?')} — {arb.get('motif','')})")
            continue
        champ = arb.get("champ")
        if champ and uid in by_uid:
            old = by_uid[uid].get(champ)
            by_uid[uid][champ] = arb.get("valeur_registre")
            print(f"  ✏️  OVERRIDE   : {uid}.{champ} : {old!r} -> {arb.get('valeur_registre')!r} "
                  f"({arb.get('date','?')} — {arb.get('motif','')})")
        elif champ:
            print(f"  ⚠️ OVERRIDE sur EXG absente des specs : {uid} — a arbitrer")
    return exigences


def compare_to_current(new: list, current_path: Path) -> None:
    """Diff qualifie : EXG nouvelles / disparues / champs modifies."""
    current = json.loads(current_path.read_text(encoding="utf-8"))
    cur_ids = {e["id"]: e for e in current.get("exigences", [])}
    new_ids = {e["id"] for e in new}
    added = sorted(new_ids - set(cur_ids))
    removed = sorted(set(cur_ids) - new_ids)
    print(f"\n== RAPPORT vs registre courant ({current_path.name}, "
          f"v{current.get('version', '?')}, {len(cur_ids)} EXG) ==")
    print(f"  NOUVELLES depuis specs ({len(added)}) : {', '.join(added) or 'aucune'}")
    print(f"  DISPARUES du registre ({len(removed)}) : {', '.join(removed) or 'aucune'}")
    changed = []
    for uid in sorted(new_ids & set(cur_ids)):
        for k in ("titre", "critere", "recette", "phase", "domaine", "core", "test"):
            if str(cur_ids[uid].get(k)) != str(next(e for e in new if e["id"] == uid).get(k)):
                changed.append(f"{uid}.{k}")
    print(f"  CHAMPS MODIFIES ({len(changed)}) : {', '.join(changed) or 'aucun'}")
    missing_arbitration = sorted(set(cur_ids) - new_ids)
    if missing_arbitration:
        print("  ⚠️ Les DISPARUES doivent etre soit declarees 'conservee', "
              "soit abrogees explicitement dans arbitrages.json "
              f"(conservation portage : {', '.join(missing_arbitration)})")


def main() -> None:
    ap = argparse.ArgumentParser(description="Generation du registre canonique des exigences")
    ap.add_argument("--version", required=True, help="version cible du registre, ex 2.9")
    ap.add_argument("--specs-dir", default="01-Principes_Spécifications")
    ap.add_argument("--arbitrations", default="01-Principes_Spécifications/arbitrages.json")
    ap.add_argument("--compare", default=None,
                    help="registre courant pour le rapport de diff (dry-run recommande)")
    ap.add_argument("--output", default=None,
                    help="fichier de sortie (defaut : dry-run, aucun fichier modifie)")
    args = ap.parse_args()

    specs_dir = Path(args.specs_dir)
    arb_path = Path(args.arbitrations)
    arbitrations = json.loads(arb_path.read_text(encoding="utf-8")) if arb_path.exists() else []
    if not arb_path.exists():
        print(f"⚠️ Aucun fichier arbitrages.json ({args.arbitrations}) : generation brute des specs.")

    print("== COLLECTE specs ==")
    exigences = collect_exigences(specs_dir)
    print(f"  {len(exigences)} EXG declarees en spec.")

    current_entries = {}
    compare_path = Path(args.compare) if args.compare else None
    if compare_path and compare_path.exists():
        current_entries = {e["id"].upper(): e for e in
                           json.loads(compare_path.read_text(encoding="utf-8")).get("exigences", [])}

    print("\n== APPLICATION DES ARBITRAGES ==")
    exigences = apply_arbitrations(exigences, arbitrations, current_entries)

    # tri stable pour des diffs lisibles
    exigences.sort(key=lambda e: e["id"].upper())
    for e in exigences:
        e.pop("_spec", None)

    registry = {
        "version": args.version,
        "generated": "build_registry.py",
        "arbitrations_applied": len(arbitrations),
        "exigences": exigences,
    }

    if args.compare and Path(args.compare).exists():
        compare_to_current(exigences, Path(args.compare))

    out = Path(args.output) if args.output else Path("/tmp/registry_dryrun.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n== SORTIE : {out} ({len(exigences)} EXG, version {args.version}) ==")
    if not args.output:
        print("Mode dry-run : aucun fichier du repo modifie.")


if __name__ == "__main__":
    main()
