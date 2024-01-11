#******make sure env is python 3.10 not 3.9******

#source venv/bin/activate
#pip install tensorflow
#pip install keras-retinanet
#pip install opencv-python
#pip install matplotlib
#run
#python find_wally.py images/36.jpg
import numpy as np
import cv2
import os
import sys
import random
import tensorflow as tf
import keras
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
import matplotlib.pyplot as plt

def get_session():
    config = tf.compat.v1.ConfigProto()
    config.gpu_options.allow_growth = True
    return tf.compat.v1.Session(config=config)

tf.compat.v1.keras.backend.set_session(get_session())

try:
    model_path = "weights.h5"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file '{model_path}' not found.")

    model = models.load_model(model_path, backbone_name='resnet50')
except Exception as e:
    print(f"Error loading model: {e}")
    sys.exit(1)

try:
    sys_args = sys.argv
    if len(sys_args) > 1:
        image_files = sys.argv[1:]
    else:
        images_dir = './images'
        test_images_dir = './test_images'
        if not os.path.exists(images_dir) or not os.path.exists(test_images_dir):
            raise FileNotFoundError("Images directory not found.")

        image_files = [os.path.join(images_dir, random.choice(os.listdir(images_dir))), 
                       os.path.join(test_images_dir, random.choice(os.listdir(test_images_dir)))]

    for image_path in image_files:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file '{image_path}' not found.")

        image = read_image_bgr(image_path)
        draw = image.copy()
        draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)

        image = preprocess_image(image)
        image, scale = resize_image(image, min_side=1800, max_side=3000)

        boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))
        boxes /= scale

        for box, score, label in zip(boxes[0], scores[0], labels[0]):
            if score < 0.5:
                break

            b = box.astype(int)
            b += np.array([-(b[2] - b[0]) // 4, -(b[3] - b[1]) // 4, (b[2] - b[0]) // 4, (b[3] - b[1]) // 4])
            cv2.rectangle(draw, (b[0], b[1]), (b[2], b[3]), (255, 0, 0), 10)

        fig = plt.figure()
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        fig.add_axes(ax)

        ax.imshow(draw, alpha=0.5)
        plt.axis('off')
        plt.show()
        plt.close()

except Exception as e:
    print(f"Error processing images: {e}")
    sys.exit(1)

print("Processing completed successfully.")
