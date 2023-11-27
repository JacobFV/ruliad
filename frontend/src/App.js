import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [grammar, setGrammar] = useState('');
  const [seed, setSeed] = useState('');
  const [iterations, setIterations] = useState(5);
  const [treeImage, setTreeImage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Sending the grammar, seed, and iterations to the backend
      const response = await axios.post('http://localhost:8000/generate', { grammar, seed, iterations });
      const tree = response.data;

      // Fetching the rendered tree image
      const imageResponse = await axios.get('http://localhost:8000/render', { params: { tree }, responseType: 'blob' });
      setTreeImage(URL.createObjectURL(imageResponse.data));
    } catch (error) {
      console.error("Error generating tree:", error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Grammar:
          <textarea value={grammar} onChange={(e) => setGrammar(e.target.value)} />
        </label>
        <label>
          Seed:
          <input type="text" value={seed} onChange={(e) => setSeed(e.target.value)} />
        </label>
        <label>
          Iterations:
          <input type="number" value={iterations} onChange={(e) => setIterations(e.target.value)} />
        </label>
        <button type="submit">Generate Tree</button>
      </form>
      {treeImage && <img src={treeImage} alt="Generated Tree" />}
    </div>
  );
}

export default App;

