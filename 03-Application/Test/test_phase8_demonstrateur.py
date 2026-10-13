# 03-Application/Test/test_phase8_demonstrateur.py
"""
Suite de tests d'intégration et de recette backend Phase 8 — v2 migrée.
Traçabilité : EXG-MET-P8-DEM_1, DEM_2, DEM_3, DEM_5 (audit trail),
DEM_6 (passerelle centrale), RES_1 (Seed/Reset),
EXG-FWK-P8-AGE_1 (Local-First SPARQL), EXG-FWK-P1-GOU_22 (vocabulaire).

Décisions actées v2 :
  - Statut 422 UNIFORME pour tout REJECTED (delta vide OU non parsable) :
    le refus est décidé à UN SEUL endroit (core/hitm_gateway.py — DEM_6).
  - Mocks recalés : core.hitm_gateway.approve_and_merge via le nom importé
    dans api.routes_phase8 ; chemins workset via core.config (monkeypatch).
  - Idempotence, rejet, reset et audit trail testés avec la VRAIE passerelle
    sur des fichiers temporaires (jamais le workspace réel ni les seeds).
"""

import re

import pytest
from unittest.mock import patch
from fastapi import FastAPI
from fastapi.testclient import TestClient

import core.config as settings
from api.routes_phase8 import router
from core.hitm_gateway import approve_and_merge

app = FastAPI()
app.include_router(router)
client = TestClient(app)

# Delta TBox PARSABLE (préfixes déclarés dans le delta lui-même) — DEM_3
VALID_DELTA_TTL = """@prefix dkg: <http://dkg.cybersec.org/tbox#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

dkg:hasThreatPattern a <http://www.w3.org/2002/07/owl#ObjectProperty> ;
    rdfs:domain dkg:Weakness ;
    rdfs:range dkg:ThreatPattern .
"""

# Delta NON parsable (préfixe soc1: jamais déclaré) — reproduit la pollution
# historique ; refusé par validate_delta (GOU_22) — DEM_3
INVALID_DELTA_TTL = "\nsoc1:TestClass rdfs:subClassOf soc1:BaseClass ."


# ------------------------------------------------------------------------------
# Fixtures : redirection des chemins workset vers tmp_path (RES_1 — les seeds
# et le workspace RÉEL ne sont jamais touchés par la suite de tests).
# ------------------------------------------------------------------------------
@pytest.fixture
def workset(tmp_path, monkeypatch):
    """EXG-MET-P8-RES_1 : environment workset isolé (tmp_path) pour les tests
    d'écriture (merge/reject/reset). Les seeds sont dupliqués en tmp."""
    seed_dir = tmp_path / "seed"
    work_dir = tmp_path / "workset"
    seed_dir.mkdir()
    work_dir.mkdir()
    seed_tbox = seed_dir / "DKG_TBox_DemoRef.ttl"
    seed_rules = seed_dir / "DKG_Rules_DemoRef.ttl"
    seed_tbox.write_text("# seed TBox (RES_1)\n", encoding="utf-8")
    seed_rules.write_text("# seed RBox (RES_1)\n", encoding="utf-8")
    for src in (settings.SEED_TBOX_DEMO_PATH, settings.SEED_RULES_DEMO_PATH):
        if src.exists():
            target = seed_tbox if "TBox" in src.name else seed_rules
            target.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    paths = {
        "tbox": work_dir / "DKG_TBox_Working.ttl",
        "rules": work_dir / "DKG_Rules_Working.ttl",
        "cti": work_dir / "cti_buffer.ttl",
        "log": work_dir / "hitl_validation_audit.log",
    }
    monkeypatch.setattr(settings, "SEED_TBOX_DEMO_PATH", seed_tbox)      # RES_1
    monkeypatch.setattr(settings, "SEED_RULES_DEMO_PATH", seed_rules)     # RES_1
    monkeypatch.setattr(settings, "WORKSET_TBOX_PATH", paths["tbox"])     # RES_1
    monkeypatch.setattr(settings, "WORKSET_RULES_PATH", paths["rules"])  # RES_1
    monkeypatch.setattr(settings, "WORKSET_CTI_BUFFER_PATH", paths["cti"])      # AGE_1
    monkeypatch.setattr(settings, "WORKSET_HITL_AUDIT_LOG_PATH", paths["log"])  # DEM_5
    return paths


