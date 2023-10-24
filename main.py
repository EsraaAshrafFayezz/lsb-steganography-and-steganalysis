import os
import shutil
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


model = load_model('path_to_pretrained_steganalysis_model.h5')

def is_message_hidden(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0

    prediction = model.predict(img)
    return prediction[0][0] > 0.5  # Assuming the model output > 0.5 indicates a hidden message

def steganalysis(dataset_folder):
    with_message_folder = os.path.join(dataset_folder, 'with_message')
    without_message_folder = os.path.join(dataset_folder, 'without_message')

    os.makedirs(with_message_folder, exist_ok=True)
    os.makedirs(without_message_folder, exist_ok=True)

    for filename in os.listdir(dataset_folder):
        if filename.endswith(".png"):
            image_path = os.path.join(dataset_folder, filename)
            if is_message_hidden(image_path):
                shutil.move(image_path, os.path.join(with_message_folder, filename))
            else:
                shutil.move(image_path, os.path.join(without_message_folder, filename))

# Provide the path to your dataset folder
dataset_folder = 'dataset'

steganalysis(dataset_folder)
