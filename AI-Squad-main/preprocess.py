import os
import cv2

def preprocess_images(image_dir, output_dir, img_size=(128, 128)):
    os.makedirs(output_dir, exist_ok=True)
    for img_name in os.listdir(image_dir):
        img_path = os.path.join(image_dir, img_name)
        img = cv2.imread(img_path)
        if img is not None:
            img_resized = cv2.resize(img, img_size)
            cv2.imwrite(os.path.join(output_dir, img_name), img_resized)

preprocess_images('/home/aniket-workstation/TrueSight/dataset/real', '/home/aniket-workstation/TrueSight/processed/real', img_size=(224, 224))
preprocess_images('/home/aniket-workstation/TrueSight/dataset/fake', '/home/aniket-workstation/TrueSight/processed/fake', img_size=(224, 224))
