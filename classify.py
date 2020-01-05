import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img, img_to_array

global graph
graph = tf.compat.v1.get_default_graph

model = tf.keras.models.load_model('eatingWithoutTFHubModel.h5')

model.compile(optimizer='adam', loss='binary_crossentropy',
              metrics=['accuracy'])

eatingCounter = 0


def predict(filename):
    img = load_img('/tmp/image_classification_files/1573399085.jpg', target_size=(150, 250))
    img_tensor = img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.

    with graph.as_default():
        prediction = model.predict(img_tensor)
    
    if(prediction.item() < 0.5):
        print('eating')
        return 200
    else:
        print('not eating')
        return 400
    #     eatingCounter = eatingCounter + 1

    # if(eatingCounter == 10):
    #     returnValue = '201'

    # if(eatingCounter > 10):
    #     eatingCounter = 0
    # return returnValue

# predict('/tmp/image_classification_files/1573399085.jpg')