import React from 'react';
import './App.css';
import { Switch, Route } from 'react-router-dom';
import OntologyMapper from './components/OntologyMapper';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>EHR Ontology Mapper</h1>
      </header>
      <main>
        <Switch>
          <Route exact path="/">
            <OntologyMapper />
          </Route>
          {/* You can add more routes here as your project expands */}
        </Switch>
      </main>
    </div>
  );
}

export default App;
