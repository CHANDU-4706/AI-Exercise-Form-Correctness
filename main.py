import cv2
import argparse
import time
import mlflow
from src.pose_detector import PoseDetector
from src.visualizer import Visualizer
from src.exercises.bicep_curl import BicepCurl
from src.exercises.lateral_raise import LateralRaise
from src.exercises.squat import Squat
from src.exercises.pushup import Pushup
from src.exercises.shoulder_press import ShoulderPress

def main():
    parser = argparse.ArgumentParser(description="AI Gym Trainer Form Correction")
    parser.add_argument("--video", type=str, default=None, help="Path to video file. Default is webcam.")
    parser.add_argument("--exercise", type=str, default="curl", choices=["curl", "lateral", "squat", "pushup", "press"], help="Exercise type")
    args = parser.parse_args()

    # Initialize Exercise
    if args.exercise == "curl":
        exercise = BicepCurl()
    elif args.exercise == "lateral":
        exercise = LateralRaise()
    elif args.exercise == "squat":
        exercise = Squat()
    elif args.exercise == "pushup":
        exercise = Pushup()
    elif args.exercise == "press":
        exercise = ShoulderPress()
    else:
        print("Invalid exercise")
        return

    # Initialize Detector
    detector = PoseDetector(detection_confidence=0.7) # Higher confidence for robustness
    visualizer = Visualizer()
    
    # Video Capture
    source = 0 if args.video is None else args.video
    cap = cv2.VideoCapture(source)
    
    pTime = 0
    
    print(f"Starting AI Trainer for {args.exercise}...")

    # MLflow Setup
    mlflow.set_experiment("AI_Trainer_Form_Correction")
    
    with mlflow.start_run():
        mlflow.log_param("exercise_type", args.exercise)
        mlflow.log_param("video_source", "webcam" if args.video is None else args.video)

        while True:
            success, img = cap.read()
            if not success:
                print("Video ended or camera error.")
                break
            
        # Resize for performance and consistency if needed
        # img = cv2.resize(img, (1280, 720))

            # 1. Detect Pose
            img, results = detector.find_pose(img)
            
            # 2. Get Landmarks
            lm_list = detector.find_position(img, draw=False)
            
            # 3. Exercise Logic
            if len(lm_list) != 0:
                if results.pose_landmarks:
                    exercise.check_form(results.pose_landmarks.landmark)
        

        
            # 4. Visuals
            feedback = exercise.get_feedback()
            count = exercise.get_counter()
            
            visualizer.draw_counter(img, count)
            
            # Dynamic color for feedback
            color = (0, 255, 0)
            if "Lower" in feedback or "Raise" in feedback or "Back" in feedback:
                color = (0, 0, 255) # Red for corrections
                
            visualizer.draw_feedback(img, feedback, color)

            # FPS calculation
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, f'FPS: {int(fps)}', (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

            cv2.imshow("AI Trainer", img)
            
            # 'q' to Quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        cap.release()
        cv2.destroyAllWindows()
        
        # Log final metrics
        final_reps = exercise.get_counter()
        mlflow.log_metric("total_reps", final_reps)
        print(f"Values logged to MLflow. Total Reps: {final_reps}")

if __name__ == "__main__":
    main()
