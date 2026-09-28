from pydantic import BaseModel, Field

class ExtractedEntity(BaseModel):
    text: str = Field(..., min_length=1)
    label: str  # ex: "ThreatActor", "Software", "CVE"
    score: float = Field(..., ge=0.0, le=1.0)
    start_char: int = Field(..., ge=0)
    end_char: int = Field(..., ge=0)
