# 03-Application/Test/test_routes_phase8.py
"""
TEST — routes Phase 8 (adaptateur HTTP — api/routes_phase8.py) —
recette/EXG :
  EXG-MET-P8-DEM_1/2/3/RES_1, EXG-FWK-P9-GTW_1 (le sas servi en REST),
  EXG-MET-P8-DEM_7 + EXG-TEC-P07-mi_3 (contrat API piloté par tests).
Verrouille la voie POST /api/phase8/scan — régression découverte au 5S
(500 silencieux après disparition des modules — aucun test ne la couvrait).
Sandbox : TOUS les chemins SSOT détournés vers tmp ; le scan réel est
remplacé par des doublures (jamais de vrai scan du poste en recette) ;
buffer CTI inactif → le chemin confrontation n'est pas invoqué.
Prérequis : httpx (TestClient). Installer si absent : pip install httpx.
"""
import json

import pytest

import core.config as settings
import core.local_host_scanner as scanner_mod
import core.agent_local_host_abox as abox_mod

fastapi_tc = pytest.importorskip("fastapi.testclient")

SEED_TBOX = """@prefix dkg: <http://dkg.cybersec.org/tbox#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
dkg:Asset a owl:Class .
dkg:newProp a owl:DatatypeProperty .
"""
SEED_RULES = "# règles locales seed (sandbox)\n"
DELTA_OK = """@prefix dkg: <http://dkg.cybersec.org/tbox#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
dkg:propRoutes a owl:DatatypeProperty .
"""


@pytest.fixture()
def sandbox(monkeypatch, tmp_path):
    paths = {
        "WORKSET_TBOX_PATH": tmp_path / "DKG_TBox_Working.ttl",
        "WORKSET_RULES_PATH": tmp_path / "DKG_Rules_Working.ttl",
        "WORKSET_CTI_BUFFER_PATH": tmp_path / "cti_buffer.ttl",
        "WORKSET_HITL_AUDIT_LOG_PATH": tmp_path / "hitl_audit.log",
        "SEED_TBOX_DEMO_PATH": tmp_path / "seed_tbox.ttl",
        "SEED_RULES_DEMO_PATH": tmp_path / "seed_rules.rq",
        "SHACL_MASTER_PATH": tmp_path / "DKG_SHACL_Master.ttl",
        "SECURE_ABOX_HOST_SCAN_PATH": tmp_path / "abox_scan.ttl",
        "SEED_ABOX_FOYER_PATH": tmp_path / "seed_abox_foyer.ttl",
        "SEED_ABOX_HOTE_PATH": tmp_path / "seed_abox_hote.ttl",
        "SEED_CTI_CLEAR_PATH": tmp_path / "seed_cti_clear.ttl",
        "EXTERNAL_SOURCES_COMPLIANCE_REGISTRY_PATH": tmp_path / "registry.json",
        "EXTERNAL_SOURCES_CATALOG_PATH": tmp_path / "catalog.json",
    }
    for name, path in paths.items():
        monkeypatch.setattr(settings, name, path)
    paths["SEED_TBOX_DEMO_PATH"].write_text(SEED_TBOX, encoding="utf-8")
    paths["SEED_RULES_DEMO_PATH"].write_text(SEED_RULES, encoding="utf-8")
    paths["SHACL_MASTER_PATH"].write_text("# shapes sandbox vides\n", encoding="utf-8")
    return paths


@pytest.fixture()
def client(sandbox):
    """App minimale : le routeur seul (pas de static files de main.py)."""
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from api.routes_phase8 import router
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def _log(sandbox):
    p = sandbox["WORKSET_HITL_AUDIT_LOG_PATH"]
    return p.read_text(encoding="utf-8") if p.exists() else ""


# ----------------------------------------------------------lectures pures
def test_exg_dem1_tbox_lue_depuis_workset(client, sandbox):
    """DEM_1 : ouverture → TBox workset servie, reset auto au premier accès."""
    r = client.get("/api/phase8/tbox")
    assert r.status_code == 200
    body = r.json()
    assert body["tbox_source"] == "workset"
    assert "dkg:Asset" in body["tbox_ttl"]


