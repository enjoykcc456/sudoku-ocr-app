import argparse
from network import SudokuNet, SudokuNet2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.datasets import mnist
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import classification_report

import pandas as pd

import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''

ap = argparse.ArgumentParser()
ap.add_argument('-o', '--output', required=True,
                help='model output path')
args = vars(ap.parse_args())

# initialize the intial learning rate, epochs and batch size
INITIAL_LR = 0.001
EPOCHS = 5
BATCH_SIZE = 128

# download the MNIST dataset
print('[INFO] downloading MNIST dataset...')
((train_data, train_labels), (test_data, test_labels)) = mnist.load_data()

# add a channel to the train and test data to indicate them as grayscale
train_data = train_data.reshape((train_data.shape[0], 28, 28, 1))
test_data = test_data.reshape((test_data.shape[0], 28, 28, 1))

# scale/normalize the data to range of 0 - 1
train_data = train_data.astype('float32') / 255.0
test_data = test_data.astype('float32') / 255.0

# convert the integer labels into labels in one hot encoding vector
# e.g. 3 => [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
label_binarizer = LabelBinarizer()
train_labels = label_binarizer.fit_transform(train_labels)
test_labels = label_binarizer.fit_transform(test_labels)

# series = pd.Series(train_labels)
# train_labels = pd.get_dummies(series)

# compile the model
print('[INFO] compiling the model...')
optimizer = Adam(learning_rate=INITIAL_LR)
model = SudokuNet2.build(width=28, height=28, depth=1, num_classes=10)
model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

# train the model
print('[INFO] training the model...')
history = model.fit(x=train_data, y=train_labels,
                    validation_data=(test_data, test_labels),
                    batch_size=BATCH_SIZE,
                    epochs=EPOCHS,
                    verbose=1)

# evaluate the model
print('[INFO] evaluating the model...')
predictions = model.predict(test_data)
classes = [str(i) for i in label_binarizer.classes_]
cls_report = classification_report(y_true=test_labels.argmax(axis=1),
                                   y_pred=predictions.argmax(axis=1),
                                   target_names=classes)
print(cls_report)

# save the model
print('[INFO] saving the model...')
model.save(args['output'], save_format='h5')
