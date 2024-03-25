from sqlalchemy.orm import Session
import models, schemas

def create_ontology_mapping(db: Session, ontology_mapping: schemas.OntologyMappingCreate):
    db_mapping = models.OntologyMapping(**ontology_mapping.dict())
    db.add(db_mapping)
    db.commit()
    db.refresh(db_mapping)
    return db_mapping

def get_ontology_mappings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.OntologyMapping).offset(skip).limit(limit).all()

def get_ontology_mapping(db: Session, mapping_id: int):
    return db.query(models.OntologyMapping).filter(models.OntologyMapping.id == mapping_id).first()