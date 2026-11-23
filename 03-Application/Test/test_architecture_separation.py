# 03-Application/Test/test_architecture_separation.py
"""
TEST — loi de séparation brique/application (EXG-inc_1, Exigence Intégrité
d'Architecture) — recette/EXG : inc_1 « interdiction du monolithique ».
Ce test EST le grep d'imports du 5S, rendu exécutable et permanent :
  - core/ (hors exposition mcp_server, trace P11) n'importe JAMAIS
    fastapi, api/ ni phases/ ;
  - api/ n'importe jamais phases/ ni Test/ ;
  - phases/ n'importe jamais api/ ni Test/.
Aucune écriture, aucun réseau : lecture pure des sources.
"""
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]   # 03-Application/
CORE_DIR = APP_DIR / "core"
API_DIR = APP_DIR / "api"
PHASES_DIR = APP_DIR / "phases"

# Exposition HTTP : sa place dans core/ est un arbitrage P11 (2 apps FastAPI)
# déjà tracé au journal — exemptée ici, mais listée explicitement (pas un
# joker silencieux).
EXEMPTS_CORE = {"mcp_server.py": "exposition HTTP/MCP — arbitrage P11 tracé"}

INTERDITS = {
    "fastapi": ("import fastapi", "from fastapi"),
    "api": ("import api", "from api"),
    "phases": ("import phases", "from phases"),
    "Test": ("import Test", "from Test"),
}


def _sources(dossier: Path, exempts=None):
    """Générateur (nom_fichier, source) des .py d'un dossier de premier
    niveau — fichiers morts détectés au premier coup."""
    if not dossier.exists():
        return
    for py in sorted(dossier.glob("*.py")):
        if exempts and py.name in exempts:
            continue
        yield py.name, py.read_text(encoding="utf-8")


def _scan(dossier, interdits, exempts=None):
    """Retourne la liste des violations lisibles : (fichier, motif)."""
    for nom, src in _sources(dossier, exempts):
        for cible, motifs in interdits.items():
            for motif in motifs:
                if motif in src:
                    yield f"{dossier.name}/{nom} -> {motif} (interdit : {cible})"


# ---------------------------------------------------------inc_1 : core isolé
def test_exg_inc1_core_ne_depend_pas_de_lapplicatif():
    """core/ = brique : jamais fastapi, api/, phases/ (mcp_server exempté P11)."""
    violations = list(_scan(CORE_DIR, INTERDITS, EXEMPTS_CORE))
    assert not violations, ("Loi de séparation brique/application violée "
                            "(inc_1) : " + " ; ".join(violations))


def test_exg_inc1_api_ne_depend_pas_des_phases_ni_tests():
    """api/ est un adaptateur HTTP fin : jamais phases/, jamais Test/."""
    violations = list(_scan(API_DIR, {"phases": INTERDITS["phases"],
                                      "Test": INTERDITS["Test"]}))
    assert not violations, ("api/ importe interdit (inc_1) : "
                            + " ; ".join(violations))


def test_exg_inc1_phases_ne_dependent_pas_de_api_ni_tests():
    """phases/ = pipelines : jamais api/, jamais Test/."""
    violations = list(_scan(PHASES_DIR, {"api": INTERDITS["api"],
                                        "Test": INTERDITS["Test"]}))
    assert not violations, ("phases/ importe interdit (inc_1) : "
                            + " ; ".join(violations))


def test_exg_inc1_exempts_declares_et_minimaux():
    """L'exemption mcp_server est un arbitrage P11 EXPLICITE : le test
    échoue si elle disparaît du code (on ne garde pas un joker fantôme)."""
    src = (CORE_DIR / "mcp_server.py").read_text(encoding="utf-8") \
        if (CORE_DIR / "mcp_server.py").exists() else ""
    assert "from fastapi import" in src or "import fastapi" in src, (
        "mcp_server.py n'utilise plus fastapi : retirez l'exemption P11 "
        "du test (inc_1 n'a plus besoin de joker).")

# CI : enregistre le fichier dans la baseline NonReg (P9)
import pytest
pytestmark = pytest.mark.non_regression
