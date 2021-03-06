import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import tensorflow
import discord
from discord.ext import commands
from asyncio.tasks import wait
from asyncio.windows_events import NULL
import discord
from discord.ext import commands
import praw
import random as rand
import asyncio
import speech_recognition as sr
import pyttsx3
import webbrowser
import requests as req
from youtubesearchpython import VideosSearch
from bs4 import BeautifulSoup
from pynput.keyboard import Controller,Key
from googletrans import Translator
from gtts import gTTS
import os
html_text = req.get("https://developers.google.com/admin-sdk/directory/v1/languages").text
soup = BeautifulSoup(html_text, 'lxml')
langs = soup.findAll('td')
lang_Codes = []
for lang in langs:
    lang_Codes.append(lang.text.lower())
trans = Translator()
physical_devices = tensorflow.config.list_physical_devices('GPU') 
tensorflow.config.experimental.set_memory_growth(physical_devices[0], True)
from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes =pickle.load(open('classes.pkl', 'rb'))

model = load_model('chatbotmodel.h5')
print(words)
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key = lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent' : classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    ans = "I don't think I understand that"
    tag = intents_list[0]['intent']
    #print(tag)
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            print(float(intents_list[0]['probability']))
            if float(intents_list[0]['probability']) > 0.65:
                ans = result
    return ans    
print("Floara is running : )")
#while True:
#   temp = input()
#   message = str(temp)
#   ints = predict_class(message)
#   res = get_response(ints, intents)
#   print(res)

client = commands.Bot(command_prefix = "f")

@client.event
async def on_ready():
    print("Bot is ready af")
    #await ctx.send("type `help me` for commands :)")
@client.command()
async def l(ctx,*,arg):
    temp = str(arg)
    src_code = trans.detect(temp).lang
    # print(src_code)
    if src_code != 'en':
        temp = trans.translate(temp, src = src_code, dest = 'en').text
    print(temp)
    message = str(temp)
    ints = predict_class(message)
    res = get_response(ints, intents)
    await ctx.send(res)
client.run("tOkEn")

    





 
