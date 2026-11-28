# 03-Application/Test/test_eol_engine.py
"""
Recette brique C2 — moteur EOL (EXG-FWK-P9-EOL_1, EOL_2, EOL_3, FRG_1,
GTW_2) + greffon audit_engine V4. Sandbox : tous les chemins SSOT
(volume EOL, fonds, journal du sas) sont redirigés vers tmp_path via
monkeypatch — le poste réel (seeds, scan .private/, volumes de données)
n est JAMAIS touché (isolation RES_1, jamais réseau en test).
"""
import pytest
from rdflib import Graph, RDF, Namespace, URIRef, Literal

import core.config as settings
from core.eol_engine import ingest_eol_source, DKG_EOL_URI
from core.audit_engine import _generate_risk_analysis

pytestmark = pytest.mark.non_regression

DKG = Namespace("http://dkg.cybersec.org/tbox#")
DKG_EOL = Namespace(DKG_EOL_URI)         # http://dkg.cybersec.org/eol#
DKG_DATA = Namespace("http://dkg.cybersec.org/data#")

# ABox de recette (TLP:CLEAR simulé) : 1 actif, 2 composants — Ubuntu
# 16.04 (match strict avec le fonds) + Firefox 999 (sans correspondance
# EOL), l un porteur d une vulnérabilité pour tester l enrichissement.
ABOX_TTL = """
@prefix dkg: <http://dkg.cybersec.org/tbox#> .
@prefix dkg-data: <http://dkg.cybersec.org/data#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

dkg-data:Asset-Test a dkg:Asset ; rdfs:label "PC Test"@fr .
dkg-data:Comp-Ubuntu a dkg:SoftwareComponent ;
    rdfs:label "Ubuntu"@fr ; dkg:version "16.04 LTS" ;
    dkg:isComponentOf dkg-data:Asset-Test ;
    dkg:supportStatus "unknown" .
dkg-data:Comp-Firefox a dkg:SoftwareComponent ;
    rdfs:label "Firefox"@fr ; dkg:version "999.0" ;
    dkg:isComponentOf dkg-data:Asset-Test ;
    dkg:supportStatus "supported" .
dkg-data:Vuln-Test a dkg:Vulnerability ;
    rdfs:label "Vuln de recette"@fr ;
    dkg:cvssScore 9.5 ;
    dkg:isVulnerabilityOf dkg-data:Comp-Ubuntu .
dkg-data:Vuln-FF a dkg:Vulnerability ;
    rdfs:label "Vuln temoin Firefox"@fr ;
    dkg:cvssScore 7.0 ;
    dkg:isVulnerabilityOf dkg-data:Comp-Firefox .
"""


