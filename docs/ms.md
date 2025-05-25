# Thesis Background: Creating a Frontend for a Speech Recognition System

In 2007, I completed my Master’s thesis in Computer Science:

**“Creating a Frontend for a Speech Recognition System”**

It focused on building a vowel recognition front-end using:
- **CMU Sphinx** — a Java-based open-source ASR engine
- **Digital Signal Processing (DSP)** — including FFTs, pre-emphasis filters, Mel filter banks, and MFCC extraction
- A frontend that visualized time-domain signals and converted them into phoneme-friendly features

The system was part of a larger academic effort by Dr Dan Harvey and Southern Oregon University CS department for tthe **ACquisition Of Restored Native Speech (ACORNS) project**. ACORNS aimed to support Native American language revitalization through technology. It emphasized vowel-level recognition as a building block for phonetic precision in low-resource language education. ACORNS is publicly available on [github](https://github.com/language-apps).

### Lessons and Reflection

Looking back, while ACORNS was focused on indigenous speech, it’s interesting to consider that **Italian might have been a smarter starting point** — phonetically rich, vowel-heavy, and more uniform in pronunciation. Italian has clearly separated vowels that are pronounced consistently, which makes it a surprisingly good candidate for building and testing STT systems. 

ParlaBot, in many ways, picks up where that early project left off — this time using:
- Modern AI tooling (Transformers, Hugging Face)
- A full microservice architecture
- Italian as the focus, inspired by personal language learning

### For the Curious

If you want to dig into my original thesis, with help from a Libray Department at SOU I was able to track down a copy. Here it is in all its Java/NetBeans/CVS glory. 
**[Download the thesis (PDF)](/docs/MastersThesis-Creating_A_Frontend_for_a_SpeechRecognitonSystem.pdf)**

