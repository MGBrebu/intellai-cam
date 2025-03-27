import cv2
from deepface import DeepFace
import datetime

# Open default camera
# 0 : Default Camera
cam = cv2.VideoCapture(0)
frame_count = 0

# --------------

def extract():
    try:
        faces = DeepFace.extract_faces(frame, detector_backend = 'mtcnn')
        return faces
    except Exception as e:
        #print("Error:", e)
        cv2.imshow("Face Detection", frame)
        faces = []
        return faces

def analyse():
    try: 
        analysis = DeepFace.analyze(
            frame,
            actions = ['age', 'gender', 'race'],
            detector_backend = 'mtcnn'
        )

        for face_analysis in analysis:
            analysis_data = {
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "age": face_analysis["age"],
                "gender": face_analysis["dominant_gender"],
                "race": face_analysis["dominant_race"]
            }
            try:
                with open("./analysis/face_analysis.json", "a") as file:
                    file.write(str(analysis_data) + "\n")
            except Exception as e:
                print("File Write Error:", e)
    
    except Exception as e:
        #print("Analysis Error:", e)
        analysis = {}

# --------------

while True:
    ret, frame = cam.read()
    if not ret:
        break
    
    frame_count += 1

    # Run only every 12 frames
    if frame_count % 12 == 0:
        # Detect Faces
        faces = extract()

        for face in faces:
            # Draw bounding box
            facial_area = face["facial_area"]
            x = facial_area['x']
            y = facial_area['y']
            w = facial_area['w']
            h = facial_area['h']
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Analyse Faces
            analyse()

        # Display the frame
        cv2.imshow("Face Detection", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

# --------------

# Stop | Release and Close Windows
cam.release()
cv2.destroyAllWindows()