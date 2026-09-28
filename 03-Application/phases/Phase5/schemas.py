"""
03-Application/Phase5/schemas.py
Schémas de validation Pydantic V2 pour la Phase 5 (Reasoning & MITM Agent).
Conforme aux exigences EXG-OR-07 et EXG-MITM-01.
"""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class InterceptionPayload(BaseModel):
    """
    Payload d'entité candidate interceptée par l'agent MITM.
    """
    model_config = ConfigDict(frozen=True)

    candidate_uri: str = Field(..., min_length=10, description="URI de l'entité candidate")
    label: str = Field(..., min_length=2, description="Libellé à vectoriser (skos:prefLabel / rdfs:label)")


class AlignmentResult(BaseModel):
    """
    Résultat d'alignement produit par l'évaluation vectorielle.
    """
    model_config = ConfigDict(frozen=True)

    candidate_uri: str
    target_uri: Optional[str] = None
    similarity_score: float = Field(..., ge=0.0, le=1.0)
    is_matched: bool = False
