#Imports
import discord, os, time, sys, requests, youtube_dl
from pydub import AudioSegment


'''CLASSE'''


class CommandeSimple:
    def __init__(self, name, listeTextes, listeAudios, mp3):
        self.name = name
        self.listeTextes = listeTextes
        self.listeAudios = listeAudios
        self.mp3 = mp3

    async def Execute(self, msg):
        print("Execution de '" + str(self.name) + "' dans " + msg.guild.name)
        for texte in self.listeTextes:
            try:
                await msg.channel.send(texte)
            except discord.errors.HTTPException :
                pass

        for audio in self.listeAudios:
            serv = str(msg.guild.name)
            path = "serveur" + "/" + serv + "/" + audio + ".mp3"
            try:
                file = open(path)
                file.close()
                await jouerAudio(msg, path) 
            except FileNotFoundError :
                await msg.delete()


'''INITIALISATION DES COMMANDES'''


#Charger les commandes du serveur
def LoadCommands(serv = "global") :
    commandes = []
    with open("serveur" + "/" + serv + "/" + serv + ".txt", "r") as fichier :
        contenu = fichier.readlines()
        for ligne in contenu:
            if ligne != "\n":
                mots = ligne.split(";", 3)
                nouvelleCommande = CommandeSimple(mots[0], [mots[1]],
                                                  [mots[0]], [mots[2]])
                commandes.append(nouvelleCommande)
    return commandes

#Redémarrer
def restart():
    time.sleep(2)
    os.execv(sys.executable, ['python'] + sys.argv)
    sys.exit(1)


'''CREER LES COMMANDES'''


#Enregistrer Commande txt
def SaveTxt(name, serv, texte = "", mp3 = False):
    with open("serveur" + "/" + serv + "/" + serv + ".txt", "a") as fichier:
        fichier.write(name + ";" + texte + " ; " + mp3 + "\n")
    with open("serveur" + "/" + "global.txt", "a") as fichier:
        fichier.write(name + ";" + texte + " ; " + mp3 + "\n")

#Enregistrer Commande mp3
def creeraudio(nom, url, serv, path, music) :
    if music == True : 
        ydl_opts = {
            'outtmpl': 
            path,
            'format':
            'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as Mp3 :
            Mp3.download([url]) 
    
    elif "youtu" in str(url) : 
        ydl_opts = {
            'outtmpl':
            path + str(nom) + ".mp3",
            'format':
            'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as Mp3 :
            Mp3.download([url])
    elif ".mp3" in str(url) :
        Mp3 = requests.get(url)
        with open(path + str(nom) + ".mp3", "wb") as f :
            f.write(Mp3.content)
    elif ".mov" or ".mp4" or ".webm" in str(url) :
        video = requests.get(url)
        with open(path + str(nom) + ".mp4", "wb") as f :
            f.write(video.content)
        AudioSegment.from_file(path + str(nom) + ".mp4").export(path + str(nom) + ".mp3", format="mp3")
        os.remove("serveur" + "/" + serv + "/" + str(nom) + ".mp4")
        


'''EXECUTER LES COMMANDES'''


#Faire un message
async def embed(msg, inline, titre0 = "Error : ", desc = None, titre1 = None, message1 = None, titre2 = None, message2 = None, titre3 = None, message3 = None, titre4 = None, message4 = None) :
    embedVar = discord.Embed(title = titre0 , description = desc, color=0xF8D4CC)
    if titre1 != None : 
      embedVar.add_field(name = titre1, value = message1, inline = False)
    if titre1 != None and titre2 != None :
      embedVar.add_field(name = titre2, value = message2, inline = inline)
    if titre2 != None and titre3 != None :
      embedVar.add_field(name = titre3, value = message3, inline = inline)
    if titre3 != None and titre4 != None :
      embedVar.add_field(name = titre4, value = message4, inline = inline)
    await msg.channel.send(embed = embedVar)

#Jouer Un Audio
async def jouerAudio(msg, path) :
    voice_channel = msg.author.voice
    if voice_channel != None:
        vc = await voice_channel.channel.connect()
        vc.play(discord.FFmpegPCMAudio(path))
        while vc.is_playing():
            time.sleep(2)
        await vc.disconnect()
    else : 
        await embed(msg, True, "Error :",str(msg.author.name) + " is not in a channel.")
    await msg.delete()