# Description: This is a Virtual assistant that displays date, time, and responds back with a random greeting
#              and returns information on a person.

#pip install pyaudio
#pip install SpeechRecognition
#pip install gTTS
#pip install wikipedia

# import the Libraries
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import datetime
import warnings
import calendar
import random
import wikipedia

# Ignore any warning Messages
warnings.filterwarnings('ignore')

# Record audio and return it as a String
def recordAudio():

    #Record the audio
    r = sr.Recognizer() #creating a recognizer object

    #Open the Microphone and start Recording
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)      #here
        print('Please Say Something')
        audio = r.listen(source, timeout=3)

    #Use Google SpeechRecognition
    data = ''
    try:
        data = r.recognize_google(audio)
        print('You said: '+data)
    except sr.UnknownValueError: #Check unkonwn Error
        print('Google Speech Recognition could not understand the audio, unknown Error')
    except sr.RequestError as e:
        print('Request results from Google Speech Recognition service error'+ e)

    return data

# A Function to give Virtant its speech
def Virtant_peech(text):

    print(text)

    #Convert Text to Speech
    myobj = gTTS(text = text, lang='en', slow=False)

    #Save the converted Audio to a file
    myobj.save('Virtant_Speech.mp3')

    #Play the saved file
    playsound('Virtant_Speech.mp3')

# A Function for a wake-word
def wakeword(text):
    WAKE_WORDS = ['machine', 'hightower', 'Virtant', 'suprabhat'] # A list of wake words

    text = text.lower() #Converting the text to all lower case words

    #Check to see if users command/text contains a wake word
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True

    #If the wake word is not found in the loop then it returns False
            return False

# A Function to get current date
def getDate():

    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()] #Eg- Sunday or Tuesday
    monthNum = now.month
    dayNum = now.day

    # A List of Months
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # A list of ordered numbers for ordered list of dates
    ordinalNumbers1 = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '15th',  '16th', '17th', '18th', '19th']
    ordinalNumbers2 = ['20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st']
    ordinalNumbers = ordinalNumbers1 + ordinalNumbers2

    # Demo returning statement - return Today is Tuesday, June the 2nd.

    return 'Today is '+weekday+', '+month_names[monthNum - 1]+' the '+ ordinalNumbers[dayNum - 1]+'. '


# A Function to return a random greeting response
def greeting(text):

    #Greeting Inputs
    GREETING_INPUTS = ['hi', 'hey', 'hello', 'hi there', 'namaskar', 'namaste', 'aadab']

    #Greeting responses
    GREETING_RESPONSES = ['hello', 'hey there', 'how you doin', 'namaskar', 'aadab']

    #If user's input is a greeting, then return a rnadomly chosen greeting response
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES) +'.'

    #If no greetings were detected, return an empty string
    return ''


# A Function to get a Person's first and last name from Text
def getPerson(text):

    wordList = text.split() # Splitting the text into a list of words

    for i in range(0, len(wordList)):
        if i + 3 <= len(wordList) - 1 and wordList[i].lower() == 'who' and wordList[i+1].lower() == 'is':
            return wordList[i+2] + ' ' + wordList[i+3]


while True:

    #Record the Audio
    text = recordAudio()
    response = ''

    # Checking for the wake up words/phrase
    if(wakeword(text) == True):

        # Check for Greetings by the user
        response = response + greeting(text)

        # Check to see if the user said anything having to do with the date
        if ('date' in text):
            get_date = getDate()
            response = response + ' ' +get_date

        # Check to see if user said anything about time
        if ('time' in text):
            now = datetime.datetime.now()
            meridian =''
            if now.hour >=12:
                meridian = 'p.m.' # Post meridian
                hour = now.hour -12
            else:
                meridian = 'a.m.' #Annie meridian
                hour = now.hour

        # Convert minute into a String
        if now.minute < 10:
            minute = '0'+str(now.minute)
        else:
            minute = str(now.minute)

        response = response + ' ' + 'It is '+str(hour)+ ':'+minute+ ' '+meridian+ ' .'


        # Check to see if the user said 'who is'
        if ('who is' in text):
            person = getPerson(text)
            wiki = wikipedia.summary(person, sentences = 2)
            response = response +' '+ wiki

        # Have the assistant respond back using audio and the text from response
        Virtant_peech(response)
