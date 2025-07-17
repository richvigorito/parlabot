import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import MicRecorder from 'mic-recorder-to-mp3';
import AudioBlock from './components/AudioBlock';
import Banner from './components/Banner';
import RightSidebar from './components/MainRightSidebar';
import LeftSidebar from './components/MainLeftSidebar';
import Joyride from 'react-joyride';
import getSteps from './joyrideSteps';
import { API_ORCHESTRATOR_URL, PHRASE_SERVICE_URL, AUDIO_PREPROCESSING_URL } from './config';


import en from './locales/en.json';
import it from './locales/it.json';

const recorder = new MicRecorder({ bitRate: 128 });
const locales = { en, it };

function App() {
  console.log("App started");
  console.log("API_ORCHESTRATOR_URL", API_ORCHESTRATOR_URL);
  console.log("API_PHRASE_SERVICE_URL", PHRASE_SERVICE_URL);
  console.log("API_AUDIO_PREPROCESSING_URL", AUDIO_PREPROCESSING_URL);

  const [isRecording, setIsRecording] = useState(false);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const recorderRef = useRef(null);
  
  // Changed: Now storing pipeline results separately
  const [pipelineResults, setPipelineResults] = useState({});
  const [targetPhrase, setTargetPhrase] = useState(null);

  const [speakers, setSpeakers] = useState(null);
  const [selectedProvider, setSelectedProvider] = useState(null);
  const [selectedSpeaker, setSelectedSpeaker] = useState(null);
  const [selectedLevel, setLevel] = useState(null);
  const [selectedPhrases, setPhrases] = useState(null);
  const [pipelines, setPipelines] = useState([]);
  const [selectedPipelines, setSelectedPipelines] = useState([]);

  const [lang, setLang] = useState('it');
  const t = locales[lang];
  const steps = getSteps(t, setLang);

  const fetchPhrasesForLevel = async (level) => {
    const res = await fetch(`${PHRASE_SERVICE_URL}/phrases?level=${level}`);
    const data = await res.json();
    setLevel(level); 
    setPhrases(data); 
  };

  const fetchPipelines = async () => {
    if(pipelines.length == 0) {
      const res = await fetch(`${AUDIO_PREPROCESSING_URL}/pipelines`);
      const data = await res.json();
      setPipelines(data); 
      setSelectedPipelines(data); 
    }
  };

  const fetchTargetPhrase = async () => {
    if (!selectedProvider || !selectedSpeaker) {
      alert("Please select a provider and speaker first.");
      return;
    }
  
    var url = `${PHRASE_SERVICE_URL}/phrases/random`;
    if(selectedLevel){
      url = PHRASE_SERVICE_URL+"/phrases/random?level="+selectedLevel;
    }
    const res = await fetch(url);
    const phrase = await res.json();
    console.log(phrase, selectedLevel)
    setTargetPhrase(phrase);
   };

  const fetchSamplePhrase = async () => {
    const res = await fetch(`${PHRASE_SERVICE_URL}/phrases?text=ciao&level=A1&limit=1`);
    const data = await res.json();

    const first = data[0]?.sources?.[0];
    if (first) {
      setSelectedProvider(first.source_name);
      setSelectedSpeaker(first.speaker);
    }
    
    // Organize into provider -> [speakers]
    const grouped = {};
    data[0].sources.forEach(source => {
      if (!grouped[source.source_name]) {
        grouped[source.source_name] = [];
      }
      if (!grouped[source.source_name].includes(source.speaker)) {
        grouped[source.source_name].push(source.speaker);
      }
    });

    setSpeakers(grouped);
    setTargetPhrase(data[0]); // Also load that sample phrase for UI
  }; 

  const handleSelectPhrase = (phrase) => {
    setTargetPhrase(phrase);
  };

   const startRecording = async () => {
    if (!recorderRef.current) return;
    
    try {
      await recorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Failed to start recording:', error);
      alert('Failed to start recording. Please check microphone permissions.');
    }
  };

  const stopRecording = async () => {
    if (!recorderRef.current || !isRecording) return;
    
    try {
      const [buffer, blob] = await recorderRef.current.stop().getMp3();
      setIsRecording(false);
      sendAudio(blob);
    } catch (error) {
      console.error('Failed to stop recording:', error);
      setIsRecording(false);
      alert('Failed to process recording.');
    }
  }; 

  const sendAudio = async (blob) => {
    setLoading(true);
    // Clear previous results
    setPipelineResults({});
    
    const formData = new FormData();
    formData.append("file", new File([blob], "recording.wav", { type: "audio/wav" }));
    // Add selected pipelines to the request
    //formData.append("pipelines", JSON.stringify(selectedPipelines));
    selectedPipelines.forEach(p => formData.append("pipelines", p));


    try {
      const res = await fetch(`${API_ORCHESTRATOR_URL}/api/transcribe`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      console.log(data);
      setResponse(data);
     
      setResponse(data); // optional if you still want to keep full response

      const newPipelineResults = {};

      if (Array.isArray(data.results)) {
        data.results.forEach((block) => {
          const pipelineName = block.pipeline || `Pipeline ${Object.keys(newPipelineResults).length + 1}`;
          newPipelineResults[pipelineName] = block;
        });
      } else {
        alert("Unexpected response format from server.");
      }

      setPipelineResults(newPipelineResults);
        
    } catch (err) {
      console.error(err);
      alert("Failed to send audio.");
    } finally {
      setLoading(false);
    }
  };

  // Initialize recorder
  useEffect(() => {
    recorderRef.current = new MicRecorder({ bitRate: 128 });
    
    // Cleanup on unmount
    return () => {
      if (recorderRef.current && isRecording) {
        try {
          recorderRef.current.stop();
        } catch (error) {
          console.warn('Recorder cleanup error:', error);
        }
      }
    };
  }, []);

  useEffect(() => {
    fetchSamplePhrase()
  }, []);

  useEffect(() => {
    fetchPipelines()
  }, []);
  
  useEffect(() => {
    if (selectedLevel) {
      fetchPhrasesForLevel(selectedLevel);
    }
  }, [selectedLevel]);

  return (
    <>
   <Joyride
  steps={steps}
  run={true}
  continuous={true}
  showSkipButton={true}
  styles={{
    options: {
      zIndex: 10000,
      overlayColor: 'rgba(0, 0, 0, 0.7)',

      beaconSize: 100,        // MASSIVE beacon
      beaconInnerSize: 50,
      beaconOuterSize: 100,

      primaryColor: '#ff0000',

      spotlightShadow: '0 0 40px 15px rgba(255,0,0,1)',
    },
    beacon: {
      cursor: 'pointer',
      animation: 'pulse 1.5s infinite',
      borderRadius: '50%',
    },
  }} 
  /> 
    <Banner />
    <div className="app-container">
      <LeftSidebar />
      <div className="main-content">
        <div className="header-row">
          <img src="/parlabot.200x200.png" alt="Logo" className="logo" />
          <h1>{t.title}</h1>
          <div className="lang-switcher">
            <button className={lang === 'en' ? 'active' : ''}
              onClick={() => setLang('en')}>
              EN 🇺🇸
            </button>
            <button className={lang === 'it' ? 'active' : ''}
              onClick={() => setLang('it')}>
              IT 🇮🇹
            </button>
          </div>
        </div>

        {selectedProvider && selectedSpeaker && (
          <>
            <p>🎤 {t.using}:
              <strong><em> {selectedProvider} / {selectedSpeaker}</em></strong>
            </p>
            <p>{t.chooseDifferentSpeaker}</p>
          </>
        )}

        {targetPhrase && (
          <div className="speaker-preview">
            {targetPhrase.sources.map((source, i) => (
              <div key={i} className={`speaker-card ${selectedProvider === source.source_name && selectedSpeaker === source.speaker ? 'active' : ''}`}>
                <button
                  className="icon-button"
                  onClick={() => {
                    const audio = new Audio(source.audio_url);
                    audio.play();
                  }}
                >
                  ▶️
                </button>
                <span className="speaker-info">{source.source_name} / {source.speaker}</span>
                <button
                  className="icon-button"
                    onClick={() => {
                      setSelectedProvider(source.source_name);
                      setSelectedSpeaker(source.speaker);
                    }}
                >
                  ✅
                </button>
              </div>
            ))}
          </div>
        )}

        <div className="random-phrase-block">
            <button onClick={fetchTargetPhrase}>{t.getPhrase}</button>
            {targetPhrase && (
              <div className="audio-section">
                  <p><strong>{t.trySaying}:</strong> {targetPhrase.text}</p>
                  {targetPhrase.sources?.map(audio => (
                      audio.source_name === selectedProvider && audio.speaker === selectedSpeaker && (
                    <audio key={audio.audio_url} controls>
                      <source src={audio.audio_url} type="audio/mpeg" />
                      Your browser does not support the audio element.
                    </audio>
                  )
                  ))}
              </div>
            )} 

          {!isRecording ? (
            <button onClick={startRecording}>{t.startRecording}</button>
          ) : (
            <button onClick={stopRecording}>{t.stopRecording}</button>
          )}

          {loading && <p className="loading-text">{t.processing}</p>}
        </div>

        <div className="pipelines-container">
          <h2>{t.pipelines}</h2>
          <div className="pipelines-grid">
            {pipelines.map((name, i) => {
              const checked = selectedPipelines.includes(name);
              return (
                <label
                  key={i}
                  className={`pipeline-item${checked ? ' checked' : ''}`}
                >
                  <input
                    type="checkbox"
                    checked={checked}
                    onChange={() => {
                      if (checked) {
                        setSelectedPipelines(selectedPipelines.filter(p => p !== name));
                      } else {
                        setSelectedPipelines([...selectedPipelines, name]);
                      }
                    }}
                  />
                  {name}
                </label>
              );
            })}
          </div>
        </div>
 
        {/* Updated: Display pipeline results organized by pipeline */}
        <div className="pipeline-results-container">
          {Object.entries(pipelineResults).map(([pipelineName, block]) => (
            <div key={pipelineName} className="pipeline-result-section">
              <div className="pipeline-header">
                {block.response && (
                  <div className="response-summary">
                    <span className="response-indicator">
                      Score: {block.response.feedback?.pronunciation_score || 'N/A'}
                    </span>
                  </div>
                )}
              </div>
              
              {block.response && (
                <div className="response-block">
                  <p><strong>{t.expected}:</strong> {block.response.target}</p>
                  <p><strong>{t.youSaid}:</strong> {block.response.you_said}</p>
                  <p><strong>{t.feedback}:</strong> {JSON.stringify(block.response.feedback)}</p>
                </div>
              )}
             
              { console.log(block)}
              <AudioBlock block={block} />
            </div>
          ))}
        </div>
      </div>
      <RightSidebar
        selectedLevel={selectedLevel}
        onLevelChange={fetchPhrasesForLevel}
        phrases={selectedPhrases}
        selectedProvider={selectedProvider}
        selectedSpeaker={selectedSpeaker}
        lang={t}
        onSelectPhrase={handleSelectPhrase}
        targetPhrase={targetPhrase}
      />
    </div>
    </>
  );
}

export default App;
