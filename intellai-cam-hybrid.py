import cv2
import json
import os
import datetime
from deepface import DeepFace

# -----------------------------------

# Open the default camera (0) using OpenCV
def open_cam(cam_id=0):
    cam = cv2.VideoCapture(cam_id)
    if not cam.isOpened():
        print("Error: Could not open camera.")
        return None
    return cam

# Extracts faces from a frame using OpenCV Haar cascades
def extract(frame):
    # Load OpenCV Haar cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Convert to grayscale for Haar detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        # Draw rectangle around face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Crop face region
        faces_coords = (x, y, w, h)
        face_img = frame[y:y+h, x:x+w]

        return face_img, faces_coords
    return None, None

# Analyse a frame for faces and their facial attributes (age, gender, race) using DeepFace
def analyse(frame):
    try: 
        analysis = DeepFace.analyze(
            frame,
            actions = ['age', 'gender', 'race'],
            detector_backend = 'mtcnn',
            enforce_detection=False
        )
        return analysis
    except Exception as e:
        #print("Analysis Error:", e)
        analysis = {}

# Save an analysis result to a JSON file
# Creates JSON file if it doesn't exist, otherwise appends
def save_analysis(result, output_file='./analysis/hybrid_face_analysis.json'):
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
                face_img, faces_coords = extract(frame)
                # Draw rectangle around face
                if face_img is not None:
                    x, y, w, h = faces_coords
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    analysis = analyse(face_img)

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

