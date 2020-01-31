# from https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/examples/python/label_image.py

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse

import numpy as np

from PIL import Image

import tensorflow as tf # TF2


def load_labels(filename):
  with open(filename, 'r') as f:
    return [line.strip() for line in f.readlines()]


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '-i',
      '--image',
      default='/home/rupam/dev/eating_verification/classes/other/1573387056.jpg',
      help='image to be classified')
  parser.add_argument(
      '-m',
      '--model_file',
      default='/home/rupam/dev/image_classification_server/models/mobilenet/detect.tflite',
      help='.tflite model to be executed')
  parser.add_argument(
      '-l',
      '--label_file',
      default='/home/rupam/dev/image_classification_server/models/mobilenet/labelmap.txt',
      help='name of file containing labels')
  parser.add_argument(
      '--input_mean',
      default=127.5, type=float,
      help='input_mean')
  parser.add_argument(
      '--input_std',
      default=127.5, type=float,
      help='input standard deviation')
  args = parser.parse_args()

  interpreter = tf.lite.Interpreter(model_path=args.model_file)
  interpreter.allocate_tensors()

  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()

  # check the type of the input tensor
  floating_model = input_details[0]['dtype'] == np.float32

  # NxHxWxC, H:1, W:2
  height = input_details[0]['shape'][1]
  width = input_details[0]['shape'][2]
  img = Image.open(args.image).resize((width, height))

  # add N dim
  input_data = np.expand_dims(img, axis=0)

  if floating_model:
    input_data = (np.float32(input_data) - args.input_mean) / args.input_std

  interpreter.set_tensor(input_details[0]['index'], input_data)

  interpreter.invoke()

  output_data = interpreter.get_tensor(output_details[0]['index'])
  results = np.squeeze(output_data)

  top_k = results.argsort()[-5:][::-1]
  labels = load_labels(args.label_file)

  print(top_k)
  for i in top_k:
    if floating_model:
      print('{:08.6f}: {}'.format(float(results[i]), labels[i]))
    else:
      #print('{:08.6f}: {}'.format(float(results[i] / 255.0), labels[i]))
      print(labels[i])