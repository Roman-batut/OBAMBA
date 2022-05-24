#Imports
import random
import asyncio

#ZQUIZZ
liste = [
          "H","He",
          "Li","Be","B","C","N","O","F","Ne",
          "Na","Mg","Al","Si","P","S","Cl","Ar",
          "K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr",
          "Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe",
          "Cs","Ba",
          "La","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu",
          "Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn",
          "Fr","Ra",
          "Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Nh","Fl","Mc","Lv","Ts","Og"]

listeLong = [
          "Hydrogène","Hélium",
          "Lithium","Beryllium","Bore","Carbone","Azote","Oxygène","Fluor","Néon",
          "Sodium","Magnésium","Aluminium","Silicium","Phosphore","Soufre","Chlore","Argon",
          "Potassium","Calcium","Scandium","Titane","Vanadium","Chrome","Manganèse","Fer","Cobalt","Nickel","Cuivre","Zinc","Gallium","Germanium","Arsenic","Sélénium","Brome","Krypton",
          "Rubidium","Strontium","Yttrium","Zirconium","Niobium","Molybdène","Technétium","Ruthénium","Rhodium","Palladium","Argent","Cadmium","Indium","Étain","Antimoine","Tellure","Iode","Xénon",
          "Césium","Baryum",
          "Lanthane","Cérium","Praséodyme","Néodyme","Prométhium","Samarium","Europium","Gadolinium","Terbium","Dysprosium","Holmium","Erbium","Thalium","Ytterbium","Lutécium",
          "Hafnium","Tantale","Tungstène","Rhénium","Osmium","Iridium","Platine","Or","Mercure","Thallium","Plomb","Bismuth","Polonium","Astate","Radon",
          "Francium","Radium",
          "Atcinium","Thorium","Protactinium","Uranium","Neptunium","Plutonium","Américium","Curium","Berkélium","Califonium","Einsteinium","Fermium","Mendelevium","Nobélium","Lawrencium","Rutherfodium","Dubnium","Seaborgium","Borhium","Hassium","Meintnérium","Darmstadtium","Roentgenium","Copernicium","Nihonium","Flérovium","Moscovium","Livermorium","Tenessine","Oganesson"]

async def quizz(client, msg, iter=1):
  if "help" in msg.content : 
    await msg.channel.send("Modèle pour rpz z","-rpz z [nombre de fois = 1]")
  else :
    for i in range(iter) :
      z = random.randint(1,36)
      await msg.channel.send("Petite question...")
      await msg.channel.send("Z=" + str(z) + " c'est quoi ?")
    
      def checkFunc(user):
        return user.author == msg.author

      try:
        reponse = await client.wait_for('message', timeout=10.0, check=checkFunc)
        if reponse.content == liste[z - 1]:
          await msg.channel.send("bien ouej")
        else :
          await msg.channel.send("Movaiz reponse ! haha t tro nul !!1!1")
          await msg.channel.send("En fait ct " + liste[z - 1] + ", c à dire " + listeLong[z - 1])  
      except asyncio.TimeoutError:
        await msg.channel.send("Ta pris tro de temps ! haha t nul !!1!1")
        await msg.channel.send("En fait ct " + liste[z - 1] + ", c à dire " + listeLong[z - 1])


#OSS 117
async def oss(msg) :
	with open("serveur/oss117.txt", "r", encoding="latin-1") as fichier :
		text = fichier.readlines()
		step = random.randrange(5)
		start = random.randrange(len(text)-step)
		for i in range(step) :
			await msg.channel.send(text[start + i])