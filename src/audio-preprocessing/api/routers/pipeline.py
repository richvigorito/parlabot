import logging
from fastapi import APIRouter, UploadFile, File,  HTTPException
from typing import Dict, Any


from core.pipelines.pipeline import Pipeline
from core.filters.trim_leading_silence import TrimLeadingSilence
from core.filters.amplify import Amplify
from core.filters.trim_trailing_silence import TrimTrailingSilence
from core.filters.resample import ResampleTo16k
from core.filters.band_pass_filter import BandPassFilter 

logger = logging.getLogger("audio-preprocessor")

class PipelineRouter:
    def __init__(self):
        self.router = APIRouter()
        self.pipelines = {
            "all-filters": Pipeline([
                ResampleTo16k(),
                Amplify(),
                BandPassFilter(),
                TrimLeadingSilence(),
                TrimTrailingSilence(),
            ]),
            "no-amplification": Pipeline([
                ResampleTo16k(),
                BandPassFilter(),
                TrimLeadingSilence(),
                TrimTrailingSilence(),
            ]),
            "resample-only": Pipeline([
                ResampleTo16k(),
            ]),
            "amplify-only": Pipeline([
                ResampleTo16k(),
                Amplify(),
            ]),
            "band-pass-filter-only": Pipeline([
                ResampleTo16k(),
                BandPassFilter(),
            ]),
            "trim-leading-silence-only": Pipeline([
                ResampleTo16k(),
                TrimLeadingSilence(),
            ]),
            "trim-trailing-silence-only": Pipeline([
                ResampleTo16k(),
                TrimTrailingSilence(),
            ]),
            "no-trimming": Pipeline([
                ResampleTo16k(),
                Amplify(),
                BandPassFilter(),
            ]),
            "trim-only": Pipeline([
                ResampleTo16k(),
                Amplify(),
                BandPassFilter(),
            ]),
        }

        self.router.post("/pipelines/{pipeline_name}/run")(self.run_pipeline)
        self.router.get("/pipelines")(self.get_pipelines)

    async def get_pipelines(self):
        return list(self.pipelines.keys())
    
    async def run_pipeline(self, pipeline_name: str, file: UploadFile = File(...)):
        logger.info(f"requested pipeline: {pipeline_name}")
        if pipeline_name not in self.pipelines:
            raise HTTPException(status_code=400, detail=f"Unknown pipeline: {pipeline_name}")
        audio_bytes = await file.read()
        pipeline = self.pipelines[pipeline_name]

        filter_outcomes, waveform = pipeline.run(audio_bytes)
        logger.info(f"Applied pipeline: {pipeline_name}")
        return {
            "input_file": filter_outcomes[0]["input_file"],
            "transformations": filter_outcomes,
            "output_file": filter_outcomes[-1]["output_file"],
            "waveform": waveform,
        }

router = PipelineRouter().router
