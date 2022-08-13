import json
import os
import optparse

shellcode = (b"\x41\x42\x20\x43")

PokemonList = ["Missingno","Bulbasaur","Ivysaur","Venusaur","Charmander","Charmeleon","Charizard","Squirtle","Wartortle","Blastoise","Caterpie","Metapod","Butterfree","Weedle","Kakuna","Beedrill","Pidgey","Pidgeotto","Pidgeot","Rattata","Raticate","Spearow","Fearow","Ekans","Arbok","Pikachu","Raichu","Sandshrew","Sandslash","NidoranF","Nidorina","Nidoqueen","NidoranM","Nidorino","Nidoking","Clefairy","Clefable","Vulpix","Ninetales","Jigglypuff","Wigglytuff","Zubat","Golbat","Oddish","Gloom","Vileplume","Paras","Parasect","Venonat","Venomoth","Diglett","Dugtrio","Meowth","Persian","Psyduck","Golduck","Mankey","Primeape","Growlithe","Arcanine","Poliwag","Poliwhirl","Poliwrath","Abra","Kadabra","Alakazam","Machop","Machoke","Machamp","Bellsprout","Weepinbell","Victreebel","Tentacool","Tentacruel","Geodude","Graveler","Golem","Ponyta","Rapidash","Slowpoke","Slowbro","Magnemite","Magneton","Farfetchd","Doduo","Dodrio","Seel","Dewgong","Grimer","Muk","Shellder","Cloyster","Gastly","Haunter","Gengar","Onix","Drowzee","Hypno","Krabby","Kingler","Voltorb","Electrode","Exeggcute","Exeggutor","Cubone","Marowak","Hitmonlee","Hitmonchan","Lickitung","Koffing","Weezing","Rhyhorn","Rhydon","Chansey","Tangela","Kangaskhan","Horsea","Seadra","Goldeen","Seaking","Staryu","Starmie","Mr. Mime","Scyther","Jynx","Electabuzz","Magmar","Pinsir","Tauros","Magikarp","Gyarados","Lapras","Ditto","Eevee","Vaporeon","Jolteon","Flareon","Porygon","Omanyte","Omastar","Kabuto","Kabutops","Aerodactyl","Snorlax","Articuno","Zapdos","Moltres","Dratini","Dragonair","Dragonite","Mewtwo","Mew","Chikorita","Bayleef","Meganium","Cyndaquil","Quilava","Typhlosion","Totodile","Croconaw","Feraligatr","Sentret","Furret","Hoothoot","Noctowl","Ledyba","Ledian","Spinarak","Ariados","Crobat","Chinchou","Lanturn","Pichu","Cleffa","Igglybuff","Togepi","Togetic","Natu","Xatu","Mareep","Flaaffy","Ampharos","Bellossom","Marill","Azumarill","Sudowoodo","Politoed","Hoppip","Skiploom","Jumpluff","Aipom","Sunkern","Sunflora","Yanma","Wooper","Quagsire","Espeon","Umbreon","Murkrow","Slowking","Misdreavus","Unown","Wobbuffet","Girafarig","Pineco","Forretress","Dunsparce","Gligar","Steelix","Snubbull","Granbull","Qwilfish","Scizor","Shuckle","Heracross","Sneasel","Teddiursa","Ursaring","Slugma","Magcargo","Swinub","Piloswine","Corsola","Remoraid","Octillery","Delibird","Mantine","Skarmory","Houndour","Houndoom","Kingdra","Phanpy","Donphan","Porygon2","Stantler","Smeargle","Tyrogue","Hitmontop","Smoochum","Elekid","Magby","Miltank","Blissey","Raikou","Entei","Suicune","Larvitar","Pupitar","Tyranitar","Lugia","Ho-Oh","Celebi","Treecko","Grovyle","Sceptile","Torchic"]
Poke_Shellcode = []

def getstringshellcode(shellcode):
    print("PokemonList count:{}".format(len(PokemonList)))
    for x in shellcode:
        Poke_Shellcode.append(PokemonList[x])
    dump=json.dumps(Poke_Shellcode)
    print(dump)
    print(dump,file=open("strshellcode.txt","a"))
    print("[*] save strshellcode the file:strshellcode.txt")
    print("")

def getshellcode(stringshellcode):
    hexshellcode=""
    for strcode in stringshellcode:
        for number in range(len(PokemonList)):
            if strcode==PokemonList[number]:
                tmp="{}".format(str(hex(number)).replace("0x",""))
                if len(tmp)!=2:
                    hexshellcode+="\\x0{}".format(tmp)
                else:
                    hexshellcode+="\\x{}".format(tmp)

    print("shellcode:")
    print(hexshellcode)
    print(hexshellcode,file=open("hexshellcode.txt","a"))
    print("[*] save the hexshellcode the file:hexshellcode.txt")

if __name__ == '__main__':
    parser=optparse.OptionParser()
    parser.add_option('-f',dest="file",help="指定shellcode bin文件")
    (option,args)=parser.parse_args()
    if option.file:
        bin=option.file
        if os.path.exists(bin):
            shellcode=open(bin,"rb").read()
        else:
            print("[-] file:{} is not found".format(bin))
            exit()
        data=(shellcode)
        getstringshellcode(data)
        getshellcode(Poke_Shellcode)
    else:
        parser.print_help()
        print("python shellcodetostr.py -f <raw_shellcode_bin>")
        exit()