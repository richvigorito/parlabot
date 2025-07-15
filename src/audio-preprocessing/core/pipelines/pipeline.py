from typing import Tuple, List, Dict, Any
import torchaudio
import torch
import logging
import io
from core.audio_io import AudioIO
from core.filters.base_filter import Filter
from storage import make_storage
#from asgi_correlation_id import correlation_id

logger = logging.getLogger("stt-service")

class Pipeline():
    def __init__(self,  pipeline: List[Filter]):
        self.pipeline = pipeline

    def run(self, input_bytes: bytes) -> Tuple[List[Dict[str, Any]], torch.Tensor]:

        storage = make_storage()
        logger.info(f"Running pipeline with {len(self.pipeline)} filters")

        filterOutcomes = []

        filter_outcomes: List[Dict[str, Any]] = []
        current_bytes = input_bytes

        for idx, f in enumerate(self.pipeline):
            next_bytes = f.run_filter(current_bytes)
            logger.info(f"[{f.name}] output size: {len(next_bytes)} bytes")

            input_path = storage.build_storage_path(idx, f.name)
            output_path = storage.build_storage_path(idx, f.name)
            ## this is inefficient cause writes twice but right now who cares
            ## better alternive write the input file, enter loop, write output
            ## and link input next itr
            inF =storage.save_file(input_path, current_bytes)
            ouF = storage.save_file(output_path, next_bytes)

            filter_outcomes.append({
                "filter_name": f.name,
                #"input_file": input_path.replace("/app/shared", "/files", 1),
                #"output_file": output_path.replace("/app/shared", "/files", 1),
                "input_file": inF,
                "output_file": ouF,
                "metadata": {},
            })

            current_bytes = next_bytes
        waveform, _ = torchaudio.load(io.BytesIO(current_bytes))

        return filter_outcomes, waveform
