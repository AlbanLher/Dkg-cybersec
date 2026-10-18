# 03-Application/Test/test_confrontation.py
# =============================================================================
# Recette CONFRONTATION_1 (P9 anticipé) — R1..R5 du DIFF_integration_applicative.
# Traçabilité : EXG-CONF_1, RES_1 (seeds jamais modifiés), AGE_1 (Local-First
# SPARQL), GOU_22 (affects* déclarées en TBox).
# Fixtures EN MÉMOIRE (jamais le workspace réel ni les seeds) — même esprit
# que test_phase8_demonstrateur.py (workset tmp).
# =============================================================================
"""
Tracabilite : EXG-MET-P8-RES_1 (test_res1), EXG-MET-P8-DEM_2 (R6, filtre de provenance),
              + EXG-CONF_1 (R1–R5, non déclaré — dette P9)
"""
from pathlib import Path

import pytest
from rdflib import Graph

from core import confrontation

# --- Fixtures TTL (standard P9 : inventaire pur + fonds CLEAR) ---------------
INVENTORY_TTL = """
@prefix dkg: <http://dkg.cybersec.org/tbox#> .
@prefix dkg-data: <http://dkg.cybersec.org/data#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

dkg-data:TLP-RED a dkg:TLPMarking ; rdfs:label "TLP:RED"@en .

dkg-data:Asset-Srv a dkg:Asset ;
    rdfs:label "Serveur Authentification Central"@fr ;
    dkg:hasInstalledComponent dkg-data:Comp-Log4j ;
    dkg:hasTLPMarking dkg-data:TLP-RED .

dkg-data:Comp-Log4j a dkg:SoftwareComponent ;
    dkg:componentId "comp-apache-log4j-core" ;
    dkg:version "2.14.1" ;
    rdfs:label "Apache Log4j Core"@fr ;
    dkg:isComponentOf dkg-data:Asset-Srv .
"""

FUNDS_TTL = """
@prefix dkg: <http://dkg.cybersec.org/tbox#> .
@prefix dkg-cti: <http://dkg.cybersec.org/cti#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

dkg-cti:CVE-2021-44228 a dkg:Vulnerability ;
    dkg:cveId "CVE-2021-44228" ;
    rdfs:label "Log4Shell Remote Code Execution"@en ;
    dkg:cvssScore "10.0"^^xsd:float ;
    dkg:affectsComponentId "comp-apache-log4j-core" ;
    dkg:affectsVersion "2.14.1" ;
    dkg:providedBy "cisa_kev_2025" , "nvd_cve_feed" .
"""


@pytest.fixture
def inventory(tmp_path: Path) -> Graph:
    g = Graph()
    g.parse(data=INVENTORY_TTL, format="turtle")
    return g


@pytest.fixture
def funds(tmp_path: Path) -> Path:
    p = tmp_path / "DKG_ABox_CTI_External.ttl"
    p.write_text(FUNDS_TTL, encoding="utf-8")
    return p


# --- R1 : inventaire pur — 0 vulnérabilité avant CTI ---------------------------
@pytest.mark.non_regression
def test_r1_inventory_pure_zero_vulnerability(inventory):
    """R1 : l'inventaire (scan/seed P9) ne contient AUCUNE Vulnerability."""
    assert confrontation.count_local_vulnerabilities(inventory) == 0


# --- R2 : CTI coché -> exactement les findings attendus, skos:exactMatch ------
@pytest.mark.non_regression
def test_r2_confrontation_produces_findings(inventory, funds):
    """R2 : CONFRONTATION_1 produit le finding local (version match exact),
    relié au fonds par skos:exactMatch ; l'ABox locale est TLP:RED."""
    res = confrontation.run_confrontation(inventory, funds_path=funds)
    assert res["findings_produced"] == 1
    assert res["local_vulnerabilities"] == 1
    item = res["findings"][0]
    assert item["cve_id"] == "CVE-2021-44228"
    assert item["cvss"] == 10.0
    assert item["severity"] == "RED"
    assert "skos:exactMatch" in inventory.serialize(format="turtle")