# ------------------------------------------------------------------------------
# EXG-FWK-P8-AGE_1 — Catalogue SSOT des sources externes
# ------------------------------------------------------------------------------
@pytest.mark.non_regression
def test_get_external_sources_catalog_exg_fwk_p8_age_1():
    """Exigence: EXG-FWK-P8-AGE_1 - Catalogue maître JSON lu via le chemin SSOT (EXG-FWK-P8-AGE_1)."""
    response = client.get("/api/phase8/sources")                       # AGE_1
    assert response.status_code in (200, 404)                         # AGE_1
    if response.status_code == 200:
        assert isinstance(response.json(), list)                      # AGE_1


# ------------------------------------------------------------------------------
# EXG-MET-P8-DEM_1 — TBox affichée dès le chargement + Tri-Boîtes + RBox
# ------------------------------------------------------------------------------
@pytest.mark.non_regression
def test_tbox_loaded_on_start_exg_met_p8_dem_1():
    """Exigence: EXG-MET-P8-DEM_1 - La TBox doit être servie dès l'ouverture (UI_Render_3_TTL_Zones)."""
    response = client.get("/api/phase8/tbox")                          # DEM_1
    assert response.status_code == 200                                # DEM_1
    data = response.json()
    assert "tbox_ttl" in data and isinstance(data["tbox_ttl"], str)   # DEM_1
    assert "soc1:SMBv1Service" not in data["tbox_ttl"]  # bloc polluant absent


@pytest.mark.non_regression
def test_rbox_served_on_trigger_exg_met_p8_dem_1():
    """Exigence: EXG-MET-P8-DEM_1 - La RBox est servie à chaque trigger (coche/mode) — raisonnement local."""
    response = client.get("/api/phase8/rbox")                          # DEM_1
    assert response.status_code == 200                                # DEM_1
    assert "rbox_ttl" in response.json()                              # DEM_1


@pytest.mark.non_regression
def test_audit_tri_boxes_render_exg_met_p8_dem_1():
    """Exigence: EXG-MET-P8-DEM_1 - Audit : les 3 zones Tri-Boîtes sont présentes dans la réponse."""
    response = client.post("/api/phase8/audit",                        # DEM_1
                           json={"mode": "foyer", "enabled_network_sources": []})
    assert response.status_code == 200                                # DEM_1
    data = response.json()
    for key in ("tbox_ttl", "abox_ttl", "cti_clear_ttl", "nl_bilan"):
        assert key in data                                            # DEM_1


# ------------------------------------------------------------------------------
# EXG-MET-P8-DEM_2 — Air-Gapped : 0 coche => 0 requête HTTP
# ------------------------------------------------------------------------------
@pytest.mark.non_regression
def test_audit_air_gapped_zero_network_exg_met_p8_dem_2():
    """Exigence: EXG-MET-P8-DEM_2 - 0 source cochée => 0 requête réseau émise (HTTP_Requests_Count == 0)."""
    payload = {"mode": "foyer", "enabled_network_sources": []}         # DEM_2
    with patch("httpx.AsyncClient.get") as mock_httpx, \
         patch("requests.get") as mock_requests:
        response = client.post("/api/phase8/audit", json=payload)     # DEM_2
        assert response.status_code == 200
        data = response.json()
        assert data["network_requests_made"] == 0                     # DEM_2
        mock_httpx.assert_not_called()                                # DEM_2
        mock_requests.assert_not_called()                             # DEM_2


@pytest.mark.non_regression
def test_audit_with_network_toggle_exg_met_p8_dem_2():
    """Exigence: EXG-MET-P8-DEM_2 - N sources cochées => compteur réseau == N (consigne sélective)."""
    payload = {"mode": "foyer",
               "enabled_network_sources": ["SRC_EOL_CTI", "SRC_CISA_KEV"]}
    response = client.post("/api/phase8/audit", json=payload)          # DEM_2
    assert response.status_code == 200                                # DEM_2
    assert response.json()["network_requests_made"] == 2              # DEM_2


