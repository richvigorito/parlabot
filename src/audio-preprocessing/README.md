#  Audio proprocessing service

The audio preprocessing service performs audio file manipulation prior to sending to the STT service. There are an array of different pipelines. These pipelines are composed of filters. While not all the pipelines/ filters are necessary its more of a tool for experimentation; in otherwords which transformations improves audio quality such that the STT tools have an easier time transcribing the audio file. Current supported filters are: 
- [Band-pass filter](https://en.wikipedia.org/wiki/Band-pass_filter)
- Wave amplification filter
- Silence Trimming filters (both front and end of wave)
