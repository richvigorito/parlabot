import React, { useState } from 'react';
import Waveform from './Waveform'; // The waveform component using wavesurfer.js
import { API_ORCHESTRATOR_URL } from '../config';

function AudioBlock({ block }) {
  const [isVisible, setIsVisible] = useState(false);

  const toggleVisibility = () => setIsVisible(prev => !prev);

  const makeUrl = (path) => new URL(path, API_ORCHESTRATOR_URL).toString();


  return (
    <div className="audio-block-container">
      <div className="audio-block-header">
        <h3 style={{ marginBottom: '0.5rem' }}>
          Pipeline: {block.pipeline}
        </h3>
        <div className="audio-section">
          <strong>Transcription:</strong> {block.transcription}
        </div>
        <div className="audio-section">
          <strong>Pronunciation Score:</strong> {block.pronunciation_score}
        </div>

        <button onClick={toggleVisibility} className="toggle-button">
          {isVisible ? 'Hide' : 'Show'}
        </button>
      </div>

      {isVisible && (
        <div className="audio-block-body">
          
          <div className="audio-section">
            <strong>Input File:</strong>
            <Waveform audioUrl={makeUrl(block.input_file)} />
          </div>
          <div className="audio-section">
            <strong>Filters:</strong>
            {block.transformations.map((filter, i) => (
              <div key={i} className="filter-block">
                <div>{filter.filter_name}</div>
                <Waveform audioUrl={makeUrl(filter.output_file)} />
              </div>
            ))}
          </div>
          <div className="audio-section">
            <strong>Output File:</strong>
            <Waveform audioUrl={makeUrl(block.output_file)} />
          </div>
        </div>
      )}
    </div>
  );
}

export default AudioBlock;

