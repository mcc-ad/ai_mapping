from typing import List  # Add this import
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
from models import Base, engine
from database import get_db
from schemas import OntologyMappingCreate, OntologyMapping
import crud
# import bionty_base as bt
# import lamindb as ln
import bionty_base as bt

# Create the FastAPI app
app = FastAPI()

# artifacts are stored in a local directory `./lamin-intro`
# ln.setup.init(schema="bionty", storage="./lamin-intro")

# Create database tables
Base.metadata.create_all(bind=engine)

# CORS middleware configuration
origins = [
    "http://localhost:3000",  # Assuming React frontend runs on localhost:3000
    "http://localhost:8000",  # FastAPI default port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["X-Requested-With", "Content-Type"],
)

@app.post("/ontology-mappings/", response_model=OntologyMapping)
def create_ontology_mapping(ontology_mapping: OntologyMappingCreate, db: Session = Depends(get_db)):
    """
    Create a new ontology mapping.
    """
    return crud.create_ontology_mapping(db=db, ontology_mapping=ontology_mapping)

@app.get("/ontology-mappings/", response_model=List[OntologyMapping])
def read_ontology_mappings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve ontology mappings.
    """
    mappings = crud.get_ontology_mappings(db, skip=skip, limit=limit)
    return mappings

@app.get("/ontology-mappings/{mapping_id}", response_model=OntologyMapping)
def read_ontology_mapping(mapping_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific ontology mapping by ID.
    """
    db_mapping = crud.get_ontology_mapping(db, mapping_id=mapping_id)
    if db_mapping is None:
        raise HTTPException(status_code=404, detail="Ontology mapping not found")
    return db_mapping


# 📖 .df(): ontology reference table
# 🔎 .lookup(): autocompletion of terms
# 🎯 .search(): free text search of terms
# ✅ .validate(): strictly validate values
# 🧐 .inspect(): full inspection of values
# 👽 .standardize(): convert to standardized names
# 🪜 .diff(): difference between two versions
# 🔗 .to_pronto(): Pronto.Ontology object

import logging
@app.get("/bionty-mapping/{input_string}")
def bionty_mapping(input_string: str):
    logging.basicConfig(level=logging.DEBUG)
    # Initialize BT with MONDO ontology
    disease_bt = bt.Disease(source="mondo", version="2023-08-02")
    logging.debug("Initialized BT with ontology, latest version")
    
    # Normalize input string for matching
    normalized_input = ''
    parts = input_string.split('_', 1)  # Splitting the input string into two parts
    if len(parts) == 2:
        _, normalized_input = parts  # Using the second part as the normalized input
    else:
        normalized_input = input_string  # If no '_' present, use the original input string
   
    # logging.debug(f"Normalized input string for matching: {normalized_input}")
    
    # # Attempt to find a direct match for the input string
    # direct_match = disease_bt.find_disease_by_name(normalized_input)
    # if direct_match:
    #     logging.debug(f"Found direct match: {direct_match['name']}")
    #     return {"match": direct_match['name'], "definition": direct_match['description']}
    # else:
    #     logging.debug("No direct match found, attempting advanced search")
    search_results = disease_bt.search(normalized_input).head(3)
    print(search_results)
    if not search_results.empty:
        top_result = search_results.iloc[0]  # Taking the top result from the dataframe
        print(f"Top result: {top_result.name}")
        return {"match": top_result.name, "definition": top_result['definition'], "ontology_id": top_result['ontology_id']}
    else:
        print("No results found")
        return {"match": None, "ontology_id": None}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
