import cv2
import json
import os
import datetime
from deepface import DeepFace

# Initialize frame counter
frame_count = 0

# Initialize webcam
cam = cv2.VideoCapture(0)

# Load OpenCV Haar cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


# -----------------------------------


def extract():
    # Convert to grayscale for Haar detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        # Draw rectangle around face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Crop face region
        face_img = frame[y:y+h, x:x+w]

        return face_img

def analyse(face_img):
    try:
        analysis = DeepFace.analyze(
            face_img,
            actions=['age', 'gender', 'race'],
            enforce_detection=False
        )
        return analysis

    except Exception as e:
        print("DeepFace error:", e)
        return {}

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

    if frame_count % 12 == 0:
        # Detect Faces
        face_img = extract()

        if face_img is not None:
            analysis = analyse(face_img)
        
            if isinstance(analysis, list) and len(analysis) > 0:
                    result = analysis[0]
                    save_analysis(result)
        
        # Show live feed
        cv2.imshow("Hybrid Model - Press 'q' to Quit", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Cleanup
cam.release()
cv2.destroyAllWindows()