@pytest.mark.non_regression
def test_bilan_computed_from_abox_exg_fwk_p8_age_1():
    """Exigence: EXG-FWK-P8-AGE_1 - Le bilan NL est calculé depuis le contenu ABox réel (Local-First)."""
    response = client.post("/api/phase8/audit",                        # AGE_1
                           json={"mode": "foyer", "enabled_network_sources": []})
    assert response.status_code == 200                                # AGE_1
    bilan = response.json()["nl_bilan"]
    assert isinstance(bilan, list) and len(bilan) >= 1                # AGE_1
    for item in bilan:                                                # AGE_1
        assert {"equipment", "component", "status",
                "severity", "action"} <= set(item)                    # AGE_1


# ------------------------------------------------------------------------------
# EXG-MET-P8-DEM_3 + DEM_6 — Gatekeeper HITL centralisé dans la passerelle
# ------------------------------------------------------------------------------
@pytest.mark.non_regression
def test_tbox_merge_hitl_gatekeeper_exg_met_p8_dem_3():
    """Exigence: EXG-MET-P8-DEM_3
    Delta vide => 422 ; delta invalide (rdflib) => 422 ; valide => 200.
    Option B actée : refus UNIFORME 422 — la décision vit dans la passerelle
    (core/hitm_gateway.py), la route reste un adaptateur pur (DEM_6)."""
    # 1. Delta vide refusé par la passerelle, exposé en 422 — DEM_3/DEM_6
    empty = client.post("/api/phase8/tbox/merge",
                        json={"delta_ttl": "   "})                     # DEM_3
    assert empty.status_code == 422                                   # DEM_3
    assert "vide" in empty.json()["detail"].lower()                   # DEM_3

    # 2. Delta non parsable refusé (validate_delta, GOU_22) — DEM_3
    bad = client.post("/api/phase8/tbox/merge",
                      json={"delta_ttl": INVALID_DELTA_TTL})           # DEM_3
    assert bad.status_code == 422                                     # DEM_3
    assert "invalide" in bad.json()["detail"].lower()                 # DEM_3

    # 3. Delta valide : fusion UNIQUEMENT via le endpoint HITL explicite,
    #    délégué à core.hitm_gateway.approve_and_merge (DEM_6).
    with patch("api.routes_phase8.approve_and_merge",
               return_value={"status": "SUCCESS",
                             "message": "Delta validé et fusionné (mock)."}
               ) as mock_merge:                                       # DEM_6
        good = client.post("/api/phase8/tbox/merge",
                           json={"delta_ttl": VALID_DELTA_TTL})        # DEM_3
        assert good.status_code == 200                                # DEM_3
        assert good.json()["status"] == "SUCCESS"                     # DEM_3
        mock_merge.assert_called_once_with(VALID_DELTA_TTL)           # DEM_6


@pytest.mark.non_regression
def test_tbox_merge_never_automatic_exg_met_p8_dem_3():
    """Exigence: EXG-MET-P8-DEM_3
    Aucun appel audit ne déclenche l'écriture TBox (DEM_3) : le symbole
    délégué approve_and_merge (importé dans routes) ne doit jamais être
    appelé hors endpoint /tbox/merge explicite."""
    with patch("api.routes_phase8.approve_and_merge") as mock_merge:   # DEM_6
        client.post("/api/phase8/audit",
                    json={"mode": "foyer",
                          "enabled_network_sources": []})             # DEM_3
        mock_merge.assert_not_called()  # TBox_Master_Modified only if APPROVE


