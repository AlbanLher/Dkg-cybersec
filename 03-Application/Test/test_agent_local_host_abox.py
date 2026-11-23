# 03-Application/Test/test_agent_local_host_abox.py
"""
TEST — agent_local_host_abox (scan réel → ABox TLP:RED, .private/) —
recette/EXG :
  EXG-TEC-P2-ABO_1 (namespace instance dédié data# + format canonique des IDs),
  EXG-FWK-P2-ABO_3 (matérialisation des relations inverses — dette D3),
  EXG-TEC-P07-mi_1 (immuabilité Pydantic frozen + parsers défensifs — dette D8),
  EXG-FWK-P1-GOU_11 (marquage TLP présent sur le graphe généré).
Sandbox : les chemins SSOT portés par le module sont détournés vers tmp —
zéro écriture dans le vrai .private/, zéro réseau.
"""
import json

import pytest
from pydantic import ValidationError
from rdflib import Graph, Namespace, RDF, URIRef

import core.agent_local_host_abox as agent_mod
from core.agent_local_host_abox import (HostScanAboxAgent, HostScanModel,
                                         ScannedAssetModel)

DKG = Namespace("http://dkg.cybersec.org/tbox#")
DKG_DATA = Namespace("http://dkg.cybersec.org/data#")

SCAN = {
    "household_assets": [{
        "asset_id": "a515-f",
        "name": "Poste de Travail Hôte(a515-f)",
        "ip_address": "127.0.0.1",
        "os": "Ubuntu 24.04 LTS",
        "exposed_services": ["ssh", "fastapi-mcp"],
        "zone": "LAN-SECURE",
    }],
    "software_components": [
        {"component_id": "comp-git", "name": "Git",
         "version": "2.43.0", "support_status": "active"},
        {"component_id": "comp-jdk", "name": "OpenJDK",
         "version": "21", "support_status": "active"},
    ],
}


@pytest.fixture()
def sandbox(monkeypatch, tmp_path):
    """Détourne les chemins du MODULE (valeurs liées à l'import)."""
    scan = tmp_path / "host_scan.json"
    abox = tmp_path / "DKG_ABox_HostScan.ttl"
    monkeypatch.setattr(agent_mod, "SECURE_INPUT_HOST_SCAN_PATH", scan)
    monkeypatch.setattr(agent_mod, "SECURE_ABOX_HOST_SCAN_PATH", abox)
    scan.write_text(json.dumps(SCAN, ensure_ascii=False), encoding="utf-8")
    return {"scan": scan, "abox": abox}


def _run_ok(sandbox):
    """Pipeline complet sur le sandbox — doit être SUCCESS."""
    r = HostScanAboxAgent().run()
    assert r["status"] == "SUCCESS", r
    abox = Graph().parse(str(sandbox["abox"]), format="turtle")
    return r, abox


# ---------------------------------------------ABO_1 : namespace & format IDs
def test_exg_abo1_namespace_data_dedie(sandbox):
    """EXG-TEC-P2-ABO_1 : les INSTANCES vivent exclusivement en data#.
    Les termes de la TBox (classes référencées comme objet de rdf:type)
    sont légitimement en tbox# — vocabulaire TBox-first (ABO_1 porte sur
    les instances, pas sur le vocabulaire cité)."""
    r, abox = _run_ok(sandbox)
    for s, p, o in abox:
        # exception vocabulaire : l'objet d'un rdf:type est une CLASSE TBox
        noeuds = [s] if p == RDF.type else [s, o]
        for noeud in noeuds:
            if isinstance(noeud, URIRef) and "dkg.cybersec.org" in str(noeud):
                assert str(noeud).startswith("http://dkg.cybersec.org/data#"), \
                    f"instance hors namespace dédié : {noeud}"
    # Format canonique des IDs instances (comp-* / Asset-Host-Scan)
    comp_ids = [str(s) for s in abox.subjects(RDF.type, DKG.SoftwareComponent)]
    assert all(str(DKG_DATA.Comp) in c or "Comp-Scan" in c for c in comp_ids)
    assert len(comp_ids) == len(SCAN["software_components"])


