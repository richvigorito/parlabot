import React from 'react';
import Waveform from './Waveform'; // The waveform component using wavesurfer.js

function AudioBlock({ block }) {
    
    console.log("block: ",block)
  return (
    <div className="audio-block-container">
        <h3 style={{ marginBottom: '0.5rem' }}>Audio Block: {block.id}</h3>

        <div className="audio-section">
          <strong>Input File:</strong>
          <Waveform audioUrl={`http://localhost:8000${block.input_file}`} />
        </div>

        <div className="audio-section">
          <strong>Filters:</strong>
          {block.transformations.map((filter, i) => (
            <div key={i} className="filter-block">
              <div>{filter.filter_name}</div>
                <Waveform audioUrl={`http://localhost:8000${filter.output_file}`} />
            </div>
          ))}
        </div>

        <div className="audio-section">
          <strong>Output File:</strong>
          <Waveform audioUrl={`http://localhost:8000${block.output_file}`} />
        </div>

        <div className="audio-section">
          <strong>Transcription:</strong> {block.transcription}
        </div>

        <div className="audio-section">
          <strong>Pronunciation Score:</strong> {block.pronunciation_score}
        </div>
    </div>
  );
}

export default AudioBlock;

