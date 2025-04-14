import cv2
from deepface import DeepFace

from utils.model_utils import open_cam, save_analysis
from utils.timer import Timer
from utils.db_utils import init_db, save_analysis_db


# -----------------------------------

class SingleModel:
    # Deprecated: analyse() includes face detection
    # Extracts faces from a frame using DeepFace
    def extract(self, frame):
        try:
            faces = DeepFace.extract_faces(frame, detector_backend = 'mtcnn')
            return faces
        except Exception as e:
            print("Extraction Error:", e)
            return []

    # Analyse a frame for faces and their facial attributes (age, gender, race) using DeepFace
    def analyse(self, frame):
        try: 
            analysis = DeepFace.analyze(
                frame,
                actions = ['age', 'gender', 'race'],
                detector_backend = 'mtcnn'
            )
            return analysis
        except Exception as e:
            print("Analysis Error:", e)
            analysis = {}

    # Uses above functions to open the camera, read frames, and analyse faces
    def run_model(self, framerate=24, frequency=24, cam_ids=[0]):
        print("----------------------")
        print("Running Model - SINGLE")
        print("----------------------")

        init_db()

        total_timer = Timer(label="Total")
        analysis_timer = Timer(label="Analysis")

        frame_counter = 0
        analysis_counter = 0

        total_timer.start()

        # Open specified cameras and set framerate
        cams = [open_cam(cam_id) for cam_id in cam_ids]
        if None in cams:
            print("Run Model Error: One or more cameras could not be opened.")
            return
        if not cams:
            print("Run Model Error: No cameras available.")
            return
        for cam in cams:
            cam.set(cv2.CAP_PROP_FPS, framerate)

        # Main loop for live camera feed and analysis
        while True:
            for cam in cams:
                ret, frame = cam.read()
                if not ret:
                    print("Run Model Error: Could not read frame from camera.")
                    continue

                frame_counter += 1

                if frame_counter % frequency == 0:
                    analysis_timer.start()

                    analysis = self.analyse(frame)

                    if isinstance(analysis, list) and len(analysis) > 0:
                        result = analysis[0]
                        save_analysis(result, './analysis/singlemodel_analysis.json')
                        save_analysis_db(result)
                        analysis_counter += 1

                    print(f"Frame: {frame_counter}")
                    analysis_timer.stop()
                    

                cv2.imshow(f"Camera Feed {cam}", frame)

            # -------------------------------
            # TESTING - STOP AFTER 20 SECONDS
            if total_timer.get_time() > 20:
                print("20 seconds elapsed, stopping analysis.")
                break
            # -------------------------------
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        total_timer.stop()

        cam.release()
        cv2.destroyAllWindows()

        # Performance Summary
        print("\n========= SINGLE  MODEL =========")
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
    model = SingleModel()
    model.run_model(framerate=24, frequency=24, cam_ids=[0])

# -----------------------------------

if __name__ == "__main__":
    main()
