
import cv2
import os
import time

person_name = input("Enter resident name: ")

save_path = f"dataset/{person_name}"
os.makedirs(save_path, exist_ok=True)

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

instructions = [
    "Look Forward",
    "Turn Left",
    "Turn Right",
    "Look Up",
    "Look Down"
]

image_count = 0

for instruction in instructions:

    print(f"\n{instruction}")
    print("Capturing in 3 seconds...")

    start_time = time.time()

    while time.time() - start_time < 3:

        ret, frame = cap.read()

        if not ret:
            continue

        cv2.putText(
            frame,
            instruction,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        countdown = 3 - int(time.time() - start_time)

        cv2.putText(
            frame,
            f"Capture in: {countdown}",
            (20, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow(
            "Resident Registration",
            frame
        )

        cv2.waitKey(1)

    ret, frame = cap.read()

    if not ret:
        continue

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_detector.detectMultiScale(
        gray,
        1.1,
        5
    )

    if len(faces) > 0:

        x, y, w, h = faces[0]

        face_img = gray[
            y:y+h,
            x:x+w
        ]

        image_count += 1

        cv2.imwrite(
            f"{save_path}/{image_count}.jpg",
            face_img
        )

        print(f"Captured image {image_count}")

cap.release()
cv2.destroyAllWindows()

print(
    f"Registration complete. "
    f"{image_count} images saved."
)