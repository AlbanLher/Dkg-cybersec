"""
03-Application/Phase6/p6_schemas.py
Modèles Pydantic V2 (Immutable) pour l'API Gateway SPARQL/GraphQL & Ségrégation TLP.
"""

from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, ConfigDict


class TLPLevel(str, Enum):
    CLEAR = "CLEAR"
    AMBER = "AMBER"
    RED = "RED"


class SPARQLQueryRequest(BaseModel):
    """Payload de requête entrante sur l'API Gateway."""
    model_config = ConfigDict(frozen=True)

    client_id: str = Field(..., min_length=3, description="Identifiant unique du client/agent")
    tlp_token: TLPLevel = Field(..., description="Niveau TLP d'habilitation de l'appelant")
    query: str = Field(..., min_length=10, description="Requête SPARQL à exécuter")


class SPARQLQueryResponse(BaseModel):
    """Payload de réponse standardisé de l'API Gateway."""
    model_config = ConfigDict(frozen=True)

    success: bool = Field(..., description="Statut de l'exécution")
    client_id: str = Field(..., description="Identifiant du client demandeur")
    tlp_applied: TLPLevel = Field(..., description="Niveau TLP appliqué à l'isolation")
    results_count: int = Field(..., ge=0, description="Nombre de n-uplets retournés")
    bindings: List[Dict[str, Any]] = Field(default_factory=list, description="Résultats SPARQL formatés")
    error_message: Optional[str] = Field(default=None, description="Message d'erreur éventuel")
