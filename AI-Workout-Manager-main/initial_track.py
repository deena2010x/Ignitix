import cv2
import numpy as np

# Define the function to initialize the tracker
def initialize_tracker():
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return None, None
    # Read the first frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        return None, None
    # Define the initial bounding box
    bbox = cv2.selectROI(frame, False)
    return cap, bbox

# Define the function to start tracking
def start_tracking(cap, bbox):
    # Create the tracker object
    tracker = cv2.TrackerCSRT_create()
    # Initialize tracker with the first frame and bounding box
    ret = tracker.init(frame, bbox)
    if not ret:
        print("Error: Could not initialize tracker.")
        return
    while True:
        # Read a new frame
        ret, frame = cap.read()
        if not ret:
            break
        # Update tracker
        ret, bbox = tracker.update(frame)
        if ret:
            # Draw bounding box
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else:
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        # Display result
        cv2.imshow("Tracking", frame)
        # Exit on ESC key or 'c' key
        if cv2.waitKey(1) & 0xFF == 27 or cv2.waitKey(10) & 0xFF == ord('c'):
            break
    cap.release()
    cv2.destroyAllWindows()

# Main function to run the tracking
def main():
    cap, bbox = initialize_tracker()
    if cap and bbox:
        start_tracking(cap, bbox)

if __name__ == "__main__":
    main()
