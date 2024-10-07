# AI Workout Manager

The AI Workout Manager is a pose detection application that uses Python, OpenCV, and MediaPipe to count exercise reps. It's capable of identifying different stages of reps and can calculate angles between various body landmarks during the workout.

## Features

1. Real-time Pose detection.
2. Exercise repetition counting.
3. Visual interface with performance metrics.
4. Elapsed time tracking.
5. Angle Estimation in real time

## Installation

Make sure you have Python 3 installed. Then, clone the repository and install the necessary packages:

```bash
git clone https://github.com/airscholar/AI-Workout-Manager.git](https://github.com/PanduDcau/AI-Workout-Manager.git
cd AI-Workout-Manager
pip install -r requirements.txt
```

## Dependencies

The AI Workout Manager relies on the following libraries:

* OpenCV for image and video processing.
* MediaPipe for pose detection.
* Numpy for numerical operations.
* Math and time libraries from Python's standard library.

## PullUp Work Exercise
### Explanation of Landmarks
1. **Added Check for Landmarks**: In `extract_landmarks`, the function returns `None` for `wrist`, `shoulder`, and `hip` if the landmarks are not found.
2. **Updated `calculate_and_display_angle`**: Added a check to ensure the landmarks are not `None` before calculating the angle.
3. **Conditional Rendering**: Updated `render_ui` to handle `None` angles gracefully.

## Deadlift Exercise
The main movement involves the hip, knee, and ankle. The typical phases are:
1. **Start Position**: Standing upright with the barbell.
2. **Lowering Phase**: Bending the knees and hips to lower the barbell to the ground.
3. **Lifting Phase**: Extending the knees and hips to return to the standing position.


## Usage

You can run the AI Workout Manager by using the following command:

```bash
python main.py
```

## File Structure

The main code is in the root directory:

- `main.py`: The primary script containing the application's logic.

The `assets` directory contains any external assets, like videos or images, that the program uses:

- `pushup.mp4`: An example video file of a person doing pushups.
- `clock.png`: A clock icon used in the UI.


## Contact

If you have any questions or suggestions, please feel free to write me an email at [wpandulap@gmail.com](wpandulap@gmail.com).
