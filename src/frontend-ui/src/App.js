import React, { useState } from 'react';
import './App.css';
import MicRecorder from 'mic-recorder-to-mp3';
import AudioBlock from './components/AudioBlock';


import en from './locales/en.json';
import it from './locales/it.json';


const recorder = new MicRecorder({ bitRate: 128 });
const locales = { en, it };


function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [audioBlocks, setAudioBlocks] = useState([]);
  const [randomPhrase, setRandomPhrase] = useState(null);

  const [lang, setLang] = useState('it');
  const t = locales[lang];

  const fetchRandomPhrase = async () => {
    const res = await fetch("http://localhost:5002/phrases/random");
    const phrase = await res.json();
    setRandomPhrase(phrase);
  };

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
      console.log(data);
      setResponse(data);
      setAudioBlocks(data);
    } catch (err) {
      console.error(err);
      alert("Failed to send audio.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
        <div className="lang-switcher">
            <button
              className={lang === 'en' ? 'active' : ''}
              onClick={() => setLang('en')}
            >EN</button>
            
            <button
              className={lang === 'it' ? 'active' : ''}
              onClick={() => setLang('it')}
            >IT</button>
        </div>


        <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
            <h1>{t.title}</h1>

            {!isRecording ? (
                <button onClick={startRecording}>{t.startRecording}</button>
            ) : (
                <button onClick={stopRecording}>{t.stopRecording}</button>
            )}

            {loading && <p className="loading-text">{t.processing}</p>}

            <div className="random-phrase-block">
                <button onClick={fetchRandomPhrase}>{t.getPhrase}</button>
                {randomPhrase && (
                    <div className="audio-section">
                        <p><strong>{t.trySaying}:</strong> {randomPhrase.text}</p>
                        <audio controls>
                            <source src={`http://localhost:5002${randomPhrase.audio_url}`} type="audio/mpeg" />
                            Your browser does not support the audio element.
                        </audio>
                    </div>
                )}
            </div>

            <div className="audio-blocks-container">
              {audioBlocks && audioBlocks.map((block, i) => (
                <div key={i} className="audio-block-with-response">
                  {block.response && (
                    <div className="response-block">
                      <p><strong>{t.expected}:</strong> {block.response.target}</p>
                      <p><strong>{t.youSaid}:</strong> {block.response.you_said}</p>
                      <p><strong>{t.feedback}:</strong> {JSON.stringify(block.response.feedback)}</p>
                    </div>
                  )}
                  <AudioBlock block={block} />
                </div>
              ))}
            </div>
        </div>
    </div>
  );
}

export default App;
