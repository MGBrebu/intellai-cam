import cv2
import json
import os
from deepface import DeepFace
import datetime

# -----------------------------------

# Open the default camera (0) using OpenCV
def open_cam(cam_id=0):
    cam = cv2.VideoCapture(cam_id)
    if not cam.isOpened():
        print("Error: Could not open camera.")
        return None
    return cam

# Deprecated: analyse() includes face detection
# Extracts faces from a frame using DeepFace
def extract(frame):
    try:
        faces = DeepFace.extract_faces(frame, detector_backend = 'mtcnn')
        return faces
    except Exception as e:
        print("Extraction Error:", e)
        return []

# Analyse a frame for faces and their facial attributes (age, gender, race) using DeepFace
def analyse(frame):
    try: 
        analysis = DeepFace.analyze(
            frame,
            actions = ['age', 'gender', 'race'],
            detector_backend = 'mtcnn'
        )
        return analysis
    except Exception as e:
        #print("Analysis Error:", e)
        analysis = {}

# Save an analysis result to a JSON file
# Creates JSON file if it doesn't exist, otherwise appends
def save_analysis(result, output_file='./analysis/single_face_analysis.json'):
    # Save selected fields + timestamp
    if not os.path.exists(output_file):
        with open(output_file, "w") as f:
            f.write("[]\n")

    trimmed_analysis = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
        "age": result.get("age", "Unknown"), "gender": result.get("dominant_gender", "Unknown"), 
        "race": result.get("dominant_race", "Unknown")
    }

    try:
        with open(output_file, "r+") as f:
            data = json.load(f)
            data.append(trimmed_analysis)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
        print("Saved:", trimmed_analysis)
    except Exception as e:
        print("Error saving analysis:", e)

# Uses above functions to open the camera, read frames, and analyse faces
def run_model(framerate=24, frequency=24, cam_ids=[0]):
    frame_count = 0

    cams = [open_cam(cam_id) for cam_id in cam_ids]

    while True:
        for cam in cams:
            ret, frame = cam.read()
            if not ret:
                print("Error: Could not read frame from camera.")
                continue

            frame_count += 1

            if frame_count % frequency == 0:
                analysis = analyse(frame)

                if isinstance(analysis, list) and len(analysis) > 0:
                    result = analysis[0]
                    save_analysis(result)
            
            cv2.imshow(f"Camera Feed {cam}", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cam.release()
    cv2.destroyAllWindows()

# -----------------------------------

# Main for testing
def main():
    run_model()

# -----------------------------------

if __name__ == "__main__":
    main()
