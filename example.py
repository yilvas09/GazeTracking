"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2, pyautogui
from gaze_tracking import GazeTracking
pyautogui.FAILSAFE = False

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

    scalor = 20; # scale positional change in pupils
    min_change = 3; # ignore tiny changes
    
    # prev_mid_pupil = (int(cam / 2) for cam in cam_size)
    prev_mid_pupil = None

    while True and webcam is not None:
        # We get a new frame from the webcam
        _, frame = webcam.read()
        frame = cv2.flip(frame, 1)

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

        # use positional changes of pupils to control mouse cursor
        if left_pupil is not None and right_pupil is not None:
            mid_pupil = tuple(int((l + r) / 2) for l, r in zip(left_pupil, right_pupil))
            if prev_mid_pupil is None:
                prev_mid_pupil = mid_pupil
            else:
                change_pupil = tuple((n - o) * (abs(n - o) >= min_change) for n, o in zip(mid_pupil, prev_mid_pupil))
                # change_screen = tuple(ch / cam * scr for ch, cam, scr in zip(change_pupil, cam_size, screen_size))
                change_screen = tuple(scalor * c for c in change_pupil)
                # print("mid:")
                # print(mid_pupil)
                # print("prev_mid")
                # print(prev_mid_pupil)
                # print(pyautogui.position())
                # print("changes:")
                # print(change_pupil)
                # print(change_screen)
                # print('=====')
                pyautogui.moveRel(change_screen, duration=0.1)
                prev_mid_pupil = mid_pupil


        cv2.imshow("Demo", frame)

        if cv2.waitKey(1) == 27:
            # print(pyautogui.position())
            break
    
    webcam.release()
    cv2.destroyAllWindows()
