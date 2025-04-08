import cv2
import json
import os
from deepface import DeepFace
import datetime

# Open default camera
# 0 : Default Camera
cam = cv2.VideoCapture(0)
frame_count = 0

# -----------------------------------

def extract(frame):
    try:
        faces = DeepFace.extract_faces(frame, detector_backend = 'mtcnn')
        return faces
    except Exception as e:
        print("Extraction Error:", e)
        return []

def analyse():
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

def save_analysis(result, output_file='./analysis/single_face_analysis.json'):
    # Save selected fields + timestamp
    if not os.path.exists(output_file):
        with open(output_file, "w") as f:
            f.write("[]\n")

    trimmed_analysis = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
        print("Saved:", trimmed_analysis)
    except Exception as e:
        print("Error saving analysis:", e)


# -----------------------------------


while True:
    ret, frame = cam.read()
    if not ret:
        break
    
    frame_count += 1

    # Run only every 12 frames
    if frame_count % 12 == 0:
    
        analysis = analyse()
        if isinstance(analysis, list) and len(analysis) > 0:
            result = analysis[0]
            save_analysis(result)

        # Display the frame
        cv2.imshow("Face Detection", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

# --------------

# Stop | Release and Close Windows
cam.release()
cv2.destroyAllWindows()