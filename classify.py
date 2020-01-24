import tensorflow as tf
import numpy as np
import threading
from datetime import datetime
import csv
import os
import subprocess
import shutil
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img, img_to_array

model = tf.keras.models.load_model('eatingWithoutTFHubModel.h5')

model.compile(optimizer='adam', loss='binary_crossentropy',
              metrics=['accuracy'])

alarmRangDate = datetime.today().date()

eatingCounter = 0
classList = [None] * 10

lock = threading.Lock()


def predict(filename):
    global eatingCounter
    global classList
    img = load_img(filename, target_size=(150, 250))
    img_tensor = img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.
    justFileName = os.path.basename(filename)

    prediction = model.predict(img_tensor)

    with lock:
        with open('log_file.csv', mode='a') as log_file:
            log_writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            now = datetime.now()

            toPrintDate = now.strftime("%Y-%m-%d")
            toPrintTime = now.strftime("%H:%M:%S")

            if(prediction.item() < 0.5):
                log_writer.writerow([toPrintDate, toPrintTime, 'Eating',classList])
                shutil.move(filename, '/home/rupam/dev/eating-classification/classes/stg_eating/{}'.format(justFileName))
                classList[eatingCounter]=1
            else:
                log_writer.writerow([toPrintDate, toPrintTime, 'Not Eating', classList])
                shutil.move(filename, '/home/rupam/dev/eating-classification/classes/stg_other/{}'.format(justFileName))
                classList[eatingCounter] = 0

            alert(classList)

            eatingCounter = eatingCounter + 1
            print('counter: {}'.format(eatingCounter))
            if(eatingCounter == 10):
                eatingCounter = 0
            return 200


def alert(classList):
    global alarmRangDate
    isTrueEating =  list(filter(lambda x: x == 1, classList))
    hasAlreadyRangForToday = True if (alarmRangDate != datetime.today().date()) else False
    if(hasAlreadyRangForToday and (len(isTrueEating) > 6)):
        alarmRangDate = datetime.today().date()
        log('Alert sound............')
        log('classList={}'.format(classList))
        log('isTrueEating={}'.format(isTrueEating))
        play_mp3()

def play_mp3():
    path = '/home/rupam/Music/medicineAlert.mp3'
    subprocess.Popen(['mpg123', '-q', path]).wait()

def log(log):
     with open('log.csv', mode='a') as log_file:
            log_writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            log_writer.writerow(log)