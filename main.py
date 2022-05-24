#Imports
from __future__ import unicode_literals
from keepAlive import keepAlive
import discord, os
import random

import fonctionsEngine as f
import fonctionsMain as t
#import music as m
import jeux as z


'''INITIALISATION'''


client = discord.Client()
listeCommandes = []


'''MAIN LOOP'''


#Mise en route
@client.event
async def on_ready():
    print("Je m'appelle {0.user}".format(client))

#Quand un message est envoyé
@client.event
async def on_message(msg) :

    #Test soi-même
		if msg.author == client.user:
			return


    #Initialisation 


    #Charger les commandes et créer les fichiers serveurs
		if "rpz" in msg.content :
			listeCommandes = t.load(msg)
			if listeCommandes == [] : f.restart()

    #Ckecker Commandes Simples
		if msg.content.startswith("rpz") :
			boolean, commande = t.check(msg, listeCommandes)
			if boolean == True : 
				await commande.Execute(msg)

    #Commande restart
		if msg.content.startswith("rpz restart"):
			await f.embed(msg, True, None,"Restarting...")
			f.restart()


    #Commandes Utiles


    #Commande Help
		if msg.content.startswith("rpz help") :
				textehelptxt, message1, message2, message3 = t.help(listeCommandes)
				if textehelptxt == "" : textehelptxt = "Aucune commandes textuelles"
				if message1 == "" : message1 = "Aucune commandes vocales"
				await f.embed(msg, True, "Liste de commandes :", "- rpz create\n- rpz ping\n- rpz wiki\n- rpz def\n- rpz how\n- rpz z\n- rpz oss", "Commandes textuelles : ", textehelptxt, "Commandes vocales : ", message1, "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", message2, "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", message3)

    #Commande Create
		if msg.content.startswith("rpz create") :
			head, body, head2, body2, head3, body3 = t.create(msg)
			await f.embed(msg, True, head, body, head2, body2, head3, body3)

    #Commande Delete
		if msg.content.startswith("rpz del") :
			head, body = t.delete(msg)
			await f.embed(msg, True, head, body)

	
		"""
	#Musique


	#Play
		if msg.content.startswith("rpz play") :
			path = await m.play(msg)
			await f.jouerAudio(msg, path + ".mp3")
	"""
	
	#Divers

    #Ping
		if msg.content.startswith("rpz ping") :
			head, body, nbping = t.ping(msg)
			for i in range(nbping) : await f.embed(msg, True, head, body)
      
    #Wiki
		if msg.content.startswith("rpz wiki") :
			head, body = t.wiki(msg)
			await f.embed(msg, True, head, body)
      
    #Definition
		if msg.content.startswith("rpz def") :
			head, body = t.definition(msg)
			await f.embed(msg, True, head, body)
      
    #Wikihow
		if msg.content.startswith("rpz how") :
			head, body = t.wikihow(msg)
			await f.embed(msg, True, head, body)

	#Translate
		if msg.content.startswith("rpz translate") :
			head, body = t.translate(msg)
			await f.embed(msg, True, head, body)
		

    #Jeux
    

    #ZQuizz
		if msg.content == "rpz z" :
			await z.quizz(client, msg)
		if msg.content.startswith("rpz z ") :
			iterations = int(msg.content.split(" ")[2])
			await z.quizz(client, msg, iterations)
		
		#OSS 
		if msg.content.startswith("rpz oss") :
			await z.oss(msg)



'''FINALISATION'''


keepAlive()
client.run(os.getenv("TOKEN"))
