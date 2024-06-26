from keras import layers, losses
from keras.models import Sequential, load_model
import tensorflow as tf
from .parameters import img_height, img_width
import os

def create_and_train_model(train_ds: tf.data.Dataset, val_ds: tf.data.Dataset, class_names):
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
              loss=losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
  
  # Train the model with 10 epochs (train 10 times)
  epochs = 10
  model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs
  )

  return model

# Create or load the model from the saved folder
def create_or_load_model(train_ds, val_ds, class_names):
    route = "cnn/model/saved/model.keras"
    folder = "cnn/model/saved"
    exists = os.path.isfile(route)

    if(exists):
      model = load_model(filepath=route, compile=True)
    else:
      if not os.path.exists(folder):
        os.mkdir(folder)
      model: Sequential = create_and_train_model(train_ds, val_ds, class_names)
      model.save(route)
    return model