# ---------------------------------
# ---------- Web Imports ----------
# ---------------------------------
from flask import Flask, render_template, request, url_for, jsonify
import time
import datetime
import json

# -----------------------------------------------------------
# ---------- SpeechToText and TextToSpeech Imports ----------
# -----------------------------------------------------------
import pyttsx3
import speech_recognition as sr
import os
import sys

# Function for relative paths
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)



# Initialising Flask WebApp
app = Flask(__name__)


# ------------------------------------------------
# ---------- Declaring Global Variables ----------
# ------------------------------------------------
Medicines = []
Schedule = []
Possible_Schedule = {
    "001": "Evening",
    "010": "Afternoon",
    "011": "Afternoon, Evening",
    "100": "Morning",
    "101": "Morning, Evening",
    "110": "Morning, Afternoon",
    "111": "Morning, Afternoon, Evening"
}


# Root Template
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/save')
def save():
    global Medicines, Schedule
    try:
        Medicines = json.loads(request.args.get('name'))
        Schedule = json.loads(request.args.get('schedule'))

        result = SaveFile()
        return jsonify(result=result)
    except Exception as e:
        return str(e)


def SaveFile():
    global Medicines, Schedule, Possible_Schedule

    Directory = 'receipts'
    if not os.path.exists(Directory):
        os.makedirs(Directory)

    count = len(os.listdir(Directory)) + 1
    Filename = "Receipt - " + str(count) + ".txt"

    with open(os.path.join(Directory, Filename), 'w') as file:
        file.write("Receipt Created on : " +
                   str(datetime.datetime.now())[:-7] + "\n\n")
        file.write("Medicine : Schedule\n")
        file.write("-------- : --------\n")
        for i in range(len(Medicines)):
            line = Medicines[i] + " : " + Schedule[i] + "\n"
            file.write(line)

    return 'File saved : ' + Filename


'''
# Run Flask WebApp on LocalHost
# LocalHost Server : http://127.0.0.1:5000/
# To TurnOff the localhost (Terminal/Command Line) : Ctrl + C 
'''
if __name__ == '__main__':
    app.run(debug=True)