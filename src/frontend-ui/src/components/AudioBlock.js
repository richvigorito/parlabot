import React from 'react';
import Waveform from './Waveform'; // The waveform component using wavesurfer.js

function AudioBlock({ block }) {
    
    console.log("block: ",block)
  return (
    <div style={{ border: '1px solid #ccc', marginBottom: 20, padding: 10 }}>
      <h3>Audio Block: {block.id}</h3>
      
      <div>
        <strong>Input File:</strong>
        <audio controls src={`http://localhost:8000${block.input_file}`} /> 
        <Waveform audioUrl={`http://localhost:8000${block.input_file}`} />
      </div>

      <div>
        <strong>Filters:</strong>
        {block.transformations.map((filter, i) => (
          <div key={i} style={{ marginLeft: 20, marginTop: 10 }}>
            <div>{filter.filter_name}</div>
              <audio controls src={`http://localhost:8000${filter.output_file}`} /> 
              <Waveform audioUrl={`http://localhost:8000${filter.output_file}`} />
          </div>
        ))}
      </div>

      <div>
        <strong>Output File:</strong>
        <audio controls src={`http://localhost:8000${block.output_file}`} /> 
        <Waveform audioUrl={`http://localhost:8000${block.output_file}`} />
      </div>

      <div>
        <strong>Transcription:</strong> {block.transcription}
      </div>

      <div>
        <strong>Pronunciation Score:</strong> {block.pronunciation_score}
      </div>
    </div>
  );
}

export default AudioBlock;

