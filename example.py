"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking

def find_video_id(id_start, id_end):
    for i in range(id_start, id_end):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                return i
            cap.release()
    return None

if __name__ == '__main__':

    gaze = GazeTracking()
    webcam_id = find_video_id(0,5)
    webcam = cv2.VideoCapture(webcam_id) if webcam_id is not None else None

    while True and webcam is not None:
        # We get a new frame from the webcam
        _, frame = webcam.read()

        # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text = ""

        if gaze.is_blinking():
            text = "Blinking"
        elif gaze.is_right():
            text = "Looking right"
        elif gaze.is_left():
            text = "Looking left"
        elif gaze.is_center():
            text = "Looking center"

        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

        cv2.imshow("Demo", frame)

        if cv2.waitKey(1) == 27:
            break
    
    webcam.release()
    cv2.destroyAllWindows()
