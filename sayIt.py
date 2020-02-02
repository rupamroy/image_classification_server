from gtts import gTTS
import subprocess
import os

def say(val):
    try:
        os.remove('announce.mp3')
    except Exception as ex:
        print(ex)

    try:
        tts = gTTS(val)
    except Exception as e:
            print("Failed to generate speech from text")
            exit(e)
    else: #if no exception then save the file
            tts.save('announce.mp3')
            subprocess.Popen(['mpg123', '-q', '{}/announce.mp3'.format(os.getcwd())]).wait()