# --- R3 : décochage -> purge complète (retour inventaire pur) ------------------
@pytest.mark.non_regression
def test_r3_purge_restores_pure_inventory(inventory, funds):
    """R3 : purge_findings retire findings + fonds ; le graphe local
    n'est jamais pollué durablement."""
    confrontation.run_confrontation(inventory, funds_path=funds)
    assert confrontation.count_local_vulnerabilities(inventory) == 1
    removed = confrontation.purge_findings(inventory)
    assert removed > 0
    assert confrontation.count_local_vulnerabilities(inventory) == 0


# --- R4 : version non affectée -> 0 finding (la négation démontre aussi) ------
@pytest.mark.non_regression
def test_r4_unaffected_version_zero_finding(inventory, funds):
    """R4 : httpd 2.4.68 réel non affecté -> 0 finding sur ce composant."""
    inventory.parse(data="""
    @prefix dkg: <http://dkg.cybersec.org/tbox#> .
    @prefix dkg-data: <http://dkg.cybersec.org/data#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    dkg-data:Comp-Httpd a dkg:SoftwareComponent ;
        dkg:componentId "comp-apache-http-server" ;
        dkg:version "2.4.68" ;
        rdfs:label "Apache HTTP Server"@fr .
    """, format="turtle")
    res = confrontation.run_confrontation(inventory, funds_path=funds)
    # le fonds ne référence PAS 2.4.68 -> seul Log4j matche, httpd reste sain
    assert res["findings_produced"] == 1
    assert all(f["component"] != "Apache HTTP Server" for f in res["findings"])


# --- R5 : idempotence — re-exécution sans doublon ------------------------------
@pytest.mark.non_regression
def test_r5_idempotent_no_duplicate(inventory, funds):
    """R5 : rejouer CONFRONTATION_1 ne duplique pas le finding (FILTER NOT
    EXISTS + RDF set-semantics) ; le compte reste 1."""
    confrontation.run_confrontation(inventory, funds_path=funds)
    res2 = confrontation.run_confrontation(inventory, funds_path=funds)
    assert res2["findings_produced"] == 0          # déjà présent -> non re-produit
    assert confrontation.count_local_vulnerabilities(inventory) == 1


# --- RES_1 : les fichiers seed ne sont jamais modifiés -------------------------
@pytest.mark.non_regression
def test_res1_seeds_never_modified(inventory, funds):
    """RES_1 : la confrontation travaille en mémoire — le fichier fonds est
    byte-identique avant/après."""
    before = funds.read_bytes()
    confrontation.run_confrontation(inventory, funds_path=funds)
    confrontation.purge_findings(inventory)
    assert funds.read_bytes() == before


# --- R6 : filtre de provenance — la collecte dépend de la source cochée -------
@pytest.mark.non_regression
def test_r6_source_filter_selects_findings(inventory, funds):
    """R6 (EXG-MET-P8-DEM_2) : seules les CVE dont dkg:providedBy intersecte
    les sources cochées participent à CONFRONTATION_1.
    - cisa_kev_2025 cochée -> finding Log4Shell ;
    - anssi_2024 cochée (ne fournit PAS cette CVE) -> 0 finding ;
    - sources=None -> tout le fonds (comportement catalogue complet)."""
    res_kev = confrontation.run_confrontation(inventory, funds_path=funds,
                                              sources=["cisa_kev_2025"])
    assert res_kev["findings_produced"] == 1
    assert res_kev["findings"][0]["cve_id"] == "CVE-2021-44228"

    g2 = Graph()
    g2.parse(data=INVENTORY_TTL, format="turtle")
    res_none = confrontation.run_confrontation(g2, funds_path=funds,
                                               sources=["anssi_2024"])
    assert res_none["findings_produced"] == 0
    assert confrontation.count_local_vulnerabilities(g2) == 0

    g3 = Graph()
    g3.parse(data=INVENTORY_TTL, format="turtle")
    res_all = confrontation.run_confrontation(g3, funds_path=funds)   # None
    assert res_all["findings_produced"] == 1                          # tout le fonds
