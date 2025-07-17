# Parlabot Frontend UI in React  ⚛️ 

This frontend is built using React and is designed to work with the Parlabt backend. It provides a user interface for interacting with the backend services. By no means am I a React expert or even a frontend developer. Where possible I deferred funtionality to the backend. From a concerns perspective, this is a good thing. The frontend should be as dumb as possible and the backend should do all the heavy lifting. This makes working with the frontend much easier, allows for a more modular design and allows me to focus my efforts on the backend where I am more comfortable and am more concerned with broadening my tech stack, ie (Go, Python, Torch, MongoDB, etc).

## Overview
To use Parlabot a user will do the following:
1. Select a CERF langnuage level on the right sidebar. 
2. Preview and select a target phrase from the list of phrases now populated in the right sidebar.
3. Select a speaker from the list of speakers in the center panel.
4. Listen to the target phrase spoken by the selected speaker.
5. Optionally select/deselect which preprocessing pipelines to the input audio.
6. Click 'repeat target phrase', speak, click 'stop' to stop recording.
7. In the bottom panel results are returned, one for each preprocessing pipeline selected.
