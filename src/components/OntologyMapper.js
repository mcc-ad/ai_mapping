import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './OntologyMapper.css'; // Assuming you have a CSS file for styling

function OntologyMapper() {
  const [inputString, setInputString] = useState('');
  const [selectedOntology, setSelectedOntology] = useState('');
  const [ontologyOptions, setOntologyOptions] = useState([]);
  const [mappingResult, setMappingResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    // Assuming the ontology options are fetched from an API or defined statically
    const fetchOntologyOptions = async () => {
      // Example static data, replace with API call if needed
      const options = [
        { label: 'Disease - DOID', value: 'DOID' },
        { label: 'Disease - Mondo', value: 'Mondo' },
        { label: 'Gene - Ensembl', value: 'Ensembl' },
        { label: 'Protein - UniProt', value: 'UniProt' },
        { label: 'Cell Marker - CellMarker', value: 'CellMarker' },
        { label: 'Developmental Stage - HSAPDV', value: 'HSAPDV' },
        { label: 'Ethnicity - HANCESTRO', value: 'HANCESTRO' },
        { label: 'Phenotype - HP', value: 'HP' },
      ];
      setOntologyOptions(options);
    };

    fetchOntologyOptions();
  }, []);

  const handleInputChange = (e) => {
    setInputString(e.target.value);
  };

  const handleOntologyChange = (e) => {
    setSelectedOntology(e.target.value);
  };

  const fetchMappedOntology = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.get(`/bionty-mapping/${selectedOntology}_${inputString}`);
      setMappingResult(response.data);
    } catch (error) {
      setError('Failed to fetch mapped ontology');
      setMappingResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ontology-mapper">
      <h2 className="title">Ontology Mapping</h2>
      <div className="input-group">
        <select
          className="ontology-select"
          value={selectedOntology}
          onChange={handleOntologyChange}
        >
          <option value="">Select Ontology</option>
          {ontologyOptions.map((option) => (
            <option key={option.value} value={option.value}>{option.label}</option>
          ))}
        </select>
        <input
          className="input-field"
          type="text"
          value={inputString}
          onChange={handleInputChange}
          placeholder="Enter term to map"
        />
        <button className="map-button" onClick={fetchMappedOntology}>Map Ontology</button>
      </div>
      {loading && <div className="loading">Loading...</div>}
      {error && <div className="error">Error: {error}</div>}
      {mappingResult && (
        <div className="result">
          <h3>Mapping Result</h3>
          {mappingResult.match ? (
            <div className="match-result">
              <p><strong>Match:</strong> {mappingResult.match}</p>
              <p><strong>Definition:</strong> {mappingResult.definition}</p>
              <p><strong>Ontology ID:</strong> {mappingResult.ontology_id}</p>
            </div>
          ) : (
            <p className="no-match">No match found.</p>
          )}
        </div>
      )}
    </div>
  );
}

export default OntologyMapper;