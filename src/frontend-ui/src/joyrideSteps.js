import React from 'react';


export default function getSteps(t, setLang) {
  const langToggle  = (
              <div style={{ marginTop: 10 }}>
                <button onClick={() => setLang('en')}>EN 🇺🇸</button>
                <button onClick={() => setLang('it')}>IT 🇮🇹</button>
            </div>
  );

  const html = (str) => <span dangerouslySetInnerHTML={{ __html: str }} />;


  return [
    {
      target: '.header-row',
      content: (
            <div>
              <p>{html(t.joyride.startTour)}</p>
              {langToggle}
            </div>
      ), 
    },
    {
      target: '.lang-switcher',
      content: 
      (
            <div>
              <p>{html(t.joyride.languageToggle)}</p>
              {langToggle}
            </div>
      ), 
    },
    {
      target: '.lang-level',
      content: 
      (
            <div>
              <p>{html(t.joyride.languageLevel)}</p>
              {langToggle}
            </div>
      ), 
    },
    {
      target: '.hide-translations-button',
      content: 
      (
            <div>
              <p>{html(t.joyride.hideTranslations)}</p>
              {langToggle}
            </div>
      ), 
    },
    {
      target: '.speaker-preview',
      content: 
      (
            <div>
              <p>{html(t.joyride.speakerSelection)}</p>
              {langToggle}
            </div>
      ), 
    },
    {
      target: '.random-phrase-block',
      content: 
      (
            <div>
              <p>{html(t.joyride.selectPhrase)}</p>
              {langToggle}
            </div>
      ), 
    },
    {
      target: '.pipelines-container',
      content: 
      (
            <div>
              <p>{html(t.joyride.results)}</p>
              {langToggle}
            </div>
      ), 
    },
    {
      target: '.top-banner',
      content: 
      (
            <div>
              <p>{html(t.joyride.endTour)}</p>
              {langToggle}
            </div>
      ) 
    }
  ];
}