@pytest.mark.non_regression
def test_tbox_merge_idempotent_noop_exg_met_p8_dem_3(workset):
    """Exigence: EXG-MET-P8-DEM_3
    Vraie passerelle, workset tmp : 1er appel SUCCESS (delta écrit UNE
    fois, GOU_5 un seul exemplaire), 2e appel NOOP (0 doublon), audit trail
    DEM_5 contient APPROVE puis NOOP(already-merged)."""
    assert not workset["tbox"].exists()                               # RES_1
    r1 = client.post("/api/phase8/tbox/merge",
                     json={"delta_ttl": VALID_DELTA_TTL})             # DEM_3
    assert r1.status_code == 200 and r1.json()["status"] == "SUCCESS"  # DEM_3
    r2 = client.post("/api/phase8/tbox/merge",
                     json={"delta_ttl": VALID_DELTA_TTL})              # DEM_3
    assert r2.status_code == 200 and r2.json()["status"] == "NOOP"     # DEM_3
    content = workset["tbox"].read_text(encoding="utf-8")             # GOU_5
    assert content.count("dkg:hasThreatPattern a") == 1  # 0 doublon  # DEM_3
    log = workset["log"].read_text(encoding="utf-8")                  # DEM_5
    assert "HITL_APPROVE user_click='APPROVE'" in log                 # DEM_5
    assert "NOOP(already-merged)" in log                              # DEM_5


@pytest.mark.non_regression
def test_tbox_reject_journalized_exg_met_p8_dem_3(workset):
    """Exigence: EXG-MET-P8-DEM_3
    POST /tbox/reject : issue explicite REJECTED + décision journalisée
    dans l'audit trail (DEM_3/DEM_5), AUCUNE écriture du workset."""
    before = (workset["tbox"].read_text(encoding="utf-8")
              if workset["tbox"].exists() else "")                    # DEM_3
    r = client.post("/api/phase8/tbox/reject",
                    json={"delta_ttl": VALID_DELTA_TTL})              # DEM_3
    assert r.status_code == 200                                       # DEM_3
    assert r.json()["status"] == "REJECTED"                           # DEM_3
    after = (workset["tbox"].read_text(encoding="utf-8")
             if workset["tbox"].exists() else "")                     # DEM_3
    assert after == before  # rien d'écrit sur rejet                 # DEM_3
    log = workset["log"].read_text(encoding="utf-8")                  # DEM_5
    assert "HITL_REJECT" in log and "REJECT(by-operator)" in log      # DEM_5


# ------------------------------------------------------------------------------
# EXG-MET-P8-RES_1 — Seed/Reset : seeds JAMAIS modifiés, workset restauré
# ------------------------------------------------------------------------------
@pytest.mark.non_regression
def test_reset_restores_workset_seeds_intact_exg_met_p8_res_1(workset):
    """Exigence: EXG-MET-P8-RES_1
    POST /reset : workset recopié depuis les seeds, buffer CTI purgé,
    seeds inchangés (byte-identical avant/après)."""
    seed_before = settings.SEED_TBOX_DEMO_PATH.read_text(encoding="utf-8")
    workset["tbox"].write_text("# workset corrompu par la démo",       # RES_1
                               encoding="utf-8")
    workset["cti"].write_text("# buffer CTI résiduel", encoding="utf-8")
    r = client.post("/api/phase8/reset")                               # RES_1
    assert r.status_code == 200 and r.json()["status"] == "SUCCESS"    # RES_1
    assert workset["tbox"].read_text(encoding="utf-8") == seed_before  # RES_1
    assert "résiduel" not in workset["cti"].read_text(encoding="utf-8")
    seed_after = settings.SEED_TBOX_DEMO_PATH.read_text(encoding="utf-8")
    assert seed_after == seed_before  # seed JAMAIS modifié            # RES_1


@pytest.mark.non_regression
def test_ensure_workset_initialized_on_first_access_exg_met_p8_res_1(workset):
    """Exigence: EXG-MET-P8-RES_1
    GET /tbox sans workset => reset automatique depuis les seeds (RES_1),
    puis service normal de la TBox workset."""
    assert not workset["tbox"].exists()                               # RES_1
    r = client.get("/api/phase8/tbox")                                # DEM_1
    assert r.status_code == 200                                       # RES_1
    assert workset["tbox"].exists()  # workset posé depuis le seed     # RES_1
    assert r.json()["tbox_source"] == "workset"                       # RES_1


