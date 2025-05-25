import React, { useEffect, useRef, useState } from 'react';
import WaveSurfer from 'wavesurfer.js';

function Waveform({ audioUrl }) {
  const waveformRef = useRef(null);
  const wavesurferRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    if (!waveformRef.current) return;

    // Create WaveSurfer instance
    const wavesurfer = WaveSurfer.create({
      container: waveformRef.current,
      waveColor: '#ddd',
      progressColor: '#4a90e2',
      height: 80,
      responsive: true,
    });

    wavesurfer.load(audioUrl);
    wavesurfer.on('finish', () => setIsPlaying(false));
    wavesurferRef.current = wavesurfer;

    return () => {
      wavesurfer.destroy();
    };
  }, [audioUrl]);

  const togglePlayback = () => {
    if (wavesurferRef.current) {
      wavesurferRef.current.playPause();
      setIsPlaying(wavesurferRef.current.isPlaying());
    }
  };

  return (
    <div>
      <div ref={waveformRef} />
      <button onClick={togglePlayback}>
        {isPlaying ? 'Pause' : 'Play'}
      </button>
    </div>
  );
}

export default Waveform;

