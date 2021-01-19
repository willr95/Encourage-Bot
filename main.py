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
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

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

  # encouragements
  options = starter_encouragements
  if "encouragements" in db.keys():
    options = options + db["encouragements"]

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))
  
  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del", 1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  # is funny

  if any(word in msg for word in funny_words):
    await message.channel.send(random.choice
    (isFunnyArray))

# running bot, token from .env file 

client.run(os.getenv('TOKEN'))