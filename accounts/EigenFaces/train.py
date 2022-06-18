import os
import cv2
import numpy as np
from image_encrypt import encrypt, decrypt

PATH = 'Images'
PASSWORD = 'Test'

def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('opencv-files/lbpcascade_frontalface.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);
    
    if (len(faces) == 0):
        return None, None
    (x, y, w, h) = faces[0]
    
    return gray[y:y+w, x:x+h], faces[0]


def train(model):
    # subject_dir_path = PATH + "/u" + str(model)
    subject_dir_path = f"{PATH}/u{model}"
    subject_images_names = os.listdir(subject_dir_path)

    faces = []
    labels = []
    label = model

    for image_name in subject_images_names:
        if image_name.endswith('_enc.txt'):
            image_path = subject_dir_path + "/" + image_name
            # encrypt(image_path, PASSWORD)
            decrypted_path = decrypt(image_path, PASSWORD)
            image = cv2.imread(decrypted_path)
            
            face, rect = detect_face(image)
            
            if face is not None:
                faces.append(face)
                labels.append(label)

            os.remove(decrypted_path)
    
    return faces, labels


def train_and_save(user_id):
    faces, labels = train(user_id)

    width_d, height_d = 280, 280
    resized = [cv2.resize(face, (width_d, height_d)) for face in faces]

    # face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer = cv2.face.EigenFaceRecognizer_create()
    face_recognizer.train(resized, np.array(labels))

    vector_path = f'trained_data/u{user_id}.txt'
    face_recognizer.write(vector_path)
    encrypt(vector_path, PASSWORD)
    os.remove(vector_path)


if __name__ == '__main__':
    train_and_save(1)
    train_and_save(2)