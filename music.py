#Imports
import urllib.request
import re
import fonctionsEngine as f

#Play
def play(msg) :
  serv = str(msg.guild.name)
  message = msg.content.split(" ")
  commande = '+'.join(message[2:])
  
  html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + commande)
  videos = re.findall(r"watch\?v=(\S{11})", html.read().decode())
  url = "https://www.youtube.com/watch?v=" + str(videos[0])
  
  path = "serveur" + "/" + str(serv) + "/" + "music" + "/" + commande + ".mp3"
  f.creeraudio(commande, url, serv, path)
  return(commande, path)
  

