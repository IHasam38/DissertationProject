import face_recognition

image = face_recognition.load_image_file("faces/Hassan.jpg")

faces = face_recognition.face_locations(
    image,
    number_of_times_to_upsample=2,
    model="hog"
)

print(faces)
print("Faces found:", len(faces))