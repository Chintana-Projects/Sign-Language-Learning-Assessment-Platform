from pathlib import Path
import json
from datetime import datetime


class InferenceLogger:
    """
    Logs inference metadata for debugging and monitoring.
    """

    def __init__(self):

        self.logs_dir = (
            Path(__file__).resolve().parents[3]
            / "logs"
        )

        self.logs_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.log_file = (
            self.logs_dir
            / "inference_log.jsonl"
        )

    # ----------------------------------------
    # Log one inference
    # ----------------------------------------

    def log(
        self,
        prediction,
        confidence,
        model_version,
        inference_time_ms
    ):

        record = {

            "timestamp":
                datetime.now().isoformat(),

            "prediction":
                prediction,

            "confidence":
                round(confidence, 4),

            "model_version":
                model_version,

            "inference_time_ms":
                round(inference_time_ms, 2)

        }

        with open(
            self.log_file,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                json.dumps(record)
            )

            file.write("\n")