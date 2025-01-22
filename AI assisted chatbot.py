#AI assisted chatbot/helper
#You need your own weather and openai api key. learned a lot this project, especially with figuring out what services to use when working with more than just the traditional
#import os and tkinter. I had made an AI assistant before, using  gpt 2 from the hugging face library. I decided it was best to have someone put their own api key to the code for 
#reusability. The code could definitely be streamlined more. I intend to keep working and expanding on this.
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import requests
import openai

# Initialize speech engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize recognizer
recognizer = sr.Recognizer()
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand.")
        return ""
    except sr.RequestError:
        print("Could not request results, please check your connection.")
        return ""

#Don't forget to replace with an actual key
openai.api_key = 'your-api-key'

def chatbot_response(prompt):#Changed this because the original function wasn't working 
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"
    

def get_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def get_weather(city):
    api_key = "your-weather-api-key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response["cod"] == 200:
        temperature = response["main"]["temp"]
        weather_description = response["weather"][0]["description"]
        return f"The temperature in {city} is {temperature}°C with {weather_description}."
    else:
        return "City not found."

def open_website(url):
    webbrowser.open(url)
    speak(f"Opening {url}")

def run_assistant():
    speak("Hello, My name is Oasis! How can I assist you today?")
    while True:
        command = listen()

        if "time" in command:
            current_time = get_time()
            speak(f"The time is {current_time}")
        
        elif "weather" in command:
            speak("Which city?")
            city = listen()
            weather_report = get_weather(city)
            speak(weather_report)
        
        elif "open" in command:
            website = command.replace("open ", "")
            open_website(f"https://{website}.com")
        
        elif "exit" in command or "stop" in command:
            speak("Goodbye! Thank you for using me!")
            break
        
        elif "chat" in command:
            speak("What would you like to ask GPT?")
            user_input = listen()
            if user_input:
                response = chatbot_response(user_input) #updated function
                speak(response)
        
        else:
            speak("I'm not sure how to help with that.")

if __name__ == "__main__":
    run_assistant()
