"""
03-Application/Phase6/api_gateway.py
Moteur de Ségrégation TLP et API Gateway SPARQL.
"""

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any
from rdflib import Graph

from config import (
    TLP_CLEAR_READ_GRAPH,
    TLP_AMBER_READ_GRAPH,
    TLP_RED_READ_GRAPH,
    PATH_P6_GATEWAY_LOG,
    DKG_TBOX,
    DKG_DATA,
    DKG_CTI
)
from Phase6.p6_schemas import SPARQLQueryRequest, SPARQLQueryResponse, TLPLevel

class SecurityEngine:
    """Moteur d'isolation dynamique des calques du DKG selon le niveau TLP."""

    @staticmethod
    def resolve_graph_sources(tlp_level: TLPLevel) -> List[Path]:
        """Retourne la liste des artefacts RDF autorisés pour le niveau TLP donné."""
        if tlp_level == TLPLevel.CLEAR:
            return TLP_CLEAR_READ_GRAPH
        elif tlp_level == TLPLevel.AMBER:
            return TLP_AMBER_READ_GRAPH
        elif tlp_level == TLPLevel.RED:
            return TLP_RED_READ_GRAPH
        else:
            raise ValueError(f"Niveau TLP inconnu : {tlp_level}")

    def build_isolated_graph(self, tlp_level: TLPLevel) -> Graph:
        """Construit en mémoire le graphe unifié restreint au périmètre TLP autorisé."""
        sources = self.resolve_graph_sources(tlp_level)
        isolated_graph = Graph()
        isolated_graph.bind("dkg", DKG_TBOX)
        isolated_graph.bind("dkg-data", DKG_DATA)
        isolated_graph.bind("dkg-cti", DKG_CTI)

        for source_path in sources:
            if source_path.exists():
                isolated_graph.parse(source_path.as_posix(), format="turtle")
            else:
                logging.warning(f"Artefact RDF introuvable ignoré : {source_path}")

        return isolated_graph


class APIGateway:
    """Gateway d'exécution SPARQL sécurisée avec journalisation d'audit."""

    def __init__(self, audit_log_path: Path = PATH_P6_GATEWAY_LOG):
        self.security_engine = SecurityEngine()
        self.audit_log_path = audit_log_path
        self._ensure_log_dir()

    def _ensure_log_dir(self) -> None:
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)

    def _audit_log(self, client_id: str, tlp: TLPLevel, count: int, status: str, msg: str = "") -> None:
        """Enregistre la trace d'exécution dans le journal d'audit."""
        timestamp = datetime.now(timezone.utc).isoformat()
        log_line = f"[{timestamp}] CLIENT={client_id} | TLP={tlp.value} | STATUS={status} | RESULTS={count} | INFO={msg}\n"
        with open(self.audit_log_path, "a", encoding="utf-8") as f:
            f.write(log_line)

    def execute_sparql(self, request: SPARQLQueryRequest) -> SPARQLQueryResponse:
        """Valide, isole et exécute la requête SPARQL du client."""
        try:
            isolated_graph = self.security_engine.build_isolated_graph(request.tlp_token)
            qres = isolated_graph.query(request.query)

            bindings: List[Dict[str, Any]] = []
            if qres.type == "SELECT":
                for row in qres:
                    row_dict = {}
                    for var in qres.vars:
                        val = row[var]
                        row_dict[str(var)] = str(val) if val is not None else None
                    bindings.append(row_dict)

            results_count = len(bindings)
            self._audit_log(request.client_id, request.tlp_token, results_count, "SUCCESS")

            return SPARQLQueryResponse(
                success=True,
                client_id=request.client_id,
                tlp_applied=request.tlp_token,
                results_count=results_count,
                bindings=bindings,
                error_message=None
            )

        except Exception as e:
            err_msg = str(e)
            self._audit_log(request.client_id, request.tlp_token, 0, "ERROR", err_msg)
            return SPARQLQueryResponse(
                success=False,
                client_id=request.client_id,
                tlp_applied=request.tlp_token,
                results_count=0,
                bindings=[],
                error_message=err_msg
            )