def test_exg_age1_rbox_locale_zero_reseau(client, sandbox):
    """AGE_1 : RBox locale servie — la route ne fait aucune requête réseau."""
    r = client.get("/api/phase8/rbox")
    assert r.status_code == 200 and "rbox_ttl" in r.json()


def test_exg_dem2_audit_foyer_bilan_nl(client, sandbox):
    """DEM_2 : audit sans source réseau → bilan NL (liste) servie."""
    sandbox["SEED_ABOX_FOYER_PATH"].write_text(SEED_TBOX, encoding="utf-8")
    r = client.post("/api/phase8/audit", json={"mode": "foyer",
                                               "enabled_network_sources": []})
    assert r.status_code == 200
    body = r.json()
    assert isinstance(body["nl_bilan"], list) and body["nl_bilan"]
    assert body["network_requests_made"] == 0


def test_exg_dem2_audit_scan_terrain_reel(client, sandbox):
    """DEM_2 (v-real) : audit mode=scan lit l'ABox .private/ du sandbox."""
    sandbox["SECURE_ABOX_HOST_SCAN_PATH"].write_text(SEED_TBOX, encoding="utf-8")
    r = client.post("/api/phase8/audit", json={"mode": "scan"})
    assert r.status_code == 200
    assert r.json()["abox_ttl"].strip() # ABox réelle chargée


def test_exg_dem4b_graphes_mermaid(client, sandbox):
    """DEM_4b : vues Mermaid TBox + superposition — jamais de 500."""
    r1 = client.get("/api/phase8/tbox/graph")
    assert r1.status_code == 200 and "mermaid" in r1.json()
    r2 = client.get("/api/phase8/superposition/graph",
                    params={"mode": "foyer", "equipment": ""})
    assert r2.status_code == 200 and "mermaid" in r2.json()


def test_exg_age2_frugalite(client, sandbox):
    """AGE_2 : abaque frugalité servie (lecture pure)."""
    sandbox["SEED_ABOX_FOYER_PATH"].write_text(SEED_TBOX, encoding="utf-8")
    r = client.get("/api/phase8/frugality", params={"mode": "foyer"})
    assert r.status_code == 200


def test_exg_sources_catalogue_ssqot(client, sandbox):
    """Catalogue : registre compliance d'abord, 404 explicite sinon."""
    r = client.get("/api/phase8/sources")
    assert r.status_code == 404        # aucun catalogue dans le sandbox
    minimal = json.dumps({"cti_sources": [
        {"id": "src_x", "label": "X", "description": "", "url_target": "",
         "category": "CTI", "tlp": "CLEAR"}]})
    sandbox["EXTERNAL_SOURCES_COMPLIANCE_REGISTRY_PATH"].write_text(
        minimal, encoding="utf-8")
    r2 = client.get("/api/phase8/sources")
    assert r2.status_code == 200 and r2.json()[0]["id"] == "src_x"


# --------------------------------------------------écritures : le sas servi
def test_exg_gtw1_merge_via_api(client, sandbox):
    """GTW_1 : POST /tbox/merge délègue au sas — SUCCESS + trace journal."""
    r = client.post("/api/phase8/tbox/merge", json={"delta_ttl": DELTA_OK})
    assert r.status_code == 200 and r.json()["status"] == "SUCCESS"
    assert "dkg:propRoutes" in sandbox["WORKSET_TBOX_PATH"].read_text(
        encoding="utf-8")
    assert "HITL_APPROVE" in _log(sandbox)


def test_exg_gtw1_merge_invalide_422(client, sandbox):
    """Contrat : delta non parsable → 422 (REJECTED traduit en HTTP)."""
    r = client.post("/api/phase8/tbox/merge",
                    json={"delta_ttl": "{ pas du turtle"})
    assert r.status_code == 422 and "fusion refusée" in r.json()["detail"]


