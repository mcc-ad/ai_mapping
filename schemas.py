from typing import List, Optional
from pydantic import BaseModel

# This will be our schema for reading ontology mappings from the database
class OntologyMappingBase(BaseModel):
    source_term: str
    target_term: str
    mapping_relation: str
    confidence_score: str

# Schema for ontology mapping creation requests
class OntologyMappingCreate(OntologyMappingBase):
    pass

# Schema for ontology mapping update requests
class OntologyMappingUpdate(OntologyMappingBase):
    pass

# Schema for responses, includes ID
class OntologyMapping(OntologyMappingBase):
    id: int

    class Config:
        orm_mode = True

