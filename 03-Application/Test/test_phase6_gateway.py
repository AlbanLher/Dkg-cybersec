"""
03-Application/Test/test_phase6_gateway.py
Suite de tests PyTest - Phase 6 : API Gateway, Immutabilité & Isolation TLP.
"""

import sys
from pathlib import Path
import pytest
from rdflib import Graph, RDF, URIRef

# Ancrage SSOT dans sys.path
APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from Phase6.p6_schemas import SPARQLQueryRequest, TLPLevel
from Phase6.api_gateway import APIGateway


@pytest.fixture
def mock_rdf_environment(tmp_path: Path, monkeypatch):
    """Fixture créant des graphes RDF étanches temporaires pour valider l'isolation TLP."""
    clear_ttl = tmp_path / "cti_clear.ttl"
    red_ttl = tmp_path / "abox_red.ttl"

    g_clear = Graph()
    g_clear.add((
        URIRef("http://dkg.cybersec.org/cti#CVE-2024-0001"),
        RDF.type,
        URIRef("http://dkg.cybersec.org/cti#Vulnerability")
    ))
    g_clear.serialize(destination=clear_ttl.as_posix(), format="turtle")

    g_red = Graph()
    g_red.add((
        URIRef("http://dkg.cybersec.org/data#Server_01"),
        RDF.type,
        URIRef("http://dkg.cybersec.org/tbox#Asset")
    ))
    g_red.serialize(destination=red_ttl.as_posix(), format="turtle")

    monkeypatch.setattr("config.TLP_CLEAR_READ_GRAPH", [clear_ttl])
    monkeypatch.setattr("config.TLP_AMBER_READ_GRAPH", [clear_ttl])
    monkeypatch.setattr("config.TLP_RED_READ_GRAPH", [clear_ttl, red_ttl])

    return tmp_path


def test_pydantic_immutability():
    """Vérifie l'immutabilité des payloads Pydantic V2 (frozen=True)."""
    req = SPARQLQueryRequest(
        client_id="test-client",
        tlp_token=TLPLevel.CLEAR,
        query="SELECT * WHERE { ?s ?p ?o }"
    )
    with pytest.raises(Exception):
        req.client_id = "modified-client"


def test_tlp_isolation_clear(mock_rdf_environment):
    """Vérifie qu'un jeton TLP:CLEAR ne voit PAS les données TLP:RED (0 fuite)."""
    gateway = APIGateway(audit_log_path=mock_rdf_environment / "audit.log")
    
    query_red = "PREFIX dkg-data: <http://dkg.cybersec.org/data#> SELECT ?s WHERE { ?s a <http://dkg.cybersec.org/tbox#Asset> }"
    req = SPARQLQueryRequest(
        client_id="user-clear",
        tlp_token=TLPLevel.CLEAR,
        query=query_red
    )
    
    res = gateway.execute_sparql(req)
    assert res.success is True
    assert res.results_count == 0


def test_tlp_access_red(mock_rdf_environment):
    """Vérifie qu'un jeton TLP:RED accède aux données internes RED."""
    gateway = APIGateway(audit_log_path=mock_rdf_environment / "audit.log")
    
    query_red = "PREFIX dkg-data: <http://dkg.cybersec.org/data#> SELECT ?s WHERE { ?s a <http://dkg.cybersec.org/tbox#Asset> }"
    req = SPARQLQueryRequest(
        client_id="user-red",
        tlp_token=TLPLevel.RED,
        query=query_red
    )
    
    res = gateway.execute_sparql(req)
    assert res.success is True
    # Validation dynamique : au moins une instance retournée
    assert res.results_count > 0


