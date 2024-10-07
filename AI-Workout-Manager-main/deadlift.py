import math
import time
import cv2
import mediapipe as mp
import numpy as np
import pandas 

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (0, 0, 255)
BLUE = (245, 117, 25)
DARK_BLUE = (0, 0, 128)

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / math.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def display_clock_icon(image, icon_path, height, width):
    clock_icon = cv2.imread(icon_path, -1)
    icon_size = 200
    clock_icon = cv2.resize(clock_icon, (375, icon_size))
    x_offset = width - clock_icon.shape[1] - 120
    y_offset = 260
    if clock_icon.shape[2] == 4:
        alpha_icon = clock_icon[:, :, 3] / 255.0
        alpha_image = 1.0 - alpha_icon
        for c in range(0, 3):
            image[y_offset:y_offset + clock_icon.shape[0], x_offset:x_offset + clock_icon.shape[1], c] = \
                alpha_icon * clock_icon[:, :, c] + \
                alpha_image * image[y_offset:y_offset + clock_icon.shape[0], x_offset:x_offset + clock_icon.shape[1], c]
    else:
        image[y_offset:y_offset + clock_icon.shape[0], x_offset:x_offset + clock_icon.shape[1]] = clock_icon
    return image

def display_time(image, start_time, height, width):
    elapsed_time = time.time() - start_time
    hours, rem = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(rem, 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    elapsed_time = "{:02}:{:02}:{:02}.{:03}".format(int(hours), int(minutes), int(seconds), milliseconds)
    position = (int(width / 2 + 200), int(height / 2))
    cv2.putText(image, elapsed_time, position, cv2.FONT_HERSHEY_SIMPLEX, 1, WHITE, 2, cv2.LINE_AA)
    return image

def process_frame(frame, pose):
    height, width, _ = frame.shape
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results, height, width

def extract_landmarks(results):
    try:
        landmarks = results.pose_landmarks.landmark
        hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
               landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        return hip, knee, ankle
    except:
        return None, None, None

def calculate_and_display_angle(hip, knee, ankle, stage, counter):
    if hip and knee and ankle:
        angle = calculate_angle(hip, knee, ankle)
        if angle > 170:  # Standing position (hips and knees extended)
            stage = "up"
        if angle < 145 and stage == 'up':  # Bent position (hips and knees flexed)
            stage = "down"
            counter += 1
        return angle, stage, counter
    return None, stage, counter


def render_ui(image, counter, stage, angle, width):
    angle_max = 178
    angle_min = 25
    # Title and Background
    cv2.rectangle(image, (int(width / 2) - 150, 0), (int(width / 2) + 250, 73), BLUE, -1)
    cv2.putText(image, 'AI Workout Manager', (int(width / 2) - 100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, WHITE, 2,
                cv2.LINE_AA)

    # Reps
    cv2.rectangle(image, (0, 0), (255, 73), BLUE, -1)
    cv2.putText(image, 'REPS', (15, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1, cv2.LINE_AA)
    cv2.putText(image, str(counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, WHITE, 2, cv2.LINE_AA)

    # Stage
    cv2.putText(image, 'STAGE', (95, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1, cv2.LINE_AA)
    cv2.putText(image, stage, (95, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, WHITE, 2, cv2.LINE_AA)

    # Progress Bar
    if angle is not None:
        progress = ((angle - angle_min) / (angle_max - angle_min)) * 100
        cv2.rectangle(image, (50, 350), (50 + int(progress * 2), 370), GREEN, cv2.FILLED)
        cv2.rectangle(image, (50, 350), (250, 370), WHITE, 2)
        cv2.putText(image, f'{int(progress)}%', (50, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, WHITE, 2, cv2.LINE_AA)

    # Angle Calculation
    if angle is not None:
        cv2.rectangle(image, (10, 90), (150, 120), WHITE, -1)
        cv2.putText(image, f'ANGLE: {int(angle)}', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, GREEN, 2, cv2.LINE_AA)

    return image


def run_pose_detection(mp_drawing, mp_pose, filename):
    counter = 0
    stage = None
    cap = cv2.VideoCapture(filename)
    start_time = time.time()
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            image, results, height, width = process_frame(frame, pose)
            hip, knee, ankle = extract_landmarks(results)
            angle, stage, counter = calculate_and_display_angle(hip, knee, ankle, stage, counter)
            image = render_ui(image, counter, stage, angle, width)
            image = display_clock_icon(image, 'assets/clock.png', height, width)
            image = display_time(image, start_time, height, width)
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=5),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=5))
            cv2.imshow('AI Workout Manager', image)
            if cv2.waitKey(10) & 0xFF == ord('c'):
                break
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    run_pose_detection(mp_drawing, mp_pose, 'assets/deadlift.mp4')
