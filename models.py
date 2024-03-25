from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base class for all your models
Base = declarative_base()

# Define the OntologyMapping model
class OntologyMapping(Base):
    __tablename__ = 'ontology_mappings'
    
    id = Column(Integer, primary_key=True, index=True)
    source_term = Column(String, index=True)
    target_term = Column(String, index=True)
    mapping_relation = Column(String)
    confidence_score = Column(String)

# Database connection URL
DATABASE_URL = "sqlite:///./test.db"

# Create the engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
