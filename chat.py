import nltk 
import discord
nltk.download('punkt')

from nltk import word_tokenize,sent_tokenize

from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
#read more on the steamer https://towardsdatascience.com/stemming-lemmatization-what-ba782b7c0bd8
import numpy as np 
import tflearn
import tensorflow as tf
import random
import json
import pickle
import requests
#from replit import db

with open("intents.json") as file:
    data = json.load(file)

try:
    with open("data.pickle","rb") as f:
        words, labels, training, output = pickle.load(f)

except:
    words = []
    labels = []
    docs_x = []
    docs_y = []
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
            
        if intent["tag"] not in labels:
            labels.append(intent["tag"])


    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    labels = sorted(labels)

    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
               bag.append(1)
            else:
              bag.append(0)
    
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        
        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)
    
    with open("data.pickle","wb") as f:
        pickle.dump((words, labels, training, output), f)



net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")


try:
    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    
    return np.array(bag)


"""
def chat():
    print("Start talking with the bot! (type quit to stop)")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

            
        result = model.predict([bag_of_words(inp, words)])[0]
        result_index = np.argmax(result)
        tag = labels[result_index]

        if result[result_index] > 0.7:  # probability that it matches the intents. json 
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
            print(random.choice(responses))
            
            if tg not in data["intents"]:
                   if "help" in inp.lower():
                       await inp.channel.send(f'How can I help?')
            
            
        else:
            print("I didnt get that. Can you explain or try again.")
"""


def get_quote():
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]["q"] + " -" + json_data[0]["a"]
        return(quote)


def get_idea():
        response = requests.get("https://www.boredapi.com/api/activity")
        json_data = json.loads(response.text)
        idea = json_data["activity"] + "!"
        return(idea)




class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
            inp = message.content

            sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "lonely"]

            resources = [
                "Crisis Text Line - Text “HELLO” to 741741",
                "Disaster Distress Helpline - Call or text 1-800-985-5990",
                "National Suicide Prevention Lifeline - Call 1-800-273-TALK (8255); En español 1-888-628-9454"
                ]
               
            if message.author.id == self.user.id:
                return
           
            else:
#               inp = message.content
               result = model.predict([bag_of_words(inp, words)])[0]
               result_index = np.argmax(result)
               tag = labels[result_index]
               
               if result[result_index] > 0.7:
                   for tg in data["intents"]:
                       if tg['tag'] == tag:
                           responses = tg['responses']
    
                   bot_response=random.choice(responses)
                   await message.channel.send(bot_response.format(message))
# Help                       
               elif "help" in inp.lower():
                       await message.channel.send("Hi, I'm here to help.".format(message))
                       await message.channel.send("If you want inspiration for the day, simply say 'inspire me'.".format(message))
                       await message.channel.send("If you're bored and want ideas for what to do today, just say 'I'm bored'.".format(message))
                       await message.channel.send("I can also provide resources if you're feeling down or depressed. Just let me know how you're feeling.".format(message))
                       await message.channel.send("Lastly, just type 'youtube' and you won't have to stick around me for entertainment!".format(message))
                       
                       
                       
# Functions                      
               elif "youtube" in inp.lower():
                       await message.channel.send("https://www.youtube.com/")
               elif "inspire" in inp.lower():
                   quote = get_quote()
                   await message.channel.send(quote)
                   
               elif "bored" in inp.lower():
                   idea = get_idea()
                   await message.channel.send(idea)


               elif any(word in inp.lower() for word in sad_words):
                   await message.channel.send(random.choice(resources))   
                   
               
              
               else:
                   await message.channel.send("I didnt get that. Can you explain or try again.".format(message))
                          
             
   


client = MyClient()
client.run('OTY1NjcwNjYwNTk4ODA0NTgy.Yl2k4g.68S4AARFbesePO7WZPvgRb_reDI')


###chat()