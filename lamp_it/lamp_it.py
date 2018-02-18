
# coding: utf-8

# # LAMP_It
# It is the interface of the lamp that will respond to the questions and assist the users

# ### imports

# In[1]:

import chatterbot
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS
import wikipedia
import wolframalpha
#answer="";
APPID="LTQUWQ-YLHV4696XJ";
client = wolframalpha.Client(APPID);


# initializing the chatbots

# In[2]:


from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

lamp = ChatBot("Lamp")
lamp.set_trainer(ListTrainer)

lamp = ChatBot(
    'lamp',
    trainer='chatterbot.trainers.ListTrainer',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        "chatterbot.logic.BestMatch",
        "chatterbot.logic.MathematicalEvaluation",
        'chatterbot.logic.TimeLogicAdapter'
    ],
    filters=[
        'chatterbot.filters.RepetitiveResponseFilter'
    ],
    #input_adapter='chatterbot.input.TerminalAdapter',
    #output_adapter='chatterbot.output.TerminalAdapter',
    database='./databaselampit.sqlite3'
)

#VOICE

def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")
#trainer for the list available in the folder
# In[3]:


def train_file(filename):
    speak("I am learinig and launching myself soon");
    path=filename+"";
    file = open(path, 'r')
    n_lines=0;
    for line in file:
        n_lines+=1
    file.close();
    print(n_lines)
    count=0
    file = open(path, 'r')
    for i in range(0,n_lines):
        question=file.readline().replace("- ","").strip();
        answer=file.readline().replace("- ","").strip();
        lamp.train([question,answer]);
        i+=1;

# code to call and test the lamp

# In[17]:

# #### funtion to know if the bot is calibarted or not

# In[4]:


def calibrate():
    file=open("ini.txt",'r')
    s=int(file.read());
    file.close();
    if (s==0):
        return False;
    else:
        return True;
print(calibrate());


# #### function for self calibration

# In[27]:


def self_calibrate():
    path_Q="calibrate.txt"
    Q= open(path_Q, 'r')
    A= open("self_calibrate.txt",'w')
    n_lines=0;
    for line in Q:
        n_lines+=1
    Q.close();
    print(n_lines)
    count=0
    Q = open(path_Q, 'r')
    for i in range(0,n_lines):
        question=Q.readline().replace("- ","").strip();
        print("Q :"+question);
        answer=input("answer")
        A.write(question+"/n");
        A.write(answer+"/n");
        lamp.train([question,answer]);
        i+=1;
        
        
### add the code to change the initial state to zero once the file had been calibrated


# In[6]:


if(calibrate()):
    print("calibarting");
    #self_calibrate();
    train_file("self_calibrate.txt");
else:
    print("dont calibrate");


# In[28]:





# #### function to call for wikipedia and wolfromalpha

# In[7]:



#fucntion to call wikipedia and wolfrom
def online(ask):
    #try and except
    try:
        #wolf
        res=client.query(ask);
        answer=next(res.results).text;
    except:
            try:
                wikipedia.set_lang("en");
                answer=wikipedia.summary(ask,sentences =2);
            except:
                answer="error";
    return answer;


# #### voice recognition functions and its setting up

# In[8]:




def recordAudio():
   # Record Audio
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration = 3);
        print("Say something!")
        audio = r.listen(source)

   # Speech recognition using Google Speech Recognition
    data = ""
    try:
       # Uses the default API key
       # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        data=r.recognize_sphinx(audio);
        print("Sphinx thinks you said " + data)

    return data


# # lamp main function

# In[1]:



def lamp_it(data):
    answer="";
    if "how are you" in data:
        answer=str(lamp.get_response(data));
        print(answer);
        speak(answer);
 
    elif "what time is it" in data:
        speak(ctime())
        
    elif "name" in data:
        answer=str(lamp.get_response(data));
        speak(answer);
 
    elif "where is" in data:
        wikipedia.set_lang("en");
        answer=wikipedia.summary(ask,sentences =2);
        speak(answer);
    elif "can you hear me" in data:
        speak("yes i can hear you ");
        
    elif "search" in data:
        answer=online(data);
        speak(answer);
    elif "calculate" in data:
        answer=online(data);
        speak(answer);
    elif "math" in data:
        answer=online(data);
        speak(answer);
    else:
        answer=str(lamp.get_response(data));
        speak(answer);


# In[11]:


#lamp_it("what is fractals");


# In[2]:





# In[ ]:


#time.sleep(5)
#train_file("ai.yml");
speak("Hi Buddy , what can I do for you?")
while 1:
    data = recordAudio();
    #data=str(input("Question:"));
    ans=lamp_it(data);


# ## testing and trainning part of the lampit

# In[4]:




