# 03-Application/Test/test_hitm_gateway.py
"""
TEST — sas hitm_gateway (brique C1, P9) — recette/EXG :
  EXG-FWK-P9-GTW_1 (exposition API+MCP du sas), GTW_2 (régimes d'écriture,
  SHACL sur M1), EXG-MET-P8-DEM_3 (fusion/rejet explicites), DEM_5 (audit
  trail), EXG-MET-P8-RES_1 (reset, seeds intacts), EXG-FWK-P1-GOU_22.
Chaque test détourne les chemins SSOT vers tmp — zéro écriture sur le
workset réel du poste, zéro dépendance réseau.
"""
import hashlib

import pytest

import core.config as settings
import core.hitm_gateway as gateway
from core.hitm_gateway import (approve_and_merge, reject, reset_demo,
                               ensure_workset_initialized, record_write,
                               validate_delta_shacl)

# ----------------------------------------------------------------JEUX DE DONNÉES
SEED_TBOX = """@prefix dkg: <http://dkg.cybersec.org/tbox#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
dkg:Asset a owl:Class .
"""
SEED_RULES = "# règles locales seed (sandbox)\n"
# Shape M1 : toute instance de dkg:Flaged doit avoir dkg:flag entier.
SHACL_MASTER = """@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix dkg: <http://dkg.cybersec.org/tbox#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
[ a sh:NodeShape ;
  sh:targetClass dkg:Flaged ;
  sh:property [ sh:path dkg:flag ; sh:datatype xsd:integer ] ] .
"""
DELTA_OK = """@prefix dkg: <http://dkg.cybersec.org/tbox#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
dkg:newProp a owl:DatatypeProperty ; dkg:flag 42 .
"""
DELTA_OK2 = """@prefix dkg: <http://dkg.cybersec.org/tbox#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
dkg:node2 a dkg:Flaged ; dkg:flag 7 .
"""
DELTA_SHACL_KO = """@prefix dkg: <http://dkg.cybersec.org/tbox#> .
dkg:node1 a dkg:Flaged ; dkg:flag "abc" .
"""


@pytest.fixture()
def sandbox(monkeypatch, tmp_path):
    """Détourne tout chemin SSOT du sas vers tmp, pose les seeds et reset."""
    paths = {
        "WORKSET_TBOX_PATH": tmp_path / "DKG_TBox_Working.ttl",
        "WORKSET_RULES_PATH": tmp_path / "DKG_RuleSet_Working.rq",
        "WORKSET_CTI_BUFFER_PATH": tmp_path / "cti_buffer.ttl",
        "WORKSET_HITL_AUDIT_LOG_PATH": tmp_path / "hitl_audit.log",
        "SEED_TBOX_DEMO_PATH": tmp_path / "seed_tbox.ttl",
        "SEED_RULES_DEMO_PATH": tmp_path / "seed_rules.rq",
        "SHACL_MASTER_PATH": tmp_path / "DKG_SHACL_Master.ttl",
    }
    for name, path in paths.items():
        monkeypatch.setattr(settings, name, path)
    paths["SEED_TBOX_DEMO_PATH"].write_text(SEED_TBOX, encoding="utf-8")
    paths["SEED_RULES_DEMO_PATH"].write_text(SEED_RULES, encoding="utf-8")
    paths["SHACL_MASTER_PATH"].write_text(SHACL_MASTER, encoding="utf-8")
    reset_demo()  # working set initialisé depuis les seeds du sandbox
    return paths


def _log(sandbox):
    p = sandbox["WORKSET_HITL_AUDIT_LOG_PATH"]
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


# -------------------------------------------------------------GTW_2 : SHACL M1
def test_exg_gtw_01_merge_shacl_accept(sandbox):
    """GTW_2/M1 : delta conforme (rdflib + SHACL) → SUCCESS + workset enrichi."""
    r = approve_and_merge(DELTA_OK)
    assert r["status"] == "SUCCESS", r
    assert "SHACL" in r["message"]
    assert "dkg:newProp" in sandbox["WORKSET_TBOX_PATH"].read_text(encoding="utf-8")


def test_exg_gtw_02_merge_shacl_reject(sandbox):
    """GTW_2/M1 : delta cassant une shape → REJECTED, workset INTACT."""
    r = approve_and_merge(DELTA_SHACL_KO)
    assert r["status"] == "REJECTED", r
    assert "SHACL" in r["message"]
    assert "dkg:node1" not in sandbox["WORKSET_TBOX_PATH"].read_text(encoding="utf-8")
    assert "REJECT(shacl)" in _log(sandbox)


def test_exg_gtw_03_validate_delta_shacl_pure(sandbox):
    """Le contrôle SHACL est une fonction pure : jamais d'écriture."""
    before = sandbox["WORKSET_TBOX_PATH"].read_text(encoding="utf-8")
    ok, detail = validate_delta_shacl(DELTA_SHACL_KO)
    assert not ok and "violation" in detail
    ok2, _ = validate_delta_shacl(DELTA_OK2)
    assert ok2
    assert sandbox["WORKSET_TBOX_PATH"].read_text(encoding="utf-8") == before


def test_exg_gtw_04_merge_idempotent_noop(sandbox):
    """EXG-MET-P8-DEM_3/GOU_5 : re-fusion du même delta → NOOP, aucun doublon."""
    approve_and_merge(DELTA_OK)
    r = approve_and_merge(DELTA_OK)
    assert r["status"] == "NOOP", r
    body = sandbox["WORKSET_TBOX_PATH"].read_text(encoding="utf-8")
    assert body.count("dkg:newProp a owl:DatatypeProperty") == 1
    assert "NOOP(already-merged)" in _log(sandbox)


def test_exg_gtw_05_merge_unparsable_reject(sandbox):
    """GOU_22 : delta non parsable → REJECT, zéro écriture."""
    r = approve_and_merge("{ pas du turtle du tout")
    assert r["status"] == "REJECTED", r
    assert "parse" in r["message"]
    assert "REJECT(unparsable)" in _log(sandbox)


def test_exg_gtw_06_merge_empty_reject(sandbox):
    """Delta vide → issue explicite REJECTED (pas d'erreur silencieuse)."""
    r = approve_and_merge("   ")
    assert r["status"] == "REJECTED", r
    assert "REJECT(empty)" in _log(sandbox)


# ------------------------------------------------------------DEM_3/DEM_5 : issue
def test_exg_gtw_07_reject_operator_traced(sandbox):
    """DEM_3 : le rejet est explicite et journalisé (DEM_5)."""
    r = reject(DELTA_OK)
    assert r["status"] == "REJECTED"
    assert "HITL_REJECT" in _log(sandbox) and "REJECT(by-operator)" in _log(sandbox)


def test_exg_gtw_08_record_write_m2(sandbox):
    """GTW_2 : preuve M2 au journal unique — format régime + SHA + UTC."""
    record_write("M2", "CTI_INGEST", detail="3 CVE ajoutées",
                 target="WORKSET_CTI_BUFFER")
    ligne = [l for l in _log(sandbox).splitlines() if "CTI_INGEST" in l][0]
    assert "regime='M2'" in ligne and "delta_sha256=" in ligne \
        and ligne.startswith("[20") and "target='WORKSET_CTI_BUFFER'" in ligne


def test_exg_gtw_09_record_write_m1_scan(sandbox):
    """GTW_2 : la même preuve pour le régime M1 (scan du poste)."""
    record_write("M1", "SCAN_APPROVE",
                 detail="scan local non intrusif (TLP:RED)",
                 target=".private/")
    ligne = [l for l in _log(sandbox).splitlines() if "SCAN_APPROVE" in l][0]
    assert "regime='M1'" in ligne and "target='.private/'" in ligne


# ----------------------------------------------------------------RES_1 : seeds
def test_exg_gtw_10_reset_seed_intact(sandbox):
    """RES_1 : le reset restaure le working set et ne JAMAIS toucher les seeds."""
    sha_seed_avant = _sha(sandbox["SEED_TBOX_DEMO_PATH"])
    with open(sandbox["WORKSET_TBOX_PATH"], "a", encoding="utf-8") as f:
        f.write("\ndkg:pollution a owl:Class .\n")
    r = reset_demo()
    assert r["status"] == "SUCCESS", r
    assert _sha(sandbox["SEED_TBOX_DEMO_PATH"]) == sha_seed_avant
    assert "dkg:pollution" not in \
        sandbox["WORKSET_TBOX_PATH"].read_text(encoding="utf-8")
    assert "HITL_RESET" in _log(sandbox)


def test_exg_gtw_11_ensure_init_auto_reset(sandbox):
    """Premier accès : working set absent => restauration automatique des seeds."""
    sandbox["WORKSET_TBOX_PATH"].unlink()
    ensure_workset_initialized()
    assert sandbox["WORKSET_TBOX_PATH"].read_text(encoding="utf-8") == SEED_TBOX


# -------------------------------------------------GTW_1 : exposition MCP du sas
def test_exg_gtw_12_mcp_tools_sas(sandbox):
    """GTW_1 : les 4 outils hitm_* du registre délèguent au sas (core.*)."""
    from core.mcp_server import DKGMCPRegistry
    r = DKGMCPRegistry.call_tool("hitm_merge_delta", {"delta_ttl": DELTA_OK})
    assert r["status"] == "SUCCESS", r
    r = DKGMCPRegistry.call_tool("hitm_reject_delta", {"delta_ttl": DELTA_OK2})
    assert r["status"] == "REJECTED"
    r = DKGMCPRegistry.call_tool("hitm_reset_workset", {})
    assert r["status"] == "SUCCESS"
    r = DKGMCPRegistry.call_tool("hitm_audit_tail", {})
    assert isinstance(r["log_tail"], list) and len(r["log_tail"]) > 0
    assert any("HITL_RESET" in l for l in r["log_tail"])


def test_exg_gtw_13_mcp_tools_registered(sandbox):
    """GTW_1 : les outils du sas sont déclarés dans le registre (contrat)."""
    from core.mcp_server import DKGMCPRegistry
    names = {t["name"] for t in DKGMCPRegistry.list_tools()}
    assert {"hitm_merge_delta", "hitm_reject_delta",
            "hitm_reset_workset", "hitm_audit_tail"} <= names
