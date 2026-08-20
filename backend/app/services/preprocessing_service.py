from pathlib import Path
import subprocess
import sys
import json


class PreprocessingService:

    def __init__(self):

        self.project_root = (
    Path(__file__).resolve().parents[3]
)

        self.extract_script = (
            self.project_root
            / "scripts"
            / "extract_landmarks.py"
        )

        self.validator_script = (
    self.project_root
    / "scripts"
    / "dataset_validator.py"
)

        self.generated_dir = (
            self.project_root
            / "generated"
        )

        self.csv_file = (
            self.generated_dir
            / "asl_landmarks.csv"
        )

        self.report_file = (
            self.generated_dir
            / "dataset_report.json"
        )

    # ------------------------------------------
    # Run a script safely
    # ------------------------------------------

    def run_script(self, script):

        if not script.exists():
            raise FileNotFoundError(
                f"Script not found:\n{script}"
            )

        result = subprocess.run(
            [
                sys.executable,
                str(script)
            ],
            cwd=str(self.project_root),
            capture_output=True,
            text=True
        )

        if result.returncode != 0:

            raise RuntimeError(
                f"Script failed:\n{result.stderr}"
            )

        return result.stdout

    # ------------------------------------------
    # Preprocess dataset
    # ------------------------------------------

    def preprocess(self):

        # 1. Generate landmarks CSV
        extraction_output = self.run_script(
            self.extract_script
        )

        # 2. Generate validation report
        validation_output = self.run_script(
            self.validator_script
        )

        # 3. Read generated report
        if self.report_file.exists():

            with open(
                self.report_file,
                "r",
                encoding="utf-8"
            ) as file:

                report = json.load(file)

        else:

            report = {}

        return {
            "success": True,
            "message": "Dataset preprocessing completed.",
            "data": {
                "images_processed":
                    report.get(
                        "total_images_processed",
                        0
                    ),

                "successful":
                    report.get(
                        "successful_landmark_detections",
                        0
                    ),

                "failed":
                    report.get(
                        "no_hand_detected",
                        0
                    ),

                "csv_file":
                    str(self.csv_file),

                "report_file":
                    str(self.report_file),

                "success_percentage":
                    report.get(
                        "success_percentage",
                        0
                    )
            }
        }