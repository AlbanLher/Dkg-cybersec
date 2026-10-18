#!/usr/bin/env python3
"""lint_ttl.py — conformité TTL du projet DKG-CyberSec (fail-fast).

Règles (cumulatives, activables par flags CLI) :
  --parse    (défaut)  : rdflib doit parser chaque .ttl (règle §49.3)
  --keyset             : préfixes/URI canoniques uniquement (tbox#, data#, cti#)
  --vocab              : prédicats proscrits absents (exploitsWeakness)

Usage : python lint_ttl.py [--keyset] [--vocab]
Sans flag : parse seul (rétrocompatible).
"""

import sys
from pathlib import Path

from rdflib import Graph, URIRef


ROOTS = [(Path(__file__).resolve().parents[2] / d)
         for d in ("02-Donnees", "03-Application")]
EXCLUDE_PARTS = {".private", "__pycache__", "video_p8", "Snapshots_Phases"}

CANONICAL_URIS = {
    "dkg": "http://dkg.cybersec.org/tbox#",
    "dkg-data": "http://dkg.cybersec.org/data#",
    "dkg-cti": "http://dkg.cybersec.org/cti#",
}
FORBIDDEN_PREFIX_URIS = {  # URI proscrites → vraie cible
    "http://dkg.cybersec.org/abox#": "http://dkg.cybersec.org/data#",
}
FORBIDDEN_PREDICATES = {"http://dkg.cybersec.org/tbox#exploitsWeakness"}


def iter_ttl_files():
    for root in ROOTS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.ttl")):
            if not (EXCLUDE_PARTS & set(path.parts)):
                yield path


def check_keyset(text: str, path: Path) -> list:
    errors = []
    for local, uri in CANONICAL_URIS.items():
        expected = f"@prefix {local}: <{uri}> ."
        if uri in text and expected not in text:
            errors.append(
                f"keyset: l'URI canonique {uri} est utilisée mais déclarée "
                f"sous un autre alias que {local}: — normaliser la déclaration"
            )
    for bad, target in FORBIDDEN_PREFIX_URIS.items():
        if bad in text:
            errors.append(f"keyset: URI proscrite {bad} → remplacer par {target}")
    for legacy in ("dkg_data:", "dkg_tbox:"):
        if legacy in text:
            errors.append(
                f"keyset: alias hérité « {legacy} » → utiliser les formes "
                f"canoniques dkg-data: / dkg:"
            )
    return errors


def check_vocab(graph: Graph, path: Path) -> list:
    errors = []
    for pred in FORBIDDEN_PREDICATES:
        if (None, URIRef(pred), None) in graph:
            errors.append(
                f"vocab: prédicat proscrit {pred} présent "
                f"(TBox de référence : hasWeakness)"
            )
    return errors


def main() -> int:
    do_keyset = "--keyset" in sys.argv
    do_vocab = "--vocab" in sys.argv
    failures = 0
    checked = 0
    for path in iter_ttl_files():
        checked += 1
        try:
            graph = Graph()
            graph.parse(path, format="turtle")
        except Exception as exc:
            print(f"FAIL {path} — parse : {exc}")
            failures += 1
            continue
        issues = []
        if do_keyset:
            issues += check_keyset(path.read_text(encoding="utf-8"), path)
        if do_vocab:
            issues += check_vocab(graph, path)
        for msg in issues:
            print(f"FAIL {path} — {msg}")
        failures += len(issues)
    print(
        f"lint-ttl {'FAIL' if failures else 'OK'} : "
        f"{checked} fichier(s) TTL, {failures} problème(s)."
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
