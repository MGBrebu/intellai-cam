import cv2
import os
from datetime import datetime
import json

# DEF: Open a given camera using OpenCV
# Default camera ID: 0
# Returns cv2 camera feed object or None if error
def open_cam(cam_id=0):
    try:
        cam = cv2.VideoCapture(cam_id)
        if not cam.isOpened():
            print("Open Cam Error: Could not open camera.")
            return None
    except cv2.error as e:
        print("OpenCV Error:", e)
        return None
    return cam

# DEF: Save an analysis result to a JSON file
# Creates JSON file if it doesn't exist, otherwise appends
def save_analysis(result, output_file='./analysis/generic_analysis.json'):
    # Save selected fields + timestamp
    if not os.path.exists(output_file):
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        # Create an empty JSON file
        with open(output_file, "w") as f:
            f.write("[]\n")

    trimmed_analysis = {
        "timestamp": datetime.now().isoformat(), 
        "age": result.get("age", "Unknown"), 
        "gender": result.get("dominant_gender", "Unknown"), 
        "race": result.get("dominant_race", "Unknown")
    }

    try:
        with open(output_file, "r+") as f:
            data = json.load(f)
            data.append(trimmed_analysis)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
        print("Analysis Saved:", trimmed_analysis)
    except Exception as e:
        print("Save Analysis Error:", e)