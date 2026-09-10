"""
03-Application/Phase3/schemas.py
Modèles de validation Pydantic V2 pour l'ingestion CTI (Phase 3).
"""

from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class CisaKevEntry(BaseModel):
    """Validation d'une entrée CISA KEV."""
    model_config = ConfigDict(extra="ignore")

    cve_id: str = Field(..., pattern=r"^CVE-\d{4}-\d{4,}$")
    vulnerability_name: str
    is_cisa_kev: bool = True
    short_description: Optional[str] = None


class CtiFeedEntry(BaseModel):
    """Validation d'un item complet du flux JSON CTI d'entrée."""
    model_config = ConfigDict(extra="ignore")

    description: str
    cvss_score: float = Field(..., ge=0.0, le=10.0)
    is_cisa_kev: bool = False
    cwe_id: Optional[str] = Field(None, pattern=r"^CWE-\d+$")
    capec_id: Optional[str] = Field(None, pattern=r"^CAPEC-\d+$")
    capec_title: Optional[str] = None
    capec_description: Optional[str] = None
