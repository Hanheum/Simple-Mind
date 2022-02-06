import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_saved_model('./Mind_model')
tflite_model = converter.convert()

with open('./mind_AI.tflite', 'wb') as f:
    f.write(tflite_model)