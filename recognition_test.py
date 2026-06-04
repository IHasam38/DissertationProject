import cv2

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

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

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

                name = labels[label_id]

                text = f"{name}"

            else:

                text = "Unknown Person"

        except:

            text = "Unknown Person"

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            text,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow(
        "Face Recognition Test",
        frame
    )

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()