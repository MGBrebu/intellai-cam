import cv2
import json
import os
import datetime
from deepface import DeepFace

from utils.model_utils import open_cam, save_analysis
from utils.timer import Timer

# -----------------------------------

class HybridModel:
    # Extracts faces from a frame using OpenCV Haar cascades
    def extract(self, frame):
        try:
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
        except Exception as e:
            print("Extraction Error:", e)
            return None, None

    # Analyse a frame for faces and their facial attributes (age, gender, race) using DeepFace
    def analyse(self, frame):
        try: 
            analysis = DeepFace.analyze(
                frame,
                actions = ['age', 'gender', 'race'],
                detector_backend = 'mtcnn',
                enforce_detection=False
            )
            return analysis
        except Exception as e:
            print("Analysis Error:", e)
            analysis = {}

    # Uses above functions to open the camera, read frames, and analyse faces
    def run_model(self, framerate=24, frequency=24, cam_ids=[0]):
        print("----------------------")
        print("Running Model - HYBRID")
        print("----------------------")

        # Initialise timers
        total_timer = Timer(label="Total")
        analysis_timer = Timer(label="Analysis")

        total_timer.start()

        frame_counter = 0
        analysis_counter = 0

        cams = [open_cam(cam_id) for cam_id in cam_ids]
        if None in cams:
            print("Run Model Error: One or more cameras could not be opened.")
            return
        if not cams:
            print("Run Model Error: No cameras available.")
            return
        
        for cam in cams:
            cam.set(cv2.CAP_PROP_FPS, framerate)

        while True:
            for cam in cams:
                ret, frame = cam.read()
                if not ret:
                    print("Run Model Error: Could not read frame from camera.")
                    continue

                frame_counter += 1

                if frame_counter % frequency == 0:
                    analysis_timer.start()

                    face_img, faces_coords = self.extract(frame)
                    
                    if face_img is not None:
                        x, y, w, h = faces_coords
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        analysis = self.analyse(face_img)

                        if isinstance(analysis, list) and len(analysis) > 0:
                            result = analysis[0]
                            save_analysis(result)
                            analysis_counter += 1
                        
                    print(f"Frame: {frame_counter}")
                    analysis_timer.stop()
                
                cv2.imshow(f"Camera Feed {cam}", frame)

            if total_timer.get_time() > 20:
                print("20 seconds elapsed, stopping analysis.")
                break
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        total_timer.stop()

        cam.release()
        cv2.destroyAllWindows()

        # Performance Summary
        print("\n========= HYBRID  MODEL =========")
        print("====== Performance Summary ======")
        print(f"Processed Frames: {frame_counter}")
        print(f"Analysed Frames: {analysis_counter}")
        estimated_fps = frame_counter / total_timer.total_time if total_timer.total_time > 0 else 0
        print(f"Estimated FPS: {estimated_fps:.2f}")
        
        total_timer.summary(False, False)
        analysis_timer.summary()

# -----------------------------------

# Main
def main():
    model = HybridModel()
    model.run_model(framerate=24, frequency=24, cam_ids=[0])

# -----------------------------------

if __name__ == "__main__":
    main()

