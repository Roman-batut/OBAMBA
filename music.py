#Imports
import urllib.request
import re
import fonctionsEngine as f
import asyncio

#Play
async def play(msg) :
  serv = str(msg.guild.name)
  message = msg.content.split(" ")
  commande = '+'.join(message[2:])

  if "www.youtube.com" in commande :
    url = commande
    path = "serveur" + "/" + str(serv) + "/" + "music" + "/" + str(commande[commande.index("=") + 1:]) + ".mp4"
    
    f.creeraudio(commande, url, serv, path, True)

  elif "open.spotify.com" in commande :
    pass

  else :
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + commande)
    videos = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    
    url = "https://www.youtube.com/watch?v=" + str(videos[0])
    path = "serveur" + "/" + str(serv) + "/" + "music" + "/" + str(videos[0]) + ".mp4"
    
    f.creeraudio(commande, url, serv, path, True)

  path = path[:path.index(".mp4")]
  
  return(path)



