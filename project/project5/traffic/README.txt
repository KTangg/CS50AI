Version 1.00

    # Create Sequential Model
    model = keras.Sequential(
    [
        # Input layer
        keras.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3)),

        # 1-ST CONVOLUTION and POOLING
        layers.Conv2D(32, 7, activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),

        # 2-ND CONVOLUTION and POOLING
        layers.Conv2D(32, 3, activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),


        # Flatten
        layers.Flatten(),

        # Hidden Layers with Dropout
        layers.Dense(256, activation="relu"),
        layers.Dense(256, activation="relu"),
        layers.Dense(256, activation="relu"),
        layers.Dense(256, activation="relu"),
        layers.Dropout(0.5),

        # Softmax Layers 
        layers.Dense(NUM_CATEGORIES, activation="softmax", name="output"),
    ]
    )

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=['accuracy', 'mse']
    )

Small-Data Accuracy: 100%
Large-Data Accuracy: 92.91%

Summary: Seem Good And Stable

Version 1.01

- Add
    layers.Conv2D(32, 5, activation="relu"),
    layers.MaxPooling2D(pool_size=(2, 2)),

Accuracy: 87.34%

Summary: Doesn't help

Version 1.02

- Change
    # 1-ST CONVOLUTION and POOLING
    layers.Conv2D(32, 7, activation="relu"),
    layers.Conv2D(32, 5, activation="relu"),
    layers.MaxPooling2D(pool_size=(2, 2)),


    # 2-ND CONVOLUTION and POOLING
    layers.Conv2D(32, 3, activation="relu"),
    layers.MaxPooling2D(pool_size=(2, 2)),

Accuracy: 95.77%

Summary: Slightly Change

Version 1.03

- Change

    # 1-ST CONVOLUTION and POOLING
    layers.Conv2D(32, 3, activation="relu"),
    layers.Conv2D(32, 3, activation="relu"),
    layers.MaxPooling2D(pool_size=(2, 2)),


    # 2-ND CONVOLUTION and POOLING
    layers.Conv2D(32, 3, activation="relu"),
    layers.MaxPooling2D(pool_size=(2, 2)),

Accuracy: 95.47%

Summary: Slightly Change

Version 1.04

- Using AveragePooling Instead

Accuracy: 97.30%

Summary: Significant Change

Version 1.05

- Using MaxPooling altenative with AveragePooling

    # 1-ST CONVOLUTION and POOLING
    layers.Conv2D(32, 3, activation="relu"),
    layers.Conv2D(32, 3, activation="relu"),
    layers.MaxPooling2D(pool_size=(2, 2)),


    # 2-ND CONVOLUTION and POOLING
    layers.Conv2D(32, 3, activation="relu"),
    layers.AveragePooling2D(pool_size=(2, 2)),

Accuracy: 98.40%

Version 1.06

- Using 512 Dense Layers

Accuracy: 96.57%

Summary No Significant Change
