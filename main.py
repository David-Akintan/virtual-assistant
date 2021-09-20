import speech_recognition as sr
import pyttsx3, sys
import datetime
import time, requests
import pywhatkit
import webbrowser
import wikipedia
import pyjokes
import yfinance as yf


r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)



def speak(query):
    engine.getProperty('rate')
    engine.setProperty('rate', 160)
    engine.say(query)
    engine.runAndWait()

def take_command(ask=False):
    data = ''
    with sr.Microphone() as source:
        try:
            r.adjust_for_ambient_noise(source, duration=1)
            #print('Say something...Please')
            audio = r.listen(source)
            data = r.recognize_google(audio)
        except ConnectionError:
            sys.stdout.write("You are not connected to the internet. Try the program again")
            exit(1)
        except ValueError :
            sys.stdout.write('I did not get what you said, could you please say it again!')
            exit(1)

    return data


def respond(query):
    if 'your name' in query:
        stored_names = []
        speak('Well... I do not have a name because I haven"t been given one')
    if 'time' in query:
        now = datetime.datetime.now().strftime('%I:%M %p')
        speak(f'The current time is {now}')
    if 'date' in query:
        day, month, year = date = datetime.datetime.now().strftime('%d %m %Y').split()
        month_name = datetime.datetime.strptime(month, '%m').strftime("%B")
        speak(f'Today is the {day}th day of {month_name} {year}')
    if 'on youtube' in query:
        song = query.replace('on youtube','')
        speak(f'Playing {song} on youtube')
        pywhatkit.playonyt(song)  
    if 'who is' in query:
        person = query[6:]
        query_search = wikipedia.summary(person, sentences=2)
        speak(query_search)
    if 'where is' in query:
        url = ''.join('https://www.google.com/maps/place/' + query[8:] + '/&amp;')
        webbrowser.open(url)
    if 'joke' in query:
        joke = pyjokes.get_joke()
        speak(joke)  
    if 'quote' in query:
        url = "http://quotes.stormconsultancy.co.uk/random.json"
        quote_json = requests.get(url).json()
        time.sleep(.05)
        quote = quote_json['quote']
        speak(quote)
  

def wish(name=False):
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak(f'Good Morning {name}')
        speak(f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}")
        speak("What  can I help you with?")
    if hour >= 12 and hour < 16:
        speak(f'Good Afternoon {name}')
        speak(f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}")
        speak("What  can I help you with?")
    else:
        speak(f'Good Evening {name}, How are you today?')
        speak(f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}")
        speak("What  can I help you with?")

def main():
    speak("Hello! How are you today. Please what is your name? ")
    time.sleep(.05)
    user_name = take_command()
    if user_name == '':
        speak("Oh wow, you have no name")
        speak("DO you want to continue the program")
        ask = take_command()
        if ask.lower == "yes":
            wish(user_name)
            while True:
                query = take_command()
                respond(query)
        else:
            exit(1)
    else:
        wish(user_name)
        while True:
            query = take_command()
            respond(query)

if __name__ == '__main__':
    main()

