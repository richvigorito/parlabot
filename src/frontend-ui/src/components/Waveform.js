import React, { useEffect, useRef, useState } from 'react';
import WaveSurfer from 'wavesurfer.js';

function Waveform({ audioUrl }) {
  const waveformRef = useRef(null);
  const wavesurferRef = useRef(null);
  const isDestroyedRef = useRef(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!waveformRef.current || !audioUrl) return;

    // Reset destroyed flag
    isDestroyedRef.current = false;

    // Safely destroy previous instance
    if (wavesurferRef.current) {
      try {
        if (typeof wavesurferRef.current.destroy === 'function') {
          wavesurferRef.current.destroy();
        }
      } catch (error) {
        // Ignore destruction errors
      }
      wavesurferRef.current = null;
    }

    // Create WaveSurfer instance with error handling
    try {
      const wavesurfer = WaveSurfer.create({
        container: waveformRef.current,
        waveColor: '#ddd',
        progressColor: '#4a90e2',
        height: 80,
        responsive: true,
        normalize: true,
        backend: 'WebAudio',
      });

      // Add event listeners with checks
      const onReady = () => {
        if (!isDestroyedRef.current) setIsLoading(false);
      };
      const onFinish = () => {
        if (!isDestroyedRef.current) setIsPlaying(false);
      };
      const onPlay = () => {
        if (!isDestroyedRef.current) setIsPlaying(true);
      };
      const onPause = () => {
        if (!isDestroyedRef.current) setIsPlaying(false);
      };
      const onError = (error) => {
        console.warn('WaveSurfer error:', error);
        if (!isDestroyedRef.current) setIsLoading(false);
      };

      wavesurfer.on('ready', onReady);
      wavesurfer.on('finish', onFinish);
      wavesurfer.on('play', onPlay);
      wavesurfer.on('pause', onPause);
      wavesurfer.on('error', onError);

      // Load the audio
      wavesurfer.load(audioUrl);
      wavesurferRef.current = wavesurfer;

    } catch (error) {
      console.warn('Failed to create WaveSurfer:', error);
      if (!isDestroyedRef.current) setIsLoading(false);
    }

    // Cleanup function
    return () => {
      isDestroyedRef.current = true;
      
      if (wavesurferRef.current) {
        try {
          // Check if the instance still exists and has methods
          if (typeof wavesurferRef.current.destroy === 'function' && 
              !wavesurferRef.current.isDestroyed) {
            wavesurferRef.current.destroy();
          }
        } catch (error) {
          // Silently ignore cleanup errors - this is expected in Strict Mode
        }
        wavesurferRef.current = null;
      }
      setIsPlaying(false);
      setIsLoading(true);
    };
  }, [audioUrl]);

  const togglePlayback = () => {
    if (wavesurferRef.current && !isLoading && !isDestroyedRef.current) {
      try {
        if (typeof wavesurferRef.current.playPause === 'function') {
          wavesurferRef.current.playPause();
        }
      } catch (error) {
        console.warn('Playback error:', error);
        if (!isDestroyedRef.current) setIsPlaying(false);
      }
    }
  };

  if (!audioUrl) {
    return <div className="waveform-placeholder">No audio available</div>;
  }

  return (
    <div className="waveform-container">
      <div ref={waveformRef} style={{ minHeight: '80px' }} />
      <button 
        onClick={togglePlayback} 
        disabled={isLoading}
        className="waveform-play-button"
      >
        {isLoading ? 'Loading...' : (isPlaying ? 'Pause' : 'Play')}
      </button>
    </div>
  );
}

export default Waveform;
