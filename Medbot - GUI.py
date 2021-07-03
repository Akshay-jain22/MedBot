'''
OS Project

Developers :
    1. Akshay Jain
    2. Anand Kumar
    3. Ashok Kumar
'''

# ---------------------------------
# ---------- GUI Imports ----------
# ---------------------------------
from tkinter import *
import time
import datetime


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


# ------------------------------------------------
# ---------- Setting Root - Tkinter GUI ----------
# ------------------------------------------------
root = Tk()
root.geometry("600x500+400+100")
root.configure(bg='powder blue')
root.iconbitmap(resource_path('assets/icon.ico'))
root.title('Medbot')
root.resizable(False, False)


# ---------------------------------------------------
# ---------- Setting Text to Speech Engine ----------
# ---------------------------------------------------
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


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

def speak(audio):
    Bot_Text.config(text=str(audio))
    Bot_Text.update()
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        text = "Good Morning"
    elif hour >= 12 and hour < 18:
        text = "Good Afternoon"
    else:
        text = "Good Evening"
    Greetings = text + ", I am MedBot sir"
    speak(Greetings)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        Bot_Text.config(text=Bot_Text['text'] + "\nListening...")
        Bot_Text.update()
        r.pause_threshold = 1.0
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        Bot_Text.config(text=Bot_Text['text'] + "\nRecognizing...")
        Bot_Text.update()
        query = r.recognize_google(audio, language="en-in")
        speak(f"User Said : {query}\n")
    
    except sr.RequestError as e:
        speak(f"Could not request results from Google Speech Recognition service : {e}")

    except Exception as e:
        speak("Some Error Occured, Try Again ")
        return "None"

    return query


def InputName():
    speak("Tell the Medicine name")
    medicine = takeCommand()
    if medicine == "None":
        InputName()

    Medicine_Name.delete(0, END)
    Medicine_Name.insert(0, medicine)
    Medicine_Name.update()


def InputSchedule():
    global Medicines, Schedule, Possible_Schedule

    speak("Tell the Schedule")
    schedule = takeCommand().replace(" ", "")
    if schedule == "None":
        return InputSchedule()

    if not schedule in Possible_Schedule.keys():
        temp = ""
        for i in Possible_Schedule.keys():
            temp += i + " "
        speak("The Schedule cannot be other than " + temp + "\n Try Again")

        return InputSchedule()

    Morning.set(0)
    Afternoon.set(0)
    Evening.set(0)

    if schedule[0] == '1'[0]:
        Morning.set(1)
    if schedule[1] == '1'[0]:
        Afternoon.set(1)
    if schedule[2] == '1'[0]:
        Evening.set(1)

    return schedule


def verify():
    global Medicines, Schedule, Possible_Schedule

    schedule = str(Morning.get()) + str(Afternoon.get()) + str(Evening.get())
    speak("Are the details correct?")
    Details = "\nMedicine Name : " + \
        Medicine_Name.get() + "\nSchedule : " + \
        Possible_Schedule[schedule]
    Bot_Text.config(text=Bot_Text['text'] + Details)

    query = takeCommand().lower()
    if query == "None":
        return verify()

    if "no" in query:
        speak("Sorry for inconvenience, Try Editing through GUI")
        return "no"

    return "yes"


def SaveFile():
    global Medicines, Schedule, Possible_Schedule

    Status_Bar.config(text='Saving File ...')
    Status_Bar.update()
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

    Status_Bar.config(text='File saved : ' + Filename)


def update_data():
    global Medicines, Schedule, Possible_Schedule

    verified = verify()
    if verified == "no":
        return

    schedule = str(Morning.get()) + str(Afternoon.get()) + str(Evening.get())
    Medicines += [Medicine_Name.get()]
    Schedule += [Possible_Schedule[schedule]]

    speak("Great. Do you want to add more medicines ?")
    query = takeCommand().lower()

    speak("Okay sir")

    if "no" in query:
        SaveFile()
        speak("Thanks for using Medbot")
        exit()

    run()


def run():
    InputName()
    schedule = InputSchedule()
    update_data()


# ------------------------------------
# ---------- Bot Text Frame ----------
# ------------------------------------
Bot_Frame = LabelFrame(root, text='  Bot is saying ...  ')
Bot_Frame.pack(padx=5, pady=5)

Bot_Text = Message(Bot_Frame, text="", width='500', font=(
    "Helevetica", 10, "bold"), bg=root['bg'], fg="white")
Bot_Text.pack(padx=5, pady=5)


# -----------------------------------
# ---------- Medicine Name ----------
# -----------------------------------
Name_Frame = Frame(root, width='500', height='50', bg=root['bg'])
Name_Frame.pack(padx=5, pady=10)

Label(Name_Frame, text="Medicine Name : ", font=(
    "Helevetice", 15), bg=root['bg'], fg='grey').place(x=0)

Medicine_Name = Entry(Name_Frame, font=(
    "Arial", 15, "bold"), fg=root['bg'], justify='center')
Medicine_Name.place(x=180)

Medicine_Listener_Image = PhotoImage(file=resource_path("assets/speaker.png"))
Medicine_Listener_Button = Button(
    Name_Frame, image=Medicine_Listener_Image, command=InputName, borderwidth=0, bg=root['bg'])
Medicine_Listener_Button.place(x=420)


# ---------------------------------------
# ---------- Medicine Schedule ----------
# ---------------------------------------
Schedule_Frame = Frame(root, width='500', height='200', bg=root['bg'])
Schedule_Frame.pack(padx=5, pady=10)

Label(Schedule_Frame, text="Listen Schedule : ", font=(
    "Helevetice", 15), bg=root['bg'], fg='grey').place(y=0)
Schedule_Listener_Image = PhotoImage(file=resource_path("assets/speaker.png"))
Schedule_Listener_Button = Button(
    Schedule_Frame, image=Schedule_Listener_Image, command=InputSchedule, borderwidth=0, bg=root['bg'])
Schedule_Listener_Button.place(x=220, y=0)

Label(Schedule_Frame, text="Morning : ", font=(
    "Helevetice", 15), bg=root['bg'], fg='grey').place(y=50)
Morning = Scale(Schedule_Frame, from_=0, to=1,
                orient=HORIZONTAL, width='10', bg=root['bg'])
Morning.set(1)
Morning.place(x=180, y=50)

Label(Schedule_Frame, text="Afternoon : ", font=(
    "Helevetice", 15), bg=root['bg'], fg='grey').place(y=100)
Afternoon = Scale(Schedule_Frame, from_=0, to=1,
                  orient=HORIZONTAL, width='10', bg=root['bg'])
Afternoon.set(1)
Afternoon.place(x=180, y=100)

Label(Schedule_Frame, text="Evening : ", font=(
    "Helevetice", 15), bg=root['bg'], fg='grey').place(y=150)
Evening = Scale(Schedule_Frame, from_=0, to=1,
                orient=HORIZONTAL, width='10', bg=root['bg'])
Evening.set(1)
Evening.place(x=180, y=150)


# ------------------------------------
# ---------- Update Details ----------
# ------------------------------------
Button(root, text='Update', command=update_data,
       bg='green', fg='white').pack(pady=5)


# --------------------------------
# ---------- Status Bar ----------
# --------------------------------
Status_Bar = Label(root, text='Medbot Running...',
                   relief=SUNKEN, anchor=W, bg=root['bg'])
Status_Bar.pack(side=BOTTOM, fill=X)

if __name__ == "__main__":
    wishMe()
    run()


root.mainloop()
