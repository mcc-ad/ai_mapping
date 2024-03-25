from sqlalchemy.orm import Session
# from . import models
import models
import schemas

# Dependency to get DB session
def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_ontology_mapping_by_id(db: Session, mapping_id: int):
    return db.query(models.OntologyMapping).filter(models.OntologyMapping.id == mapping_id).first()

def get_ontology_mappings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.OntologyMapping).offset(skip).limit(limit).all()

def create_ontology_mapping(db: Session, ontology_mapping: schemas.OntologyMappingCreate):
    db_ontology_mapping = models.OntologyMapping(**ontology_mapping.dict())
    db.add(db_ontology_mapping)
    db.commit()
    db.refresh(db_ontology_mapping)
    return db_ontology_mapping

def update_ontology_mapping(db: Session, mapping_id: int, ontology_mapping: schemas.OntologyMappingUpdate):
    db_ontology_mapping = get_ontology_mapping_by_id(db, mapping_id)
    if db_ontology_mapping:
        update_data = ontology_mapping.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_ontology_mapping, key, value)
        db.commit()
        db.refresh(db_ontology_mapping)
    return db_ontology_mapping

def delete_ontology_mapping(db: Session, mapping_id: int):
    db_ontology_mapping = get_ontology_mapping_by_id(db, mapping_id)
    if db_ontology_mapping:
        db.delete(db_ontology_mapping)
        db.commit()
        return True
    return False
