from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Activation, MaxPool2D, Flatten, Dense, Dropout


class SudokuNet():
    @staticmethod
    def build(width, height, depth, num_classes):
        model = Sequential()
        input_shape = (width, height, depth)

        # first layer with Conv2D => Relu => Max Pooling
        model.add(Conv2D(32, (5, 5), padding='same', input_shape=input_shape))
        model.add(Activation('relu'))
        model.add(MaxPool2D(pool_size=(2, 2)))

        # second layer
        model.add(Conv2D(32, (3, 3), padding='same'))
        model.add(Activation('relu'))
        model.add(MaxPool2D(pool_size=(2, 2)))

        # first fully-connected layer
        model.add(Flatten())
        model.add(Dense(64))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))

        # second fully-connected layer
        model.add(Dense(64))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))

        # softmax classifier
        model.add(Dense(num_classes))
        model.add(Activation('softmax'))

        return model


class SudokuNet2():
    @staticmethod
    def build(width, height, depth, num_classes):
        model = Sequential()
        input_shape = (width, height, depth)

        # first conv layer
        model.add(Conv2D(254, kernel_size=(3, 3), input_shape=input_shape))
        model.add(MaxPool2D(2, 2))

        # second conv layer
        model.add(Conv2D(128, kernel_size=(3, 3)))
        model.add(MaxPool2D(2, 2))

        # convert 2D input to 1D vectors
        model.add(Flatten())

        model.add(Dense(140, activation='relu'))
        model.add(Dropout(0.2))

        model.add(Dense(80, activation='relu'))
        model.add(Dropout(0.2))

        model.add(Dense(units=10, activation='sigmoid'))

        return model
