import cv2
import os
import numpy as np

dataset_path = "dataset"

recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []

label_ids = {}
current_id = 0

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

for person_name in os.listdir(dataset_path):

    person_path = os.path.join(
        dataset_path,
        person_name
    )

    if not os.path.isdir(person_path):
        continue

    label_ids[current_id] = person_name

    for image_name in os.listdir(person_path):

        image_path = os.path.join(
            person_path,
            image_name
        )

        image = cv2.imread(
            image_path,
            cv2.IMREAD_GRAYSCALE
        )

        if image is None:
            continue

        faces.append(image)
        labels.append(current_id)

    current_id += 1

recognizer.train(
    faces,
    np.array(labels)
)

recognizer.save("trainer.yml")

with open("labels.txt", "w") as f:

    for label_id, name in label_ids.items():

        f.write(
            f"{label_id},{name}\n"
        )

print("Training completed.")
print("Model saved as trainer.yml")