import React, { useState, useEffect } from 'react';
import './App.css';
import MicRecorder from 'mic-recorder-to-mp3';
import AudioBlock from './components/AudioBlock';
import Banner from './components/Banner';
import RightSidebar from './components/MainRightSidebar';
import LeftSidebar from './components/MainLeftSidebar';


import en from './locales/en.json';
import it from './locales/it.json';


const recorder = new MicRecorder({ bitRate: 128 });
const locales = { en, it };


function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [audioBlocks, setAudioBlocks] = useState([]);
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

  const fetchPhrasesForLevel = async (level) => {
    const res = await fetch(`http://localhost:5002/phrases?level=${level}`);
    const data = await res.json();
    setLevel(level); 
    setPhrases(data); 
  };

  const fetchPipelines = async () => {
    if(pipelines.length == 0) {
      const res = await fetch(`http://localhost:5003/pipelines`);
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

    //  const res = await fetch("http://localhost:5002/phrases/random=$LEVEL");
    var url = "http://localhost:5002/phrases/random";
    if(selectedLevel){
      url = "http://localhost:5002/phrases/random?level="+selectedLevel;
    }
    const res = await fetch(url);
    const phrase = await res.json();
    console.log(phrase, selectedLevel)
    setTargetPhrase(phrase);
   };

  const fetchSamplePhrase = async () => {
    const res = await fetch("http://localhost:5002/phrases?text=ciao&level=A1&limit=1");
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
    <Banner />
    <div className="app-container">
      <LeftSidebar />
      <div className="main-content">
        <div className="header-row">
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
                    const audio = new Audio(`http://localhost:5002${source.audio_url}`);
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
                      <source src={`http://localhost:5002${audio.audio_url}`} type="audio/mpeg" />
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
