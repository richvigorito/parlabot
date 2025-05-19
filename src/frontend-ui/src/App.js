import React, { useState } from 'react';
import MicRecorder from 'mic-recorder-to-mp3';

const recorder = new MicRecorder({ bitRate: 128 });

function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const startRecording = () => {
    recorder.start().then(() => {
      setIsRecording(true);
    }).catch(console.error);
  };

  const stopRecording = () => {
    recorder.stop().getMp3().then(([buffer, blob]) => {
      setIsRecording(false);
      sendAudio(blob);
    }).catch(console.error);
  };

  const sendAudio = async (blob) => {
    setLoading(true);
    const formData = new FormData();
    formData.append("file", new File([blob], "recording.wav", { type: "audio/wav" }));

    try {
      const res = await fetch("http://localhost:8000/api/transcribe", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResponse(data);
    } catch (err) {
      console.error(err);
      alert("Failed to send audio.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>ParlaBot: Speak Italian ☕</h1>

      {!isRecording ? (
        <button onClick={startRecording}>Start Recording</button>
      ) : (
        <button onClick={stopRecording}>Stop & Analyze</button>
      )}

      {loading && <p>Processing...</p>}

      {response && (
        <div style={{ marginTop: '2rem' }}>
          <p><strong>Expected:</strong> {response.target}</p>
          <p><strong>You said:</strong> {response.you_said}</p>
          <p><strong>Feedback:</strong> {JSON.stringify(response.feedback)}</p>
        </div>
      )}
    </div>
  );
}

export default App;
