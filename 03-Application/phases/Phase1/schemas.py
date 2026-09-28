"""
03-Application/Phase1/schemas.py
"""

from pydantic import BaseModel, Field
from rdflib import URIRef


class OWLClassSchema(BaseModel):
    name: str = Field(..., pattern=r"^[A-Z][a-zA-Z0-9]+$")
    pref_label_fr: str = Field(..., min_length=2)
    pref_label_en: str = Field(..., min_length=2)
    alt_label_fr: str = Field(..., min_length=2)
    definition_fr: str = Field(..., min_length=10)


class OWLObjectPropertySchema(BaseModel):
    name: str = Field(..., pattern=r"^[a-z][a-zA-Z0-9]+$")
    domain: str
    range_cls: str
    inverse_name: str | None = None
    pref_label_fr: str = Field(..., min_length=2)
    pref_label_en: str = Field(..., min_length=2)
    comment_fr: str = Field(..., min_length=5)


class OWLDatatypePropertySchema(BaseModel):
    name: str = Field(..., pattern=r"^[a-z][a-zA-Z0-9]+$")
    domain: str
    datatype: URIRef
    pref_label_fr: str = Field(..., min_length=2)
    pref_label_en: str = Field(..., min_length=2)

    class Config:
        arbitrary_types_allowed = True


class SHACLCvssConstraintSchema(BaseModel):
    target_class: str = "Vulnerability"
    path_property: str = "cvssScore"
    datatype: URIRef
    max_inclusive: float = Field(default=10.0, ge=0.0, le=10.0)
    min_inclusive: float = Field(default=0.0, ge=0.0, le=10.0)

    class Config:
        arbitrary_types_allowed = True
