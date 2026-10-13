#!/usr/bin/env python3
"""lint_ttl.py — fail-fast : parse rdflib de tous les .ttl du workspace.
Échoue avec la liste des fichiers non conformes (préfixe manquant, syntaxe).
Règle projet : tout préfixe utilisé doit être déclaré (T-R_1 / GOU_14)."""
import sys
from pathlib import Path
from rdflib import Graph

ROOT = Path(__file__).resolve().parents[2]   # racine Workspace
failures = []
checked = 0
for ttl in ROOT.rglob("*.ttl"):
    if any(part.startswith(".") for part in ttl.parts):   # .private/ etc.
        continue
    checked += 1
    g = Graph()
    try:
        g.parse(str(ttl), format="turtle")
    except Exception as exc:
        failures.append(f"FAIL {ttl.relative_to(ROOT)} : {str(exc)[:120]}")

if failures:
    print("\n".join(failures))
    print(f"\n{len(failures)}/{checked} fichier(s) TTL non conforme(s).")
    sys.exit(1)
print(f"lint-ttl OK : {checked} fichier(s) TTL conformes.")
