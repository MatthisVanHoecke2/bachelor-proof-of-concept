import numpy as np
import tensorflow as tf

from keras import layers, utils
from keras.models import Sequential
import pathlib

# Define parameters
batch_size = 32
img_height = 180
img_width = 180

def load_training_data():
  # download the flowers dataset into the keras cache directory '~/.keras'
  dataset_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
  data_dir = utils.get_file('flower_photos.tar', origin=dataset_url, extract=True)
  data_dir = pathlib.Path(data_dir).with_suffix('')
  return data_dir

# According to the TensorFlow tutorial, it's good practice to split the dataset into smaller datasets for training and validating
def validation_split():
  data_dir = load_training_data() # Load the data directory

  # Create the training dataset
  train_ds = utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2, # Assign 80% of data for training
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

  class_names = train_ds.class_names

  # Create the validation dataset
  val_ds = utils.image_dataset_from_directory(
  data_dir,
  validation_split=0.2, # Assign 20% of data for validating
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

  return train_ds, val_ds, class_names

def configure_dataset_performance(train_ds: tf.data.Dataset, val_ds: tf.data.Dataset):
  AUTOTUNE = tf.data.AUTOTUNE
  # Cache the datasets to keep the images in memory after being loaded off disk
  # Shuffle the training dataset to get a more representative datasample in each batch
  # Prefetching allows faster training execution by performing multiple tasks at once, while executing training step 'i' the data for step 'i+1' will be read by the input pipeline
  train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
  val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

  return train_ds, val_ds

def create_model(train_ds: tf.data.Dataset, val_ds: tf.data.Dataset, class_names):
  num_classes = len(class_names)

  # Create the model by stacking convolution layers
  model = Sequential([
    layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes)
  ])

  # Compile the model
  model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
  
  # Train the model with 10 epochs (train 10 times)
  epochs = 10
  model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs
  )
  return model


def predict_data(model: Sequential, class_names):
  # Load image to classify
  sunflower_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/592px-Red_sunflower.jpg"
  sunflower_path = utils.get_file('Red_sunflower', origin=sunflower_url)

  img = utils.load_img(
      sunflower_path, target_size=(img_height, img_width)
  )
  img_array = utils.img_to_array(img)
  img_array = tf.expand_dims(img_array, 0) # Create a batch

  predictions = model.predict(img_array) # Classify the image
  score = tf.nn.softmax(predictions[0]) # Calculate confidence score

  print(
      "This image most likely belongs to {} with a {:.2f} percent confidence."
      .format(class_names[np.argmax(score)], 100 * np.max(score))
  )

def run_model():
  train_ds, val_ds, class_names = validation_split()
  train_ds, val_ds = configure_dataset_performance(train_ds, val_ds)
  model = create_model(train_ds, val_ds, class_names)
  predict_data(model, class_names)

run_model()