# ------------------------------------------------------------------------------
# CTI CLEAR — chargement différé + persistance dans le buffer workset (AGE_1)
# ------------------------------------------------------------------------------
@pytest.mark.non_regression
def test_cti_lazy_select_and_buffer_exg_fwk_p8_age_1(workset):
    """Exigence: EXG-FWK-P8-AGE_1
    POST /cti/select retourne le sous-graphe et l'écrit dans le buffer
    workset (settings.WORKSET_CTI_BUFFER_PATH — anciennement
    SELECTED_CTI_BUFFER_PATH, supprimé de routes_phase8)."""
    r = client.post("/api/phase8/cti/select",                          # AGE_1
                    json={"source_ids": ["SRC_EOL_CTI"]})
    assert r.status_code == 200                                       # AGE_1
    data = r.json()
    assert "cti_clear_ttl" in data                                   # AGE_1
    assert workset["cti"].exists()  # buffer workset persisté          # AGE_1
    assert data["cti_clear_ttl"] == workset["cti"].read_text(
        encoding="utf-8")  # réponse == contenu fichier (SSOT)         # AGE_1


# ------------------------------------------------------------------------------
# EXG-MET-P8-DEM_4b — Vue superposition verticale par alerte (TLP:RED/CTI vert)
# ------------------------------------------------------------------------------
@pytest.mark.non_regression
def test_superposition_graph_vertical_tlp_colors_exg_met_p8_dem_4b():
    """Exigence: EXG-MET-P8-DEM_4B
    GET /superposition/graph : flowchart TD VERTICAL, nœuds internes
    TLP:RED (classe intern) et externes TLP:CLEAR (classe extern) ; lecture
    pure (aucune écriture)."""
    if not settings.SEED_ABOX_HOTE_PATH.exists():                     # DEM_4b
        pytest.skip("Seeds §29 non posés sur cette machine (DEM_4b)")
    r = client.get("/api/phase8/superposition/graph",                  # DEM_4b
                   params={"mode": "hote",
                           "equipment": "Serveur Authentification Central"})
    assert r.status_code == 200                                        # DEM_4b
    m = r.json()["mermaid"]
    assert m.startswith("flowchart TD")  # VERTICAL (DEM_4b)           # DEM_4b
    assert "TLP:RED" in m and "Log4" in m                              # DEM_4b
    assert "classDef intern" in m and "classDef extern" in m           # DEM_4b


@pytest.mark.non_regression
def test_superposition_flags_undeclared_cti_vocab_exg_fwk_p1_gou_22(workset):
    """Exigence: EXG-FWK-P1-GOU_22
    Lien exploitsWeakness du CTI non déclaré en TBox de référence =>
    marqué ⚠️ (GOU_22, rupture de raisonnement visible) ; après merge HITL
    déclarant la propriété dans le workset, le ⚠️ disparaît (boucle bouclée)."""
    if not settings.SEED_ABOX_HOTE_PATH.exists():                     # GOU_22
        pytest.skip("Seeds §29 non posés sur cette machine (GOU_22)")
    # CORRECTIF v3.1 (12/10) : déclencher l'auto-init RES_1 AVANT d'écrire le
    # buffer — sinon ensure_workset_initialized() => reset_demo() purge le
    # buffer qu'on vient de poser (constaté : X3 rendu via skos:exactMatch
    # de l'ABox, mais aucun lien exploitsWeakness ni ⚠️).
    client.get("/api/phase8/tbox")                                    # RES_1
    workset["cti"].write_text(                                         # AGE_1
        "@prefix dkg: <http://dkg.cybersec.org/tbox#> .\n"
        "@prefix dkg-cti: <http://dkg.cybersec.org/cti#> .\n"
        "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n"
        "dkg-cti:CVE-2021-44228 a dkg:Vulnerability ;\n"
        "    dkg:cveId \"CVE-2021-44228\" ;\n"
        "    dkg:exploitsWeakness dkg-cti:CWE-502 .\n", encoding="utf-8")
    params = {"mode": "hote", "equipment": "Serveur Authentification Central"}
    r1 = client.get("/api/phase8/superposition/graph", params=params)  # GOU_22
    assert r1.status_code == 200
    m1 = r1.json()["mermaid"]
    assert "exploitsWeakness" in m1 and "⚠️" in m1  # non déclarée => ⚠️ (GOU_22)
    # Merge HITL déclarant la propriété => le ⚠️ disparaît (boucle bouclée)
    delta = ("@prefix dkg: <http://dkg.cybersec.org/tbox#> .\n"
             "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
             "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
             "dkg:exploitsWeakness a owl:ObjectProperty ;\n"
             "    rdfs:domain dkg:Vulnerability ; rdfs:range dkg:Weakness .\n")
    rmerge = client.post("/api/phase8/tbox/merge",
                         json={"delta_ttl": delta})                   # DEM_3
    assert rmerge.status_code == 200 and rmerge.json()["status"] == "SUCCESS"
    r2 = client.get("/api/phase8/superposition/graph", params=params)  # GOU_22
    m2 = r2.json()["mermaid"]
    assert "exploitsWeakness" in m2 and "⚠️" not in m2  # déclaré => OK (GOU_22)


