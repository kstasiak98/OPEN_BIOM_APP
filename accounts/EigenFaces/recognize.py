import os
import cv2
import numpy as np
from accounts.EigenFaces.image_encrypt import encrypt, decrypt

PASSWORD = 'Test'

def detect_faces(img):
    width_d, height_d = 280, 280 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    face_cascade = cv2.CascadeClassifier('opencv-files/lbpcascade_frontalface.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);
    
    if (len(faces) == 0):
        return [None, None]
    
    results = []
    for f in faces:
        (x, y, w, h) = f
        results.append([cv2.resize(gray[y:y+w, x:x+h], (width_d, height_d)), f])
    
    return results


def predict(face_recognizer, img):
    img_cp = img.copy()
    detected = detect_faces(img_cp)

    results = []
    for d in detected:
        if len(d) > 0:
            results.append(face_recognizer.predict(d[0]))
            cv2.imshow(str(results[-1]), d[0])
            cv2.waitKey(5000)
    
    return results


def predict_user(user_id, img):
    # face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer = cv2.face.EigenFaceRecognizer_create()
    vector_enc_path = f'trained_data/u{user_id}_enc.txt'
    vector_dec_path = decrypt(vector_enc_path, PASSWORD)

    face_recognizer.read(vector_dec_path)
    predictions = predict(face_recognizer, img)
    os.remove(vector_dec_path)
    return predictions

if __name__ == '__main__':
    # test_img = cv2.imread("test1.jpg")
    # print(predict_user(1, test_img))
    test_img2 = cv2.imread("test3.jpg")
    print(predict_user(1, test_img2))
    # test_img3 = cv2.imread("test3.jpg")
    # print(predict_user(1, test_img3))