import tensorflow as tf
from PIL import Image
import numpy as np
import os

dataset_dir = 'D:\\PycharmProjects\\Mind\\mind_dataset\\'
train_dir = os.listdir(dataset_dir)

train_images = []
train_labels = []
test_images = []
test_labels = []

val_split = 0.1

for a, dir in enumerate(train_dir):
    whatsin = os.listdir(dataset_dir+dir)
    count = 0
    split_point = int(round(len(whatsin)*(1-val_split)))
    for image_name in whatsin:
        image = Image.open(dataset_dir+dir+'\\'+image_name).convert('RGB')
        image = image.resize((100, 100))
        image = np.array(image)

        label = np.zeros(len(train_dir))
        label[a] = 1

        count += 1
        if count > split_point:
            test_images.append(image)
            test_labels.append(label)
        else:
            train_images.append(image)
            train_labels.append(label)

train_images = np.asarray(train_images)
train_images = np.reshape(train_images, [train_images.shape[0], 100, 100, 3])

train_labels = np.asarray(train_labels)

test_images = np.asarray(test_images)
test_images = np.reshape(test_images, [test_images.shape[0], 100, 100, 3])

test_labels = np.asarray(test_labels)

network = [
    tf.keras.layers.Conv2D(32, (3, 3), input_shape=(100, 100, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(len(train_dir), activation='softmax')
]

model = tf.keras.Sequential(network)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x=train_images, y=train_labels, validation_data=(test_images, test_labels), epochs=10)

model.save('./Mind_model')

converter = tf.lite.TFLiteConverter.from_saved_model('./Mind_model')
tflite_model = converter.convert()

with open('./mind_AI.tflite', 'wb') as f:
    f.write(tflite_model)