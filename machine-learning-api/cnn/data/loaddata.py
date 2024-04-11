import numpy as np
import tensorflow as tf

from keras import utils
from .parameters import batch_size, img_height, img_width
import pathlib

def __load_training_data():
  # download the flowers dataset into the keras cache directory '~/.keras'
  dataset_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
  data_dir = utils.get_file('flower_photos.tar', origin=dataset_url, extract=True)
  data_dir = pathlib.Path(data_dir).with_suffix('')
  return data_dir

# According to the TensorFlow tutorial, it's good practice to split the dataset into smaller datasets for training and validating
def __validation_split():
  data_dir = __load_training_data() # Load the data directory

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

def __configure_dataset_performance(train_ds: tf.data.Dataset, val_ds: tf.data.Dataset):
  AUTOTUNE = tf.data.AUTOTUNE
  # Cache the datasets to keep the images in memory after being loaded off disk
  # Shuffle the training dataset to get a more representative datasample in each batch
  # Prefetching allows faster training execution by performing multiple tasks at once, while executing training step 'i' the data for step 'i+1' will be read by the input pipeline
  train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
  val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

  return train_ds, val_ds

def load_dataset():
  train_ds, val_ds, class_names = __validation_split()
  train_ds, val_ds = __configure_dataset_performance(train_ds, val_ds)
  return train_ds, val_ds, class_names