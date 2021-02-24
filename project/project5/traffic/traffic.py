import cv2
import numpy as np
import os
import sys
import pydotplus
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )
    

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    # Create images list
    images = []
    labels = []
    # Loop for every category
    for ctg_dir in range(NUM_CATEGORIES):
        label = ctg_dir
        ctg_dir = str(ctg_dir)
        # Open Categories
        with os.scandir(os.path.join(data_dir, ctg_dir)) as ctg:
            for entry in ctg:
                # Open Image
                img = cv2.imread(os.path.join(data_dir, ctg_dir, entry.name))
                # Resize Image
                dim = (IMG_WIDTH, IMG_HEIGHT)
                img = cv2.resize(img, dim)

                # Add to images list and labels list
                images.append(img)
                labels.append(label)

    print(f"Data Type: {type(images[0])}")
    print(f"Resize Image to: {len(images[0])} X {len(images[0][0])} X {len(images[0][0][0])}")
    print("Data Loaded")

    return (images, labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    
    # Create Sequential Model
    model = keras.Sequential(
    [
        # Input layer
        keras.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3)),

        # 1-ST CONVOLUTION and POOLING
        layers.Conv2D(32, 3, activation="relu"),
        layers.Conv2D(32, 3, activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),

        # 2-ND CONVOLUTION and POOLING
        layers.Conv2D(32, 3, activation="relu"),
        layers.AveragePooling2D(pool_size=(2, 2)),

        # Flatten
        layers.Flatten(),

        # Hidden Layers with Dropout
        layers.Dense(256, activation="relu"),
        layers.Dropout(0.2),
        layers.Dense(256, activation="relu"),
        layers.Dropout(0.2),
        layers.Dense(256, activation="relu"),
        layers.Dropout(0.2),
        layers.Dense(256, activation="relu"),
        layers.Dropout(0.2),

        # Softmax Layers 
        layers.Dense(NUM_CATEGORIES, activation="softmax", name="output"),
    ]
    )

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=['accuracy', 'mse']
    )

    return model




if __name__ == "__main__":
    main()