import { useState } from 'react';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [resultUrl, setResultUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResultUrl(null); // Reset result when new image is picked
    }
  };

  
  const handleUpload = async () => {
    if (!selectedFile) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('https://pothole-detector-qrnb.onrender.com/', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const blob = await response.blob();
        setResultUrl(URL.createObjectURL(blob));
      } else {
        alert("Server Error. Is the backend running?");
      }
    } catch (error) {
      console.error(error);
      alert("Failed to connect to server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Header Section */}
      <header>
        <h1 className="hero-title">RoadGuard AI</h1>
        <p className="hero-subtitle">
          Advanced Autonomous Pothole Detection System. Upload road imagery to analyze infrastructure hazards in real-time.
        </p>
      </header>

      {/* Upload Section */}
      <div className="upload-card">
        <label htmlFor="file-upload" className="upload-label">
          <span className="upload-icon">📁</span>
          {selectedFile ? selectedFile.name : "Click to Upload Road Image"}
        </label>
        <input 
          id="file-upload" 
          type="file" 
          accept="image/*" 
          onChange={handleFileChange} 
          className="file-input"
        />
      </div>

      {/* Action Button */}
      {selectedFile && (
        <div style={{ marginBottom: '40px' }}>
          <button 
            className="primary-btn" 
            onClick={handleUpload} 
            disabled={loading}
          >
            {loading ? <div className="loader"></div> : "Analyze Image"}
          </button>
        </div>
      )}

      {/* Results Section */}
      <div className="results-section">
        {previewUrl && (
          <div className="image-card">
            <h3>Original Feed</h3>
            <img src={previewUrl} alt="Original" className="display-image" />
          </div>
        )}

        {resultUrl && (
          <div className="image-card" style={{ border: '1px solid var(--accent)' }}>
            <h3 style={{ color: 'var(--accent)' }}>AI Detection</h3>
            <img src={resultUrl} alt="Result" className="display-image" />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;