@pytest.fixture()
def eol_env(tmp_path, monkeypatch):
    """Sandbox SSOT : volume EOL + fonds + journal sas redirigés vers tmp.
    Le fonds est copié depuis le SSOT du repo (lecture seule)."""
    fonds_src = settings.EOL_FONDS_RECETTE_PATH
    assert fonds_src.exists(), f"Fonds EOL de recette introuvable : {fonds_src}"
    funds = tmp_path / "fonds"
    funds.mkdir()
    (funds / "eol_fonds_recette.ttl").write_text(
        fonds_src.read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.setattr(settings, "EOL_FONDS_RECETTE_PATH",
                        funds / "eol_fonds_recette.ttl")
    monkeypatch.setattr(settings, "ABOX_EXTERNE_EOL_PATH",
                        tmp_path / "DKG_EOL_Source.ttl")
    monkeypatch.setattr(settings, "WORKSET_HITL_AUDIT_LOG_PATH",
                        tmp_path / "hitl_validation_audit.log")
    return tmp_path


def _ingest(eol_env):
    return ingest_eol_source()


# --- EOL_1 : ingestion offline (recette 1) -----------------------------------
def test_eol1_ingestion_offline_ecrit_le_volume(eol_env):
    """Recette : EXG-FWK-P9-EOL_1 — Integration EOL (moteur)."""
    r = _ingest(eol_env)
    vol = settings.ABOX_EXTERNE_EOL_PATH
    assert vol.exists(), "le volume EOL doit etre ecrit dans l ABox Externe"
    assert r["eol_records_added"] == 5, "5 records attendus du fonds de recette"
    assert r["volume_triples"] >= 40
    assert settings.EOL_SOURCE_ID in r["sources_loaded"]
    assert r["remote_probe"]["status"] in ("stand-by", "offline", "live")

# --- EOL_2 : namespace + TLP par SELECTION SPARQL (jamais regex .ttl) --------
def test_eol2_namespace_et_marquage_tlp_par_sparql(eol_env):
    """Recette : EXG-FWK-P9-EOL_2 — Namespace dedie dkg-eol."""
    _ingest(eol_env)
    g = Graph()
    g.parse(str(settings.ABOX_EXTERNE_EOL_PATH), format="turtle")
    q = """
    PREFIX dkg-eol: <http://dkg.cybersec.org/eol#>
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    SELECT ?e ?tlp WHERE {
      ?e a dkg-eol:EndOfLife .
      OPTIONAL { ?e dkg:hasTLPMarking ?tlp }
    }"""
    rows = list(g.query(q))
    assert len(rows) == 5
    for row in rows:
        assert str(row.e).startswith(DKG_EOL_URI), \
            "instance hors du namespace dkg-eol (jamais dkg-data)"
        assert row.tlp is not None and str(row.tlp) == "TLP:CLEAR"

# --- EOL_3 : date xsd:date + sourceNote + successeur --------------------------
def test_eol3_dates_sourcenote_et_successeur(eol_env):
    """Recette : EXG-FWK-P9-EOL_3 — Date EOL sourcee, propagate, successeur."""
    _ingest(eol_env)
    g = Graph()
    g.parse(str(settings.ABOX_EXTERNE_EOL_PATH), format="turtle")
    q = """
    PREFIX dkg-eol: <http://dkg.cybersec.org/eol#>
    PREFIX dkg: <http://dkg.cybersec.org/tbox#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT ?e ?d ?sn ?sv WHERE {
      ?e a dkg-eol:EndOfLife ;
         dkg:eolDate ?d ;
         dkg:sourceNote ?sn .
      OPTIONAL { ?e dkg:successorVersion ?sv }
    }"""
    rows = list(g.query(q))
    assert len(rows) == 5
    for row in rows:
        assert isinstance(row.d, Literal) and \
            str(row.d.datatype) == "http://www.w3.org/2001/XMLSchema#date"
        assert str(row.sn).strip()
        assert row.sv is not None, "successorVersion attendu (fonds v2)"

# --- FRG_1 / idempotence : cumul, jamais de doublon ---------------------------
def test_frg1_cumul_idempotent_double_ingestion(eol_env):
    """Recette : EXG-FWK-P9-FRG_1 — Pipeline Frugal : cumul idempotent."""
    r1 = _ingest(eol_env)
    r2 = _ingest(eol_env)
    assert r1["eol_records_added"] == 5
    assert r2["eol_records_added"] == 0, "re-ingestion = 0 ajout (delta mort)"
    assert r2["volume_triples"] == r1["volume_triples"], \
        "RDF set : jamais de doublon, le volume ne grossit pas"

# --- GTW_2 : trace M2 au journal unique du sas, UNE seule ingestion ----------
def test_gtw2_sas_trace_m2_eol_ingest_unique(eol_env):
    """Recette : EXG-FWK-P9-GTW_2 — Regimes d Ecriture via la passerelle (trace M2)."""
    _ = _ingest(eol_env)
    log = settings.WORKSET_HITL_AUDIT_LOG_PATH.read_text(encoding="utf-8")
    assert "EOL_INGEST regime='M2'" in log
    _ = _ingest(eol_env)              # cumul sans ajout : PAS de nouvelle trace
    log2 = settings.WORKSET_HITL_AUDIT_LOG_PATH.read_text(encoding="utf-8")
    assert log2.count("EOL_INGEST") == 1, \
        "une ingestion sans ajout ne se retrace pas au sas"

# --- RES_1 : le fonds (intrant) reste intact ---------------------------------
def test_res1_fonds_et_seeds_intacts(eol_env):
    """Recette : EXG-MET-P8-RES_1 — Fonds et seeds intacts."""
    import hashlib
    funds = settings.EOL_FONDS_RECETTE_PATH
    before = hashlib.sha256(funds.read_bytes()).hexdigest()
    _ingest(eol_env)
    after = hashlib.sha256(funds.read_bytes()).hexdigest()
    assert before == after, "le fonds EOL est un intrant, jamais modifie"

# --- Greffon V4 : enrichissement du finding (EOL_3) ---------------------------
def test_greffon_v4_finding_enrichi_eol(eol_env):
    _ingest(eol_env)
    vol_ttl = settings.ABOX_EXTERNE_EOL_PATH.read_text(encoding="utf-8")
    bilan, _ = _generate_risk_analysis(ABOX_TTL, "", eol=vol_ttl)
    hits = [f for f in bilan if f.get("eol_date")]
    assert hits, "le composant Ubuntu 16.04 doit produire un finding EOL"
    f = hits[0]
    assert f["eol_date"] == "2021-04-01"
    assert f.get("eol_source_note"), "le triplet source (sourceNote) voyage"
    assert f.get("eol_version_installed") == "16.04 LTS"
    assert f.get("eol_successor_version")
    assert "Fin de support" in f["status"]

# --- Greffon V4 : non-régression, findings sans EOL inchangés ----------------
def test_greffon_v4_findings_non_eol_inchanges(eol_env):
    _ingest(eol_env)
    vol_ttl = settings.ABOX_EXTERNE_EOL_PATH.read_text(encoding="utf-8")
    base, delta_base = _generate_risk_analysis(ABOX_TTL, "", eol="# volume vide simulé")
    enrichi, delta_enrichi = _generate_risk_analysis(ABOX_TTL, "", eol=vol_ttl)
    fire = [f for f in enrichi if "Firefox" in f["component"]]
    assert fire, "le composant Firefox doit produire son finding habituel"
    assert not fire[0].get("eol_date"), "Firefox (sans record EOL) ne doit pas etre enrichi"
    assert [f for f in base if "Firefox" in f["component"]] == fire, \
        "le finding non-EOL doit rester strictement identique"

# --- V5 : la route expose le moteur (adaptateur fin) --------------------------
def test_v5_route_post_eol_ingest(eol_env):
    from fastapi.testclient import TestClient
    import main
    client = TestClient(main.app)
    resp = client.post("/api/phase8/eol/ingest")
    assert resp.status_code == 200
    body = resp.json()
    assert body["eol_records_added"] == 5
    assert settings.ABOX_EXTERNE_EOL_PATH.exists()

# --- Robustesse : intrants absents, jamais de crash ---------------------------
def test_intrant_absent_pas_de_crash(eol_env, monkeypatch):
    monkeypatch.setattr(settings, "EOL_FONDS_RECETTE_PATH",
                        eol_env / "inexistant.ttl")
    r = _ingest(eol_env)
    assert r["eol_records_added"] == 0, "fonds absent : 0 ajout, pas de crash"
    assert settings.ABOX_EXTERNE_EOL_PATH.exists()

# --- Robustesse : fonds corrompu, marqueur visible, pas de crash -------------
def test_fonds_corrompu_marqueur_visible_pas_de_crash(eol_env):
    settings.EOL_FONDS_RECETTE_PATH.write_text(
        "Ceci n est pas du Turtle du tout {{{{", encoding="utf-8")
    r = _ingest(eol_env)
    assert r["eol_records_added"] == 0, "fonds corrompu : ingestion ignoree"
    vol = settings.ABOX_EXTERNE_EOL_PATH.read_text(encoding="utf-8")
    assert "non parsable" in vol, "marqueur visible dans le volume EOL"
