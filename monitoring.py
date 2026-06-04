from playsound import playsound
from ultralytics import YOLO
import cv2
import os
import time
import threading
from datetime import datetime

# -----------------------------
# AUDIO
# -----------------------------
def play_audio(audio_file):

    threading.Thread(
        target=playsound,
        args=(audio_file,),
        daemon=True
    ).start()

# -----------------------------
# EVENT LOG
# -----------------------------
def log_event(event_text):

    with open("event_log.txt", "a") as log_file:
        log_file.write(event_text + "\n")

# -----------------------------
# LOAD YOLO
# -----------------------------
model = YOLO("yolov8n.pt")

# -----------------------------
# LOAD FACE RECOGNITION
# -----------------------------
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

labels = {}

with open("labels.txt", "r") as f:

    for line in f:

        label_id, name = line.strip().split(",")

        labels[int(label_id)] = name

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# -----------------------------
# CAMERA
# -----------------------------
cap = cv2.VideoCapture(0)

# -----------------------------
# SCREENSHOTS
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
    resident_name = "Unknown"

    display_frame = frame.copy()

    # -----------------------------
    # FACE RECOGNITION
    # -----------------------------
    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_cascade.detectMultiScale(
        gray,
        1.1,
        5
    )

    for (x, y, w, h) in faces:

        face_img = gray[y:y+h, x:x+w]

        try:

            label_id, confidence = recognizer.predict(
                face_img
            )

            if confidence < 80:

                resident_name = labels[label_id]

                color = (0, 255, 0)

            else:

                resident_name = "Unknown Person"

                color = (0, 0, 255)

        except:

            resident_name = "Unknown Person"

            color = (0, 0, 255)

        cv2.rectangle(
            display_frame,
            (x, y),
            (x+w, y+h),
            color,
            2
        )

        cv2.putText(
            display_frame,
            resident_name,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

    # -----------------------------
    # YOLO DETECTION
    # -----------------------------
    results = model(frame, conf=0.7)

    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])

            if class_id == 0:

                person_detected = True

                last_person_seen = time.time()

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                width = x2 - x1
                height = y2 - y1

                fallen = width > height

                cv2.rectangle(
                    display_frame,
                    (x1, y1),
                    (x2, y2),
                    (255, 255, 0),
                    2
                )

                if fallen:

                    fall_detected = True

                    cv2.putText(
                        display_frame,
                        "FALL DETECTED!",
                        (x1, y1 - 35),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (0, 0, 255),
                        2
                    )

    # -----------------------------
    # ALERTS
    # -----------------------------
    current_time = time.time()

    if current_time - last_voice_time > VOICE_DELAY:

        if fall_detected:

            print("Fall detected")

            play_audio(
                "Sound recordings/fall detection.mp3"
            )

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            filename = (
                f"screenshots/fall_{timestamp}.jpg"
            )

            cv2.imwrite(
                filename,
                display_frame
            )

            log_event(
                f"{datetime.now()} - FALL DETECTED - {filename}"
            )

        elif person_detected:

            print(
                f"Resident: {resident_name}"
            )

        else:

            if current_time - last_person_seen > 3:

                play_audio(
                    "Sound recordings/no person.mp3"
                )

        last_voice_time = current_time

    # -----------------------------
    # STATUS
    # -----------------------------
    cv2.putText(
        display_frame,
        f"Resident: {resident_name}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    # -----------------------------
    # SHOW WINDOW
    # -----------------------------
    cv2.imshow(
        "Smart Home Guardian",
        display_frame
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# -----------------------------
# CLEANUP
# -----------------------------
cap.release()
cv2.destroyAllWindows()