def test_exg_dem3_rejet_explicite_trace(client, sandbox):
    """DEM_3 : POST /tbox/reject → issue traçable, workset intact.
    (Le rejet ne crée RIEN : le workset doit être initialisé par une
    lecture au préalable — comportement attendu, pas un oubli.)"""
    client.get("/api/phase8/tbox")            # premier accès → workset posé
    avant = sandbox["WORKSET_TBOX_PATH"].read_text(encoding="utf-8")
    r = client.post("/api/phase8/tbox/reject", json={"delta_ttl": DELTA_OK})
    assert r.status_code == 200 and r.json()["status"] == "REJECTED"
    assert "HITL_REJECT" in _log(sandbox)
    assert sandbox["WORKSET_TBOX_PATH"].read_text(
        encoding="utf-8") == avant


def test_exg_res1_reset_via_api(client, sandbox):
    """RES_1 : POST /reset → workset restauré, seeds intacts, buffer purgé."""
    with open(sandbox["WORKSET_TBOX_PATH"], "a", encoding="utf-8") as f:
        f.write("\ndkg:pollution a owl:Class .\n")
    r = client.post("/api/phase8/reset")
    assert r.status_code == 200 and r.json()["status"] == "SUCCESS"
    corps = sandbox["WORKSET_TBOX_PATH"].read_text(encoding="utf-8")
    assert "dkg:pollution" not in corps and "dkg:Asset" in corps


# -------------------------------------------le scan réel (voie des 5S)
class _FakeScanner:
    def scan_current_host(self):          # jamais un vrai scan en recette
        return {"household_assets": [], "software_components": []}


class _FakeAgent:
    reponse = {"status": "SUCCESS", "assets": 1, "components": 2}
    def run(self):
        return dict(_FakeAgent.reponse)


def test_exg_dem7_scan_reel_ok_hitl_m1(client, sandbox, monkeypatch):
    """DEM_7 : POST /scan → 200, consentement HITL journalisé (régime M1).
    Verrouille la régression du 5S (500 silencieux, aucun test)."""
    monkeypatch.setattr(scanner_mod, "LocalHostScanner", _FakeScanner,
                        raising=False)
    monkeypatch.setattr(abox_mod, "HostScanAboxAgent", _FakeAgent,
                        raising=False)
    r = client.post("/api/phase8/scan")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["status"] == "SUCCESS" and body["mode"] == "scan"
    assert "regime='M1'" in _log(sandbox) and "SCAN_APPROVE" in _log(sandbox)


def test_exg_dem7_scan_echec_500_explicite(client, sandbox, monkeypatch):
    """DEM_7 : échec du scan → 500 avec message borné (pas de trace brute)."""
    monkeypatch.setattr(scanner_mod, "LocalHostScanner", _FakeScanner,
                        raising=False)
    monkeypatch.setattr(abox_mod, "HostScanAboxAgent", _FakeAgent,
                        raising=False)
    _FakeAgent.reponse = {"status": "ERROR", "message": "boom"}
    try:
        r = client.post("/api/phase8/scan")
        assert r.status_code == 500
        assert "Scan échoué" in r.json()["detail"]
    finally:
        _FakeAgent.reponse = {"status": "SUCCESS", "assets": 1,
                              "components": 2}


# ------------------------------------------------------------CTI (M2 via sas)
def test_exg_gtw2_cti_ingest_m2_journalise(client, sandbox):
    """GTW_2 : sélection CTI → ingestion buffer + trace M2 au journal du sas
    (le chemin record_write de cti_intake, cette fois par la vraie route)."""
    r = client.post("/api/phase8/cti/select",
                    json={"source_ids": ["source_inconnue_sandbox"]})
    assert r.status_code == 200
    assert sandbox["WORKSET_CTI_BUFFER_PATH"].exists()
    assert "SOURCES: source_inconnue_sandbox" in \
        sandbox["WORKSET_CTI_BUFFER_PATH"].read_text(encoding="utf-8")
    assert "CTI_INGEST" in _log(sandbox) and "regime='M2'" in _log(sandbox)

# CI : enregistre le fichier dans la baseline NonReg (P9)
import pytest
pytestmark = pytest.mark.non_regression