# ---------------------------------------------------ABO_3 : inverses (dette D3)
def test_exg_abo3_paires_inverses_completes(sandbox):
    """EXG-FWK-P2-ABO_3 : toute relation a sa déclarée inverse matérialisée
    (isComponentOf ↔ hasInstalledComponent : paires complètes, aucune
    orpheline dans un seul sens)."""
    r, abox = _run_ok(sandbox)
    direct = {(str(c), str(a)) for c, _, a in
              abox.triples((None, DKG.isComponentOf, None))}
    inverse = {(str(a), str(c)) for a, _, c in
               abox.triples((None, DKG.hasInstalledComponent, None))}
    assert direct, "aucune relation isComponentOf matérialisée"
    assert inverse, "aucune relation hasInstalledComponent matérialisée"
    # paires inverses : (c→a) existe ⟺ (a→c) existe
    assert all((a, c) in inverse for c, a in direct), \
        "relation(s) isComponentOf sans inverse matérialisée (ABO_3)"
    assert all((c, a) in direct for a, c in inverse), \
        "relation(s) hasInstalledComponent sans inverse matérielle (ABO_3)"


# -------------------------------------------mi_1 : immuabilité & défense (D8)
def test_exg_mi1_modeles_frozen(sandbox):
    """EXG-TEC-P07-mi_1 : les modèles Pydantic V2 sont immuables (frozen)."""
    m = ScannedAssetModel(asset_id="x", name="n")
    with pytest.raises(ValidationError):
        m.asset_id = "y"                       # frozen=True : mutation interdite


def test_exg_mi1_extra_ignore(sandbox):
    """mi_1 : clés JSON inconnues ignorées (anti-crash sur scan hétérogène)."""
    m = ScannedAssetModel(asset_id="x", name="n", champ_inconnu="valeur")
    assert m.asset_id == "x"


def test_exg_mi1_scan_malforme_pas_de_crash(sandbox):
    """mi_1 : scan JSON corrompu → issue ERROR explicite, jamais d'exception
    non gérée (l'IHM reçoit un dict, pas une trace)."""
    sandbox["scan"].write_text("{ json cassé volontairement", encoding="utf-8")
    r = HostScanAboxAgent().run()
    assert r["status"] == "ERROR", r


def test_exg_mi1_scan_absent_pas_de_crash(sandbox):
    """mi_1 : scan absent → ERROR explicite (pas de crash, pas d'écriture)."""
    sandbox["scan"].unlink()
    r = HostScanAboxAgent().run()
    assert r["status"] == "ERROR"
    assert not sandbox["abox"].exists()


def test_exg_mi1_scan_bourre_extra_champs(sandbox):
    """mi_1 : scan réel avec champs supplémentaires (fatigue d'outils) →
    validation OK sur les seuls champs du contrat, extra ignoré."""
    scan = {"household_assets": [dict(SCAN["household_assets"][0],
                                       scanner="local_host_scanner v3")],
            "software_components": SCAN["software_components"],
            "horodatage": "2026-11-23T16:00:00Z"}
    sandbox["scan"].write_text(json.dumps(scan), encoding="utf-8")
    r, abox = _run_ok(sandbox)
    assert r["assets"] == 1 and r["components"] == 2


# -------------------------------------------GOU_11 : marquage TLP du graphe
def test_exg_gou11_marquage_tlp_present(sandbox):
    """EXG-FWK-P1-GOU_11 : le graphe généré porte son marquage TLP (RED)."""
    r, abox = _run_ok(sandbox)
    marquages = list(abox.subjects(RDF.type, DKG.TLPMarking))
    assert marquages, "aucun dkg:TLPMarking dans l'ABox du scan"
    asset = URIRef(str(DKG_DATA["Asset-Host-Scan"]))
    assert (asset, DKG.hasTLPMarking, None) in abox, \
        "l'actif du scan n'est pas rattaché à son marquage TLP"

# CI : enregistre le fichier dans la baseline NonReg (P9)
import pytest
pytestmark = pytest.mark.non_regression
