import discord
import os
import requests
import json
import random
from replit import db

client = discord.Client()

#variables

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

funny_words = ["lmao", "lol", "haha", "LMAO", "LOL", "LOLOL", "lolol", "hehe"]

starter_encouragements = [
  "Cheer Up!",
  "Hang in there.",
  "You're a great person."
]

isFunnyArray = ["Wow, that is funny!"]

# calling api

def get_quote():
  response = requests.get("https://zenquotes.io/api/today")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + "  - " + json_data[0]['a']
  return (quote)

# adding and deleting encouragements

def update_encouragements(encouraging_message):
  if "encouragements" in db.key():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else: db["encouragements"] = [encouraging_message]

# events

@client.event 
async def on_ready():
  print('We have logged in as {0.user}'
  .format(client))

@client.event
async def on_message(message):
  
  if message.author == client.user:
    return
  
  msg = message.content

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice
    (starter_encouragements))

  if any(word in msg for word in funny_words):
    await message.channel.send(random.choice
    (isFunnyArray))

# running bot, token from .env file 

client.run(os.getenv('TOKEN'))