# EXG-FWK-P8-AGE_2 — Abaque Green-Dev : volumes chargés vs disponibles
# ------------------------------------------------------------------------------
@pytest.mark.non_regression
def test_frugality_abaque_green_dev_exg_fwk_p8_age_2():
    """Exigence: EXG-FWK-P8-AGE_2
    GET /frugality : ratio chargé/disponible cohérent (<= 100), TOP
    entités non vide et trié décroissant, .private/ exclu (TLP:RED)."""
    if not settings.SEED_ABOX_HOTE_PATH.exists():                     # AGE_2
        pytest.skip("Seeds §29 non posés sur cette machine (AGE_2)")
    r = client.get("/api/phase8/frugality", params={"mode": "hote"})   # AGE_2
    assert r.status_code == 200
    f = r.json()
    assert 0 < f["loaded_total_bytes"] <= f["available_total_bytes"]    # AGE_2
    assert 0 < f["loaded_vs_available_pct"] <= 100.0
    top = f["top_entities"]
    assert top and top[0]["triplets"] >= top[-1]["triplets"]           # tri décroissant
    assert all(e["triplets"] > 0 for e in top)


# ------------------------------------------------------------------------------
# EXG-FWK-P1-GOU_22 — Cohérence vocabulaire ABox / TBox de référence
# ------------------------------------------------------------------------------
@pytest.mark.non_regression
def test_abox_tbox_vocabulary_coherence_exg_fwk_p1_gou_22():
    """Exigence: EXG-FWK-P1-GOU_22
    L'ABox seed ne doit utiliser que des propriétés déclarées dans la
    TBox de référence (workset). Base saine §25 : exposesService,
    hasThreatPattern, etc. y sont déclarées => 0 proposition HITL au
    premier audit ; exploitsWeakness/isCisaKev restent hors ABox."""
    abox_path = settings.SEED_ABOX_FOYER_PATH                         # GOU_22
    tbox_path = settings.WORKSET_TBOX_PATH                            # GOU_22
    if not (hasattr(settings, "SEED_ABOX_FOYER_PATH")
            and abox_path.exists() and tbox_path.exists()):
        pytest.skip("Seeds §29 / workset non posés sur cette machine (GOU_22)")
    abox = abox_path.read_text(encoding="utf-8")                      # GOU_22
    tbox = tbox_path.read_text(encoding="utf-8")                      # GOU_22
    declared = set(re.findall(r"^dkg:(\w+)\s+a\s+owl:(?:Object|Datatype)Property",
                             tbox, flags=re.M))                       # GOU_22
    used = set(re.findall(r"dkg:(\w+)\s+", abox))                     # GOU_22
    class_decls = set(re.findall(r"^dkg:(\w+)\s+a\s+owl:Class",
                                 tbox, flags=re.M))                   # GOU_22
    for prop in used:                                                 # GOU_22
        if prop[0].islower():  # propriétés (minuscule) vs classes     # GOU_22
            assert prop in declared or prop in class_decls or \
                prop in {"hasTLPMarking"}, \
                f"EXG-FWK-P1-GOU_22 : dkg:{prop} utilisée en ABox " \
                f"mais absente de la TBox de référence"
    assert "dkg:exploitsWeakness" not in abox, \
        "EXG-FWK-P1-GOU_22 : exploitsWeakness appartient au CTI coché, " \
        "pas à l'ABox seed"
