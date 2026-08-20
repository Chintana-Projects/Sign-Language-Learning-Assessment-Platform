import json
from pathlib import Path
from datetime import datetime


class JSONSaver:

    def __init__(self):

        # SignSync Project Root
        self.project_root = Path(__file__).resolve().parents[3]

        # captures/
        self.capture_folder = self.project_root / "captures"
        self.capture_folder.mkdir(exist_ok=True)

    def save(self, landmark_data):

        existing_files = sorted(
            self.capture_folder.glob("capture_*.json")
        )

        file_number = len(existing_files) + 1

        file_name = f"capture_{file_number:03}.json"

        file_path = self.capture_folder / file_name

        data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "number_of_hands": len(landmark_data),
            "hands": []
        }

        for hand_index, hand in enumerate(landmark_data):

            hand_info = {
                "hand_number": hand_index + 1,
                "landmarks": hand
            }

            data["hands"].append(hand_info)

        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

        print(f"\nLandmarks saved to:\n{file_path}")