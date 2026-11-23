# 03-Application/Test/test_local_volumes.py
"""
TEST — local_volumes (accès SSOT aux volumes locaux, lecture pure) —
recette/EXG :
  EXG-MET-P8-RES_1 + EXG-FWK-P1-GOU_12 (isolation : les seeds ABox et le scan
  réel .private/ ne sont JAMAIS modifiés par une lecture — dette D7),
  EXG-FWK-P8-AGE_1 (volume CTI local actif vs placeholder).
Sandbox : chemins SSOT détournés vers tmp ; confrontation (si buffer actif)
s'exécute en mémoire — ses échecs sont absorbés par le module (déjà le
comportement du code ; on ne teste pas confrontation ici, on teste
l'ISOLATION des fichiers).
"""
import hashlib

import pytest

import core.config as settings
import core.local_volumes as lv

SEED_FOYER = """@prefix dkg: <http://dkg.cybersec.org/tbox#> .
@prefix dkg-data: <http://dkg.cybersec.org/data#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
dkg-data:Box-Foyer dkg:hostname "Box Internet Familiale" .
"""
CTI_ACTIF = """@prefix dkg: <http://dkg.cybersec.org/tbox#> .
@prefix dkg-data: <http://dkg.cybersec.org/data#> .
dkg-data:Vuln-Test a dkg:Vulnerability .
"""


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture()
def sandbox(monkeypatch, tmp_path):
    paths = {
        "SEED_ABOX_FOYER_PATH": tmp_path / "seed_abox_foyer.ttl",
        "SEED_ABOX_HOTE_PATH": tmp_path / "seed_abox_hote.ttl",
        "SECURE_ABOX_HOST_SCAN_PATH": tmp_path / "abox_scan.ttl",
        "WORKSET_CTI_BUFFER_PATH": tmp_path / "cti_buffer.ttl",
        "EXTERNAL_SOURCES_COMPLIANCE_REGISTRY_PATH": tmp_path / "registry.json",
    }
    for name, path in paths.items():
        monkeypatch.setattr(settings, name, path)
    paths["SEED_ABOX_FOYER_PATH"].write_text(SEED_FOYER, encoding="utf-8")
    return paths


# -------------------------------------------GOU_12/RES_1 : isolation lecture
def test_exg_res1_seed_foyer_jamais_modifie_lecture_avec_cti(sandbox):
    """D7 : lecture mode=foyer avec CTI ACTIF (confrontation en mémoire) —
    le seed ABox reste à l'octet près identique."""
    buf = sandbox["WORKSET_CTI_BUFFER_PATH"]
    buf.write_text(CTI_ACTIF, encoding="utf-8")
    avant = _sha(sandbox["SEED_ABOX_FOYER_PATH"])
    lv._load_abox_by_mode("foyer")          # lecture (avec raisonnement mémoire)
    assert _sha(sandbox["SEED_ABOX_FOYER_PATH"]) == avant, \
        "le seed ABox a été modifié par une lecture (violation RES_1/GOU_12)"


def test_exg_res1_seed_foyer_jamais_modifie_lecture_inventaire_pur(sandbox):
    """D7 : lecture sans volume CTI actif (inventaire pur) → seed intact."""
    avant = _sha(sandbox["SEED_ABOX_FOYER_PATH"])
    ttl = lv._load_abox_by_mode("foyer")
    assert _sha(sandbox["SEED_ABOX_FOYER_PATH"]) == avant
    assert "Box Internet Familiale" in ttl


def test_exg_res1_scan_reel_lecture_pure(sandbox):
    """D7 : mode=scan → le fichier .private/ est restitué tel quel, jamais
    réécrit (fait d'observation durable)."""
    path = sandbox["SECURE_ABOX_HOST_SCAN_PATH"]
    path.write_text("# ABox scan réel (TLP:RED) — contenu de test\n", encoding="utf-8")
    avant = _sha(path)
    ttl = lv._load_abox_by_mode("scan")
    assert ttl.strip().startswith("# ABox scan réel")
    assert _sha(path) == avant, "l'ABox du scan réel a été modifiée par lecture"


def test_exg_res1_scan_absent_message_explicite(sandbox):
    """mode=scan sans scan enregistré : marqueur visible, pas de crash ni
    d'écriture compensatoire."""
    ttl = lv._load_abox_by_mode("scan")
    assert "Aucun scan du poste enregistré" in ttl
    assert not sandbox["SECURE_ABOX_HOST_SCAN_PATH"].exists()


# -------------------------------------------------AGE_1 : CTI local actif
def test_exg_age1_placeholder_pas_un_volume_actif(sandbox):
    """AGE_1 : le placeholder '# CTI buffer vide' (état initial/reset) n'est
    pas compté comme volume local actif → None."""
    buf = sandbox["WORKSET_CTI_BUFFER_PATH"]
    buf.write_text("# CTI buffer vide — sélectionnez des sources TLP:CLEAR.\n",
                   encoding="utf-8")
    assert lv._local_cti_active() is None


def test_exg_age1_volume_actif_detecte(sandbox):
    """AGE_1 : des données réellement chargées → volume actif détecté."""
    sandbox["WORKSET_CTI_BUFFER_PATH"].write_text(CTI_ACTIF, encoding="utf-8")
    actif = lv._local_cti_active()
    assert actif is not None and "Vuln-Test" in actif

# CI : enregistre le fichier dans la baseline NonReg (P9)
import pytest
pytestmark = pytest.mark.non_regression
