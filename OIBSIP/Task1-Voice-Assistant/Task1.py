import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

engine = pyttsx3.init()

# Make assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Take voice input
def take_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = listener.listen(source)

    try:
        command = listener.recognize_google(audio)
        command = command.lower()
        print("You said:", command)
        return command
    except:
        return "none"

# Main Program
speak("Voice assistant activated")

while True:
    command = take_command()

    if "hello" in command:
        speak("Hello! How can I help you today?")

    elif "time" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {time}")

    elif "date" in command:
        date = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {date}")

    elif "search" in command:
        query = command.replace("search", "")
        speak("Searching on Google")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif "stop" in command or "exit" in command:
        speak("Session ends....")
        break

    else:
        speak("Sorry, I didn’t understand that.")
