import React from 'react';
import '../Banner.css';
import { FaGithub, FaLinkedin } from 'react-icons/fa';

function Banner() {
  return (
    <div className="top-banner">
      <div className="left">
        <div className="mode-selector">
          <span className="mode active">Parlabot</span> | 
          <span className="mode">Vowel Recognizer</span>
        </div> 
      </div>
        •
        <a href="#about">About</a>
        <a href="https://github.com/richvigorito/parlabot" target="_blank" rel="noopener noreferrer">
          <FaGithub className="icon" /> GitHub
        </a>
        <a href="https://linkedin.com/in/rich-vigorito" target="_blank" rel="noopener noreferrer">
          <FaLinkedin className="icon" /> LinkedIn
        </a>
    </div>
  );
}

export default Banner;

 
