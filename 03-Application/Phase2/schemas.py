"""
03-Application/Phase2/schemas.py
Modèles de validation Pydantic V2 aux frontières (EXG-OR-07).
Garantit l'intégrité et le typage strict des données entrantes de la Phase 2.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ThreatPatternInputModel(BaseModel):
    id: str = Field(..., pattern=r"^CAPEC-\d+$", description="Identifiant CAPEC normé")
    label: str
    description: str


class WeaknessInputModel(BaseModel):
    id: str = Field(..., pattern=r"^CWE-\d+$", description="Identifiant CWE normé")
    label: str
    threat_pattern_id: Optional[str] = Field(None, pattern=r"^CAPEC-\d+$")


class VulnerabilityInputModel(BaseModel):
    id: str = Field(..., pattern=r"^CVE-\d{4}-\d+$", description="Identifiant CVE normé")
    label: str
    cvss_score: float = Field(..., ge=0.0, le=10.0, description="Score CVSS de 0.0 à 10.0")
    weakness_id: Optional[str] = Field(None, pattern=r"^CWE-\d+$")


class SoftwareComponentInputModel(BaseModel):
    id: str
    label: str
    vulnerability_id: Optional[str] = Field(None, pattern=r"^CVE-\d{4}-\d+$")


class AssetInputModel(BaseModel):
    id: str
    label: str
    tlp_marking: Optional[str] = Field(None, pattern=r"^TLP-(CLEAR|AMBER|RED)$")
    installed_component_id: Optional[str] = None


class Phase2InventoryModel(BaseModel):
    tlp_markings: List[str] = Field(default_factory=list)
    threat_patterns: List[ThreatPatternInputModel] = Field(default_factory=list)
    weaknesses: List[WeaknessInputModel] = Field(default_factory=list)
    vulnerabilities: List[VulnerabilityInputModel] = Field(default_factory=list)
    software_components: List[SoftwareComponentInputModel] = Field(default_factory=list)
    assets: List[AssetInputModel] = Field(default_factory=list)


class SHACLValidationReport(BaseModel):
    conforms: bool
    violation_count: int = Field(..., ge=0)
    results_text: str
    severity_levels: List[str] = Field(default_factory=list)

    @property
    def has_fatal_violations(self) -> bool:
        return "Violation" in self.severity_levels
