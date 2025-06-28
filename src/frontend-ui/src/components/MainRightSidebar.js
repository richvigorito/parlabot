import React, { useState } from 'react';

function RightSidebar({ selectedLevel, onLevelChange, phrases, selectedProvider, selectedSpeaker, lang, onSelectPhrase, targetPhrase }) {
  const [hideTranslations, setHideTranslations] = useState(false);

  return (
    <div className="sidebar">
      <div className="translation-toggle">
        <button
          onClick={() => setHideTranslations(prev => !prev)}
        >
          {hideTranslations ? lang.showTranslations : lang.hideTranslations}
        </button>
      </div>

      <h3>{lang.selectLevel}</h3>
      <div className="lang-level">
      {['A1', 'A2', 'B1', 'B2', 'C1', 'C2'].map(level => (
        <button
          key={level}
          onClick={() => onLevelChange(level)}
          className={`lang-level ${selectedLevel === level ? 'active-level' : ''}`}
        >
          {level}
        </button>
      ))}
      </div>

     {phrases && phrases.map((phrase, i) => {
  const isSelected = targetPhrase && phrase.text === targetPhrase.text;

  return (
    <div
      key={i}
      className="phrase-snippet"
      style={{ backgroundColor: isSelected ? '#008080' : 'transparent' }}
    >
      <button
        className="use-phrase-btn"
        title={lang.useThisPhrase || "Use this phrase"}
        onClick={() => onSelectPhrase(phrase)}
      >
        🔁
      </button>
      <p><strong>{phrase.text}</strong></p>
      {!hideTranslations && <p>{phrase.translation}</p>}
      {phrase.sources?.map(src => (
        src.source_name === selectedProvider && src.speaker === selectedSpeaker && (
          <audio key={src.audio_url} controls>
            <source src={src.audio_url} type="audio/mpeg" />
            Your browser does not support the audio element.
          </audio>
        )
      ))}
      <hr />
    </div>
  );
})} 
    </div>
  );
}

export default RightSidebar;
