#Imports
import os, requests
import wikipedia
wikipedia.set_lang("fr")
from whapi import parse_steps, search
from larousse_api import larousse
from googletrans import Translator

import fonctionsEngine as f


'''INITIALISATION'''


#Charger les Commandes
def load(msg) :
  try:
    file = open("serveur" + "/" + msg.guild.name + "/" + msg.guild.name + ".txt", "r", encoding="latin-1")
    file.close()
    listeCommandes = msg.guild.name + "Commandes"
    listeCommandes = f.LoadCommands(msg.guild.name)
    return(listeCommandes)
  except FileNotFoundError :
    os.makedirs("serveur" + "/" + msg.guild.name)
    file = open("serveur" + "/" + msg.guild.name + "/" + msg.guild.name + ".txt", "w")
    file.close()
    return([])

#Ckeck Commandes
def check(msg, listeCommandes) :
  for commande in listeCommandes :
    try :
      mots = msg.content.split(" ", 2)
      if mots[0] + " " + mots[1] == ("rpz " + str(commande.name)) :
        return(True, commande)
    except IndexError : pass
  return(False, None)


'''CREATION ET AFFICHAGE DES COMMANDES'''


#Afficher les Commandes
def help(listeCommandes, textehelpmp3 = "", textehelptxt = "") :
  for commande in listeCommandes :
    if "True" in str(commande.mp3) :
        textehelpmp3 += ("- rpz " + str(
            commande.name) + "\n")
    else:
        textehelptxt += "- rpz " + str(
            commande.name) + "\n"
  y = textehelpmp3.count("-")//3
  try :
    message1 = textehelpmp3[:[i for i, x in enumerate(textehelpmp3) if x == "-"][y]]
    message1reste = textehelpmp3[[i for i, x in enumerate(textehelpmp3) if x == "-"][y]:]
    message2 = message1reste[:[i for i, x in enumerate(message1reste) if x == "-"][y]]
    message2reste = message1reste[[i for i, x in enumerate(message1reste) if x == "-"][y]:]
    return(textehelptxt,message1,message2,message2reste)
  except IndexError : 
    return(textehelptxt, textehelpmp3, "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
  

#Creer les Commandes
def create(msg) :
  if "help" in msg.content : return("Modèles pour rpz create", None, "Modèle classique :","-rpz create [nom de la commande];[texte et image];[.mp3 ou lien youtube]","Modèle uniquement vocale :", "-rpz create [nom de la commande];[.mp3 ou lien youtube]")

  else : 
      serv = str(msg.guild.name)
      texte = msg.content
      texte = texte.replace("rpz create ", "")
      mots = texte.split(";", 3)
      #Détecter la présence d'audio dans mots[2]
      try:
        if "http" in mots[2]:
            mp3oupas = str(True)
            url = mots[2]
        else:
            mp3oupas = str(False)
            url = None
      except IndexError:
          mp3oupas = str(False)
          url = None
      #Détecter la présence d'audio dans mots[1]
      try :
        if "youtu" in mots[1] or ".mp3" or ".mp4" or ".mov" or ".webm" in mots[1]:
            url = mots[1]
            mots[1] = ""
            mp3oupas = str(True)
      except IndexError : 
        mp3oupas = str(False)
        url = None
      #Enregistrer les informations textuelles
      try : 
        if mots[1] != None : 
          f.SaveTxt(mots[0], serv, mots[1], mp3oupas)
      except IndexError : return("Error :", "Il manque des arguments", None, None, None, None)
      #Enregistrer les informations audios
      try:
        path = "serveur" + "/" + str(serv) + "/" 
        f.creeraudio(mots[0], url, serv, path, False)
        return("Information :", "Commande ajoutée", None, None, None, None)
      except requests.exceptions.MissingSchema :
        return("Error :", "Il y a eu une erreur de toute les couleurs c'est chaud wallah", None, None, None, None)

#Supprimer les Commandes
def delete(msg) :
  if "help" in msg.content : return("Modèles pour rpz del", "-rpz del [nom de la commande]")

  else :
    serv = str(msg.guild.name)
    message = msg.content.split("rpz del ")
    commande = message[1]
    with open("serveur" + "/" + serv + "/" + serv + ".txt", "r", encoding="latin-1") as fichier :
      lines = fichier.readlines()
    with open("serveur" + "/" + serv + "/" + serv + ".txt", "w", encoding="latin-1") as fichier :
      for element in lines :
        if element.split(";")[0] != commande :
          fichier.write(element)
        elif "True" in element :
          os.remove("serveur" + "/" + serv + "/" + commande + ".mp3")
    return("Information :", "Commande supprimée")


'''FONCTIONNALITES'''


#Ping les Utilisateurs
def ping(msg) :
  if "help" in msg.content : 
    return("Modèle pour rpz ping","-rpz ping [ping de la personne] [nombre de ping < 11]", 1)
  
  else :
    message = msg.content.split(" ")
    nomduping = message[2]
    nombredeping = int(message[3])
    if nombredeping < 11 :
      return("Information :", nomduping + " est demandé urgament", nombredeping)
    else :
      return("Error :", "Nombre de pings trops élevé", 1)

#Cherche le Wiki
def wiki(msg) :
  if "help" in msg.content : 
    return("Modèle pour rpz wiki","-rpz wiki [sujet ou nom de page]")
  
  else :
    try :
      try :
        wiki = str(msg.content)[9:]
        summary = wikipedia.summary(wiki, sentences=4)
      except wikipedia.exceptions.PageError :
        wiki = str(msg.content)[10:]
        summary = wikipedia.summary(wiki, sentences=4)
      if "==" in str(summary) :
        summary = summary[:int(summary.find("=="))]
      return("Wikipédia :", summary)
    except wikipedia.exceptions.DisambiguationError : 
      return("Error", "La recherche n'est pas assez précise et n'a pu aboutir")
    except wikipedia.exceptions.PageError : 
      return("Error", "La page recherchée n'existe pas")

#Cherche la Définition
def definition(msg) :
  if "help" in msg.content : 
    return("Modèle pour rpz def","-rpz def [mot]")
  
  else :
      mot = str(msg.content)[8:]
      definition = larousse.get_definitions(mot)
      if definition != [] :
        definitionstr = ""
        for i in range (3) : 
          try : definitionstr += str(definition[i]) + "\n"
          except IndexError : break
        return("Définition de " + str(mot), str(definitionstr))
      else : 
        return("Error", "Le mot recherché n'existe pas ou est mal orthographié")

#Cherche le WikiHow  
def wikihow(msg) :
  if "help" in msg.content : 
    return("Modèle pour rpz how","-rpz how [sujet ou nom de page]")
  
  else :
    question = str(msg.content)[8:]
    recherche = search(question, 1)
    try :
      ID = recherche[0].get("article_id")
      steps = parse_steps(ID)
      result = ""
      if int(str(steps.keys()).count("step")) > 1 :
        for i in range (1,int(str(steps.keys()).count("step"))) : 
          result += "**Step " + str(i) + " :** " + steps["step_"+str(i)]["summary"] + "\n"
        return("WikiHow : " + recherche[0].get("title"), result)
      else : 
        result = "**Step 1 :** " + steps["step_1"]["summary"]
        return("WikiHow : " + recherche[0].get("title"), result)
    except IndexError : 
      return("Error", "Ce wikihow n'existe pas ou n'a pu être trouvé")

#Cherche la Traduction
def translate(msg) :
	if "help" in msg.content : 
		return("Modèle pour rpz translate","-rpz translate [texte];[langue d'arrivée]")

	else :
		ts = Translator()
		txt, lg = msg.content[14:].split(";")
		trans = ts.translate(text = txt, dest = lg)
		print(trans)
		return("Traduction :", trans)
