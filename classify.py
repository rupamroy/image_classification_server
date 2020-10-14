import tensorflow as tf
import numpy as np
import threading
from datetime import datetime, timedelta
import time
import csv
import os
import subprocess
import shutil
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import weather

# model = tf.keras.models.load_model('eatingWithoutTFHubModel_3.h5')

# model.compile(optimizer='adam', loss='binary_crossentropy',
#               metrics=['accuracy'])

# alarmRangDate = (datetime.today() - timedelta(1)).date()

# eatingCounter = 0
# classList = [None] * 10

# lock = threading.Lock()


def predict(filename):
    global eatingCounter
    global classList
    img = load_img(filename, target_size=(150, 250))
    img_tensor = img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.
    justFileName = os.path.basename(filename)

    prediction = model.predict(img_tensor)

    now = datetime.now()

    toPrintDate = now.strftime("%Y-%m-%d")
    toPrintTime = now.strftime("%H:%M:%S")

    if(prediction.item() < 0.5):
        start_time = time.time()
        shutil.move(
            filename, '/home/rupam/dev/eating_verification/classes/stg_eating/{}'.format(justFileName))
        print('Move to eating: {}'.format(time.time() - start_time))
        classList[eatingCounter] = 1
        print([toPrintDate, toPrintTime, 'Eating', classList])
    else:
        print([toPrintDate, toPrintTime, 'Not Eating', classList])
        start_time = time.time()
        shutil.move(
            filename, '/home/rupam/dev/eating_verification/classes/stg_other/{}'.format(justFileName))
        print('To move to not eating: {}'.format(time.time() - start_time))
        classList[eatingCounter] = 0

    alert(classList)

    eatingCounter = eatingCounter + 1
    if(eatingCounter == 10):
        eatingCounter = 0
    return 200


def alert(classList):
    global alarmRangDate
    isTrueEating = list(filter(lambda x: x == 1, classList))
    alarmDidNotRingToday = True if (
        alarmRangDate != datetime.today().date()) else False
    if(alarmDidNotRingToday and (len(isTrueEating) > 4)):
        alarmRangDate = datetime.today().date()
        log(['Alert sound............', 'classList=',
             classList, 'isTrueEating=', isTrueEating])
        play_mp3()
        weather.getWeather()


def play_mp3():
    path = '/home/rupam/Music/medicineAlert.mp3'
    subprocess.Popen(['mpg123', '-q', path]).wait()


def log(log):
    with open('log.csv', mode='a') as log_file:
        log_writer = csv.writer(log_file, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        log_writer.writerow(log)

def weekendSpecial():
    weekday = datetime.now().weekday()
    # if sunday or saturday
    weekdayExcuse = True if ( weekday == 5 or weekday == 6) else False
    hour = datetime.now().hour
    hoursOnWeekday = True if (hour >= 7 and hour < 16) else False
    return (weekdayExcuse and hoursOnWeekday)
    
