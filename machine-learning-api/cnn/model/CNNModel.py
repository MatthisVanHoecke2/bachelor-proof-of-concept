from cnn.data.loaddata import load_dataset
from cnn.data.createmodel import create_model
from fastapi import UploadFile
from keras import utils
from keras.models import Sequential
import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
from cnn.data.parameters import img_height, img_width

class CNNModel():
  def __init__(self):
    train_ds, val_ds, class_names = load_dataset()
    self.class_names = class_names
    self.model: Sequential = create_model(train_ds, val_ds, class_names)

  def get_class_names(self):
    return self.class_names

  def predict_data(self, image: UploadFile):
    img = Image.open(image.file)
    img_array = utils.img_to_array(img)
    img_array = tf.image.resize_with_pad(img_array, target_height=img_height, target_width=img_width)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = self.model.predict(img_array) # Classify the image
    score = tf.nn.softmax(predictions[0]) # Calculate confidence score

    return {"prediction": self.class_names[np.argmax(score)], "confidence": 100 * np.max(score)}