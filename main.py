import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client=discord.Client()

sad_words=['sad','depressed','depressing','disheartened','crestfallen','dismayed','dismal','despairing',' upset','worried','hopeless','discouraged','disheartened','unhappy','miserable','mournful','gloomy','sorrowful','sorrow','glum','dispirited','disappointed','dejected','Woeful']

default_encouragements=['Cheer up!','Hang in there.','Never give up.','Keep up the good work.','Don’t give up.','Stay strong.','Follow your dreams.','Believe in yourself.']

if "responding" not in db.keys():
  db["responding"]=True

def get_quote():
  response=requests.get("https://zenquotes.io/api/random")
  json_data= json.loads(response.text)
  quote=json_data[0]['q']+" -"+json_data[0]['a']
  return(quote)

def get_animequote():
    response=requests.get("https://animechan.vercel.app/api/random")
    json_data=json.loads(response.text)
    quote=json_data['quote']+" --"+json_data['character']+" from "+json_data['anime']
    return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements=db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"]=encouragements
  else:
    db["encouragements"]=[encouraging_message]

def delete_encouragements(index):
  encouragements=db["encouragements"]
  if len(encouragements)>index:
    del encouragements[index]
    db["encouragements"]=encouragements

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  
  if message.author==client.user:
    return
  msg=message.content

  if msg.startswith(("$who made you","$who built you")):
    await message.channel.send("Author : "+os.environ['author'])

  if msg.startswith("$inspireq"):
    quote=get_quote()
    await message.channel.send(quote)
  
  if msg.startswith("$animeq"):
    quote=get_animequote()
    await message.channel.send(quote)
  
  if db["responding"]:
    options=default_encouragements
    
    if "encouragements" in db.keys():
      options=options+list(db["encouragements"])
    
    if any(word in msg.lower() for word in sad_words):
      await message.channel.send(random.choice(options))
  
  if msg.startswith("$new"):
    encouraging_message=msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")
  
  if msg.startswith("$del"):
    encouragements=[]
    if "encouragements" in db.keys():
      index=int(msg.split("$del",1)[1])
      delete_encouragements(index)
      encouragements=list(db["encouragements"])
    await message.channel.send(encouragements)
  
  if msg.startswith("$list"):
    encouragements=[]
    if "encouragements" in db.keys():
      encouragements=list(db["encouragements"])
    await message.channel.send(encouragements)
  if msg.startswith("$respondingh"):
    value=msg.split("$respondingh ",1)[1]
    if value.lower()=='true':
      db["responding"]=True
      await message.channel.send("Responding is on.")
    else:
      db["responding"]=False
      await message.channel.send("Responding is off.")

keep_alive()

client.run(os.environ['Token'])
