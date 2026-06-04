from playsound import playsound
from ultralytics import YOLO
import cv2
import os
import time
import threading
from datetime import datetime

# -----------------------------
# AUDIO THREAD FUNCTION
# -----------------------------
def play_audio(audio_file):

    threading.Thread(
        target=playsound,
        args=(audio_file,),
        daemon=True
    ).start()


# -----------------------------
# EVENT LOGGING
# -----------------------------
def log_event(event_text):

    with open("event_log.txt", "a") as log_file:
        log_file.write(event_text + "\n")


# -----------------------------
# LOAD YOLO MODEL
# -----------------------------
model = YOLO("yolov8n.pt")


# -----------------------------
# START CAMERA
# -----------------------------
cap = cv2.VideoCapture(0)


# -----------------------------
# CREATE SCREENSHOTS FOLDER
# -----------------------------
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")


# -----------------------------
# TIMERS
# -----------------------------
last_voice_time = 0
last_person_seen = time.time()

VOICE_DELAY = 5


# -----------------------------
# MAIN LOOP
# -----------------------------
while True:

    ret, frame = cap.read()

    if not ret:
        break

    person_detected = False
    fall_detected = False

    # run YOLO detection
    results = model(frame, conf=0.7)

    display_frame = frame.copy()

    for result in results:

        boxes = result.boxes

        for box in boxes:

            class_id = int(box.cls[0])

            # HUMAN DETECTION ONLY
            if class_id == 0:

                person_detected = True

                # update last seen timer
                last_person_seen = time.time()

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                width = x2 - x1
                height = y2 - y1

                # SIMPLE FALL LOGIC
                fallen = width > height

                # DRAW RECTANGLE
                cv2.rectangle(
                    display_frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                # FALL DETECTION
                if fallen:

                    fall_detected = True

                    cv2.putText(
                        display_frame,
                        "FALL DETECTED!",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (0, 0, 255),
                        2
                    )

                else:

                    cv2.putText(
                        display_frame,
                        "Person Detected",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2
                    )

    current_time = time.time()

    # -----------------------------
    # VOICE ALERTS
    # -----------------------------
    if current_time - last_voice_time > VOICE_DELAY:

        # FALL DETECTED
        if fall_detected:

            print("Fall detected")

            play_audio("Sound recordings/fall detection.mp3")

            # SAVE SCREENSHOT
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            filename = f"screenshots/fall_{timestamp}.jpg"

            cv2.imwrite(filename, display_frame)

            # LOG EVENT
            event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            log_text = f"{event_time} - FALL DETECTED - {filename}"

            log_event(log_text)

        # PERSON DETECTED
        elif person_detected:

            print("Person detected")

            play_audio("Sound recordings/Person detected.mp3")

        # NO PERSON DETECTED
        else:

            # wait before confirming no person
            if current_time - last_person_seen > 3:

                print("No person detected")

                play_audio("Sound recordings/no person.mp3")

        last_voice_time = current_time

    # -----------------------------
    # STATUS DISPLAY
    # -----------------------------
    if person_detected:

        cv2.putText(
            display_frame,
            "Monitoring Active",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )

    else:

        cv2.putText(
            display_frame,
            "No Person Detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

    # -----------------------------
    # SHOW CAMERA WINDOW
    # -----------------------------
    cv2.imshow("Smart Home Guardian", display_frame)

    # PRESS Q TO QUIT
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# -----------------------------
# CLEANUP
# -----------------------------
cap.release()
cv2.destroyAllWindows()