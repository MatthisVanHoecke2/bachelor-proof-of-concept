from keras import layers
from keras.models import Sequential
import tensorflow as tf
from .parameters import img_height, img_width

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