'''
OS Project

Developers :
    1. Akshay Jain
    2. Anand Kumar
    3. Ashok Kumar
'''


import pyttsx3
import speech_recognition as sr
import datetime

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    print("I am MedBot sir")
    speak("I am MedBot sir")


# It takes microphone input from user and returns a string input
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1.0
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User Said : {query}\n")

    except Exception as e:
        speak("Some Error Occured ")
        print("Some Error Occured : ")
        return "None"

    return query


if __name__ == "__main__":
    # Greet the User at Beginning
    wishMe()

    Flag = True
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

    while(Flag):
        print("Tell the Medicine name : ")
        speak("Tell the Medicine name")

        medicine = takeCommand().lower()

        print("Tell the Schedule")
        speak("Tell the Schedule")

        schedule = takeCommand().lower().replace(" ", "")

        if not schedule in Possible_Schedule.keys():
            temp = Possible_Schedule.keys()
            temp = [i for i in temp]
            print("The Schedule cannot be other than ", temp)
            print("Try Again")
            speak("Try Again")
            continue

        print("Medicine Name : ", medicine)
        print("Schedule : ", Possible_Schedule[schedule])
        print("Are the details correct? [YES / NO]")
        speak("Are the details correct?")

        query = takeCommand().lower()

        if "no" in query:
            print("Sorry for inconvenience, Try Again")
            continue

        Medicines += [medicine]
        Schedule += [Possible_Schedule[schedule]]
        print("Great. Do you want to add more medicines ?")
        query = takeCommand().lower()

        print("Okay sir")
        speak("Okay sir")

        if "no" in query:
            Flag = False

    print("\nThe Medicines and Schedule are : ")
    n = len(Medicines)
    for i in range(n):
        print(Medicines[i], " : ", Schedule[i])

    print("\nThanks for using Medbot")

    END = input("Press Enter to exit : ")
