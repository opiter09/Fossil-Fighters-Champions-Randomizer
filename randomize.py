import os
import shutil
import subprocess
import random
import sys
import FreeSimpleGUI as psg

def digsiteOutput():
    text = open("newDigsiteSpawns.txt", "wt")
    text.close()
    text = open("newDigsiteSpawns.txt", "at")
    for root, dirs, files in os.walk("NDS_UNPACK/data/map/m/bin/"):
        for file in files:
            if (file == "0.bin"):
                f = open(os.path.join(root, file), "rb")
                r = f.read()
                f.close()
                point = int.from_bytes(r[0x6C:0x70], "little")
                mapN = os.path.join(root, file).split("\\")[-2]
                mapN = mapN.split("/")[-1] # it just works
                f = open("ffc_kasekiNames.txt", "rt")
                vivoNames = list(f.read().split("\n")).copy()
                f.close()
                realP = [ int.from_bytes(r[point:(point + 4)], "little") ]
                loc = point + 4
                while (realP[-1] > 0):
                    realP.append(int.from_bytes(r[loc:(loc + 4)], "little"))
                    loc = loc + 4
                realP = realP[0:-1]
                check = 0
                for val in realP:
                    index = int.from_bytes(r[(val + 2):(val + 4)], "little")
                    if (index == 0):
                        continue
                    else:
                        if (check == 0):
                            check = 1
                            text.write(mapN + ":\n")
                    text.write("\tZone " + str(index).zfill(2) + ":\n")
                    numTables = int.from_bytes(r[(val + 12):(val + 16)], "little")
                    point3 = int.from_bytes(r[(val + 16):(val + 20)], "little")
                    for i in range(numTables):
                        text.write("\t\tFossil Chip " + str(i) + ":\n")
                        point4 = int.from_bytes(r[(val + point3 + (i * 4)):(val + point3 + (i * 4) + 4)], "little")
                        point5 = int.from_bytes(r[(val + point4 + 12):(val + point4 + 16)], "little")
                        maxFos = int.from_bytes(r[(val + point4 + point5 + 4):(val + point4 + point5 + 8)], "little")
                        text.write("\t\t\tMax Spawns: " + str(maxFos) + "\n")
                        numWeird = int.from_bytes(r[(val + point4 + point5 + 8):(val + point4 + point5 + 12)], "little")
                        numSpawns = int.from_bytes(r[(val + point4 + point5 + 16):(val + point4 + point5 + 20)], "little")
                        startSpawns = val + point4 + point5 + 24 + (numWeird * 2)
                        for j in range(numSpawns):
                            thisStart = startSpawns + (j * 8)
                            dark = (["N/A", "Normal", "Dark"])[r[thisStart]]
                            rare = (["N/A", "Normal", "Rare"])[r[thisStart + 1]]
                            vivoNum = int.from_bytes(r[(thisStart + 2):(thisStart + 4)], "little")
                            # chance = int.from_bytes(r[(val + point4 + 4):(val + point4 + 8)], "little")
                            s = "\t\t\t" + "[0x" + hex(thisStart + 2).upper()[2:] + "] " + vivoNames[vivoNum]
                            s = s + " (" + dark + ", " + rare + ")" + "\n"
                            text.write(s)
                if (check == 1):
                    text.write("\n")
    text.close()

def messageReplace(fileNum, oldList, newList):
    byteList = []
    subprocess.run([ "fftool.exe", "./NDS_UNPACK/data/msg/msg_" + fileNum ])
    f = open("./NDS_UNPACK/data/msg/bin/msg_" + fileNum + "/0.bin", "rb")
    r = f.read()
    f.close()
    numStrings = int.from_bytes(r[4:8], "little")
    for i in range(12, 12 + (numStrings * 4), 4):
        loc = int.from_bytes(r[i:(i + 4)], "little")
        nextLoc = int.from_bytes(r[(i + 4):(i + 8)], "little")
        if ((i + 4) >= (12 + (numStrings * 4))):
            nextLoc = os.stat("./NDS_UNPACK/data/msg/bin/msg_" + fileNum + "/0.bin").st_size
        temp = (r[(loc + 8):nextLoc]).decode("UTF-8", errors = "ignore")
        for j in range(min(len(oldList), len(newList))):
            temp = temp.replace(oldList[j], newList[j])
        temp = temp.encode("UTF-8", errors = "ignore")
        align = 4 - (len(r[loc:(loc + 8)] + temp) % 4)
        if (align < 4):
            byteList.append(r[loc:(loc + 8)] + temp + bytes(align))
        else:
            byteList.append(r[loc:(loc + 8)] + temp)
    f = open("./NDS_UNPACK/data/msg/bin/msg_" + fileNum + "/0.bin", "wb")
    f.close()
    f = open("./NDS_UNPACK/data/msg/bin/msg_" + fileNum + "/0.bin", "ab")
    f.write(r[0:16])
    writeLoc = int.from_bytes(r[12:16], "little")
    for i in range(len(byteList) - 1):
        writeLoc = writeLoc + len(byteList[i])
        f.write(writeLoc.to_bytes(4, "little"))
    for i in range(len(byteList)):
        f.write(byteList[i])
    f.close()
    subprocess.run([ "fftool.exe", "compress", "./NDS_UNPACK/data/msg/bin/msg_" + fileNum + "/", "-c", "None", "-c", "None",
        "-i", "0.bin", "-o", "./NDS_UNPACK/data/msg/msg_" + fileNum ])
    shutil.rmtree("NDS_UNPACK/data/msg/bin/")

layout = [
    [ psg.Text("Randomize Fossils?", size = 17), psg.Button("Yes", key = "dig", size = 5) ],
    [ psg.Text("Randomize Starters?", size = 17), psg.Button("Yes", key = "start", size = 5) ],
    [ psg.Text("Randomize Teams?", size = 17), psg.Button("No", key = "team", size = 5) ],
    [ psg.Text("Randomize Colors?", size = 17), psg.Button("No", key = "color", size = 5) ],
    [ psg.Text("Randomize Particles?", size = 17), psg.Button("No", key = "anim", size = 5) ],
    [ psg.Text("Mono-Spawn Mode?", size = 17), psg.Button("No", key = "mono", size = 5) ],
    [ psg.Text("Custom Starters:", size = 17), psg.Input(default_text = "", key = "custom", size = 22, enable_events = True) ],
    [ psg.Text("Post-Game Vivos:", size = 17), psg.Input(default_text = "43, 76, 105, 114, 119, 128", key = "broken",
        size = 22, enable_events = True) ],
    [ psg.Text("PGV's in Teams?", size = 17), psg.Button("No", key = "include", size = 5) ],
    [ psg.Text("Team Level Change:", size = 17), psg.Input(default_text = "0", key = "level", size = 5, enable_events = True) ],
    [ psg.Text("TLC on Nameless?", size = 17), psg.Button("Yes", key = "jewel", size = 5) ],
    [ psg.Button("Run") ]
]
window = psg.Window("", layout, grab_anywhere = True, resizable = True, font = "-size 12")
good = 0
res = { "dig": "Yes", "start": "Yes", "include": "No", "team": "No", "color": "No", "anim": "No", "mono": "No", "jewel": "Yes" }
brokenR = ""
levelR = 0
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if (event == psg.WINDOW_CLOSED) or (event == "Quit"):
        good = 0
        break
    elif (event in res.keys()):
        x = ["No", "Yes"]
        new = x[int(not x.index(window[event].get_text()))]
        window[event].update(new)
        res[event] = new
    elif (event == "Run"):
        good = 1
        brokenR = values["broken"]
        levelR = values["level"]
        customR = values["custom"]
        try:
            levelR = int(levelR)
        except:
            levelR = 0
        break
    
if (good == 1):
    vivos = list(range(1, 150))
    random.shuffle(vivos)
    vivos = [0] + vivos

    broken = list(brokenR.replace(" ", "").replace("\n", "").split(","))
    broken = list(set(broken))
    try:
        broken = [ max(1, min(149, int(x))) for x in broken ]
    except:
        broken = []
    # print(broken)

    shift = [3, 23, 43, 58, 83, 5, 37, 62, 87, 91, 27, 29, 41, 68, 80, 45, 55, 60, 64, 90, 21, 40, 42, 49, 84]
    for b in broken:
        try:
            shift.remove(b)
        except:
            pass
    for i in shift:
        if (vivos[i] in broken):
            x = vivos[i]
            y = vivos[vivos[i]]
            vivos[i] = y
            vivos[x] = x
    for i in range(min(len(broken), len(shift))):
        ind = vivos.index(broken[i])
        x = vivos[ind]
        y = vivos[shift[i]]
        vivos[ind] = y
        vivos[shift[i]] = x
    # print(vivos[111])
    # print(vivos.index(111))

    vivoNames = ["NONE"] + list(open("ffc_vivoNames.txt", "rt").read().split("\n"))
    vivoLongNames = ["NONE"] + list(open("ffc_vivoLongNames.txt", "rt").read().split("\n"))
    fossilNames = list(open("ffc_kasekiNames.txt", "rt").read().split("\n"))
    
    if ((res["start"] == "Yes") or (customR != "")):
        if (res["start"] == "Yes"):
            shift = 0
            starters = [ vivos[102], vivos[112], vivos[118], vivos[136], vivos[73] ]
            while ((102 in starters) or (112 in starters) or (118 in starters) or (136 in starters) or (73 in starters)):
                shift = shift + 1
                starters = [ vivos[102 - shift], vivos[112 - shift], vivos[118 - shift], vivos[136 - shift], vivos[73 - shift] ]
        else:
            starters = [102, 112, 118, 136, 73]
        custom = list(customR.replace(" ", "").replace("\n", "").split(","))
        temp = []
        for c in custom:
            if c not in temp:
                temp.append(c)
        custom = temp.copy()
        try:
            custom = [ max(1, min(210, int(x))) for x in custom ]
        except:
            custom = []  
        for i in range(min(len(custom), 5)):
            starters[i] = custom[i]
        temp = 149 # Dikelo
        for k in ["Head", "Single"]:
            if ((vivoNames[starters[4]] + " " + k) in fossilNames):
                temp = starters[4]
        starters[4] = temp
        old = [102, 112, 118, 136, 73]
        if (res["dig"] == "No"): # the starters will still be random, but everything else isn't for the digsite stuff below
            vivos = [0] + list(range(1, 150))
        for i in range(5):
            x = vivos.index(min(149, starters[i]))
            y = vivos[old[i]]
            vivos[x] = y
            vivos[old[i]] = min(149, starters[i])

    fossilTable = { "Head": [0], "Body": [0], "Arms": [0], "Legs": [0] }
    for v in vivoNames:
        for k in fossilTable.keys():
            if ((v + " " + k) in fossilNames):
                fossilTable[k].append(fossilNames.index(v + " " + k))
            elif ((v + " Single") in fossilNames):
                fossilTable[k].append(fossilNames.index(v + " Single"))
    # print(fossilTable["Head"])

    if (os.path.exists("NDS_UNPACK/y7.bin") == True):
        shutil.rmtree("./NDS_UNPACK/")
    if (os.path.exists("out.nds") == True):
        os.remove("out.nds")
    subprocess.run([ "dslazy.bat", "UNPACK", sys.argv[1] ])
    
    subprocess.run([ "xdelta3-3.0.11-x86_64.exe", "-d", "-f", "-s", "NDS_UNPACK/arm9.bin", "ffc_apFix.xdelta",
        "NDS_UNPACK/arm9x.bin" ])
    if (os.path.exists("NDS_UNPACK/arm9x.bin") == True):
        os.remove("NDS_UNPACK/arm9.bin")
        os.rename("NDS_UNPACK/arm9x.bin", "NDS_UNPACK/arm9.bin")

    moveLevels = []
    subprocess.run([ "fftool.exe", "NDS_UNPACK/data/etc/creature_defs" ])
    f = open("NDS_UNPACK/data/etc/bin/creature_defs/0.bin", "rb")
    zero = f.read()
    f.close()
    moveLevels.append([0, 0, 0])
    for i in range(210):
        oldOffset = int.from_bytes(zero[(44 + (i * 4)):(48 + (i * 4))], "little")
        ml2 = zero[oldOffset + 0xC6]
        ml3 = zero[oldOffset + 0xC8]
        ml4 = zero[oldOffset + 0xCA]
        moveLevels.append([ml2, ml3, ml4])
    shutil.rmtree("NDS_UNPACK/data/etc/bin/")
    
    if ((res["dig"] == "Yes") or (res["start"] == "Yes") or (customR != "")):
        subprocess.run([ "fftool.exe", "NDS_UNPACK/data/episode/e0023" ])
        f = open("NDS_UNPACK/data/episode/bin/e0023/0.bin", "rb")
        r = f.read()
        f.close()
        f = open("NDS_UNPACK/data/episode/bin/e0023/0.bin", "wb")
        f.close()
        f = open("NDS_UNPACK/data/episode/bin/e0023/0.bin", "ab")
        f.write(r[0:0x2C84])
        temp = 565 # Dikelo Single
        for k in ["Head", "Single"]:
            if ((vivoNames[vivos[119]] + " " + k) in fossilNames):
                temp = fossilNames.index(vivoNames[vivos[119]] + " " + k)
        f.write(temp.to_bytes(2, "little"))
        f.write(r[0x2C86:])
        f.close()
        subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/episode/bin/e0023/", "-c", "None", "-c", "None",
            "-i", "0.bin", "-o", "NDS_UNPACK/data/episode/e0023" ])
        shutil.rmtree("NDS_UNPACK/data/episode/bin/")

        subprocess.run([ "fftool.exe", "NDS_UNPACK/data/map/m" ])
        for root, dirs, files in os.walk("NDS_UNPACK/data/map/m/bin"):
            for file in files:
                if (file == "0.bin"):
                    used = {}
                    f = open(os.path.join(root, file), "rb")
                    r = f.read()
                    f.close()
                    first = {"Head": 0, "Body": 0, "Arms": 0, "Legs": 0}
                    silver = [900, 901, 902, 903]
                    random.shuffle(silver)
                    mapN = os.path.join(root, file).split("\\")[-2]
                    if (os.path.exists("NDS_UNPACK/data/map/e/" + mapN) == False):
                        continue
                    f = open(os.path.join(root, file), "wb")
                    f.close()
                    f = open(os.path.join(root, file), "ab")
                    point = int.from_bytes(r[0x6C:0x70], "little")
                    realP = [ int.from_bytes(r[point:(point + 4)], "little") ]
                    loc = point + 4
                    while (realP[-1] > 0):
                        realP.append(int.from_bytes(r[loc:(loc + 4)], "little"))
                        loc = loc + 4
                    realP = realP[0:-1]
                    for val in realP:
                        index = int.from_bytes(r[(val + 2):(val + 4)], "little")
                        if (index == 0):
                            continue
                        numTables = int.from_bytes(r[(val + 12):(val + 16)], "little")
                        point3 = int.from_bytes(r[(val + 16):(val + 20)], "little")
                        for i in range(numTables):
                            point4 = int.from_bytes(r[(val + point3 + (i * 4)):(val + point3 + (i * 4) + 4)], "little")
                            point5 = int.from_bytes(r[(val + point4 + 12):(val + point4 + 16)], "little")
                            numWeird = int.from_bytes(r[(val + point4 + point5 + 8):(val + point4 + point5 + 12)], "little")
                            numSpawns = int.from_bytes(r[(val + point4 + point5 + 16):(val + point4 + point5 + 20)], "little")
                            startSpawns = val + point4 + point5 + 24 + (numWeird * 2)
                            for j in range(numSpawns):
                                thisStart = startSpawns + (j * 8)
                                kasekiNum = int.from_bytes(r[(thisStart + 2):(thisStart + 4)], "little")
                                used[thisStart + 2] = kasekiNum
                    for i in range(0, len(r), 2):
                        if (i in used.keys()):
                            check = 0
                            temp = ["Head", "Body", "Arms", "Legs"]
                            for p in temp:
                                if (used[i] in fossilTable[p]):
                                    if (fossilNames[used[i]].endswith("Single") == True):
                                        old = fossilTable[p].index(used[i])
                                        new = fossilTable["Head"][vivos[old]]
                                        if (first[p] == 0):
                                            for t in temp:
                                                first[t] = fossilTable[t][vivos[old]]
                                        # print(fossilNames[used[i]])
                                        # print(fossilNames[new])
                                        # print("\n")
                                    else:
                                        old = fossilTable[p].index(used[i])
                                        new = fossilTable[p][vivos[old]]
                                        if (first[p] == 0):
                                            first[p] = new
                                    if (res["mono"] == "Yes"):
                                        f.write(first[p].to_bytes(2, "little"))
                                    else:
                                        f.write(new.to_bytes(2, "little"))
                                    check = 1
                                    break
                                elif ((used[i] in [900, 901, 902, 903]) and (res["dig"] == "Yes")):
                                    new = silver[used[i] - 900]
                                    f.write(new.to_bytes(2, "little"))
                                    check = 1
                                    break
                            if ((used[i] in [995, 996, 997, 998]) and ((res["start"] == "Yes") or (customR != ""))):
                                p = temp[used[i] - 995]
                                if ((vivoNames[starters[4]] + " Single") in fossilNames):
                                    new = fossilNames.index(vivoNames[starters[4]] + " Single")
                                elif ((vivoNames[starters[4]] + " " + p) in fossilNames):
                                    new = fossilNames.index(vivoNames[starters[4]] + " " + p)
                                else:
                                    new = 565 # Dikelo Single
                                f.write(new.to_bytes(2, "little"))
                                check = 1
                            if (check == 0):
                               f.write(r[i:(i + 2)]) 
                        else:
                            f.write(r[i:(i + 2)])
                    f.close()
                    subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/map/m/bin/" + mapN, "-i", "0.bin", "-o",
                        "NDS_UNPACK/data/map/m/" + mapN ])
        digsiteOutput()
        shutil.rmtree("NDS_UNPACK/data/map/m/bin/")
        
        subprocess.run([ "fftool.exe", "NDS_UNPACK/data/etc/donate_kaseki_defs" ])
        f = open("NDS_UNPACK/data/etc/bin/donate_kaseki_defs/0.bin", "rb")
        r = f.read()
        f.close()
        f = open("NDS_UNPACK/data/etc/bin/donate_kaseki_defs/0.bin", "wb")
        f.close()
        f = open("NDS_UNPACK/data/etc/bin/donate_kaseki_defs/0.bin", "ab")
        f.write(r[0:0x18])
        for i in range(0x18, len(r), 8):
            f.write(r[i:(i + 4)])
            check = 0
            curr = int.from_bytes(r[(i + 4):(i + 6)], "little")
            for p in ["Head", "Body", "Arms", "Legs"]:
                if (curr in fossilTable[p]):
                    old = fossilTable[p].index(curr)
                    new = fossilTable[p][vivos[old]]
                    f.write(new.to_bytes(2, "little"))
                    check = 1
                    break
            if (check == 0):
               f.write(r[(i + 4):(i + 6)])
            f.write(r[(i + 6):(i + 8)])
        f.close()
        subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/etc/bin/donate_kaseki_defs/", "-i", "0.bin", "-o",
            "NDS_UNPACK/data/etc/donate_kaseki_defs" ])
        shutil.rmtree("NDS_UNPACK/data/etc/bin/")
        
    if ((res["start"] == "Yes") or (customR != "")):
        subprocess.run([ "fftool.exe", "NDS_UNPACK/data/episode/e0012" ])
        f = open("NDS_UNPACK/data/episode/bin/e0012/0.bin", "rb")
        r = f.read()
        f.close()
        f = open("NDS_UNPACK/data/episode/bin/e0012/0.bin", "wb")
        f.close()
        f = open("NDS_UNPACK/data/episode/bin/e0012/0.bin", "ab")
        places = [0x1B28, 0x1B48, 0x1B60, 0x1DD8, 0x1DF8, 0x1E10, 0x2088, 0x20A8, 0x20C0, 0x2338, 0x2358, 0x2370, len(r)]
        temp = [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4]
        f.write(r[0:places[0]])
        for i in range(len(places) - 1):
            f.write(starters[temp[i]].to_bytes(2, "little"))
            f.write(r[(places[i] + 2):places[i + 1]])
        f.close()
        subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/episode/bin/e0012/", "-c", "None", "-c", "None",
            "-i", "0.bin", "-o", "NDS_UNPACK/data/episode/e0012" ])
            
        subprocess.run([ "fftool.exe", "NDS_UNPACK/data/episode/e0022" ])
        f = open("NDS_UNPACK/data/episode/bin/e0022/0.bin", "rb")
        r = f.read()
        f.close()
        f = open("NDS_UNPACK/data/episode/bin/e0022/0.bin", "wb")
        f.close()
        f = open("NDS_UNPACK/data/episode/bin/e0022/0.bin", "ab")
        f.write(r[0:0x1780])
        temp = 565 # Dikelo Single
        revi = 149
        for k in ["Head", "Single"]:
            if ((vivoNames[starters[4]] + " " + k) in fossilNames):
                temp = fossilNames.index(vivoNames[starters[4]] + " " + k)
                revi = starters[4]
        f.write(temp.to_bytes(2, "little"))
        f.write(r[0x1782:0x1C74])
        f.write(revi.to_bytes(2, "little"))
        f.write(r[0x1C76:0x244C])
        f.write(revi.to_bytes(2, "little"))
        f.write(r[0x244E:])
        f.close()
        subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/episode/bin/e0022/", "-c", "None", "-c", "None",
            "-i", "0.bin", "-o", "NDS_UNPACK/data/episode/e0022" ])
        shutil.rmtree("NDS_UNPACK/data/episode/bin/")
        
        articleList = ["a", "a", "a", "a", "a"]
        for i in range(5):
            if (vivoLongNames[starters[i]][0] in ["A", "E", "I", "O", "U"]):
                if (vivoLongNames[starters[i]] != "Utahraptor"):
                    articleList[i] = "an"
        oldLong = [vivoLongNames[x] for x in [102, 112, 118, 136, 73]]
        newLong = [vivoLongNames[x] for x in starters]
        oldDesc = [
            "That there's an $c4Aerosteon$c0. He's\na power type that overwhelms\nfoes with his sharp claws.",
            "That's a fast-growing, well-balanced\nvivosaur called a $c4Toba Titanosaur$c0. \nIt's one'a yer more fashionable types.",
            "Now that there's a $c4Tsintaosaurus$c0. \nIt's a backup-type vivosaur that \nhas great support skills.",
            "And finally, we got a $c4Dimetrodon$c0.\nIt's a tricky technical type that\nconfounds foes with special skills."
        ]
        newDesc = [
            "We got " + articleList[0] + " $c4" + newLong[0] + "$c0,",
            articleList[1] + " $c4" + newLong[1] + "$c0,",
            articleList[2] + " $c4" + newLong[2] + "$c0,",
            "and " + articleList[3] + " $c4" + newLong[3] + "$c0."
        ]
        messageReplace("0012", oldDesc + oldLong, newDesc + newLong)
        
        tricName = vivoLongNames[starters[4]]
        messageReplace("0022", ["a $c2Triceratops Dino Medal"], [articleList[4] + " $c2" + tricName + "\nDino Medal"])
        oldNames = [vivoNames[x] for x in [102, 112, 118, 136, 73]]
        newNames = [vivoNames[x] for x in starters]
        new = open("newStarters.txt", "wt")
        new.close()
        new = open("newStarters.txt", "at")
        for i in range(4):
            new.write(oldNames[i] + " --> " + newNames[i] + "\n")
        new.close()

        for i in range(1, 5):
            subprocess.run([ "fftool.exe", "NDS_UNPACK/data/battle_param/battle_param_defs_" + str(i) ])
            f = open("NDS_UNPACK/data/battle_param/bin/battle_param_defs_" + str(i) + "/0.bin", "rb")
            r = f.read()
            f.close()
            f = open("NDS_UNPACK/data/battle_param/bin/battle_param_defs_" + str(i) + "/0.bin", "wb")
            f.close()
            f = open("NDS_UNPACK/data/battle_param/bin/battle_param_defs_" + str(i) + "/0.bin", "ab")
            loc = int.from_bytes(r[0x38:0x3C], "little") - 0x18
            f.write(r[0:loc])
            f.write(starters[i - 1].to_bytes(2, "little"))
            f.write(r[(loc + 2):])
            f.close()
            subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/battle_param/bin/battle_param_defs_" + str(i),
                "-c", "None", "-c", "None", "-i", "0.bin", "-o", "NDS_UNPACK/data/battle_param/battle_param_defs_" + str(i) ])
        shutil.rmtree("NDS_UNPACK/data/battle_param/bin/")            
        
    if ((res["team"] == "Yes") or (levelR != 0)):
        f = open("ffc_enemyNames.txt", "rt")
        eNames = list(f.read().split("\n"))
        f.close()

        subprocess.run([ "fftool.exe", "NDS_UNPACK/data/battle_param" ])
        for root, dirs, files in os.walk("NDS_UNPACK/data/battle_param/bin"):
            for file in files:
                if (file == "0.bin"):
                    f = open(os.path.join(root, file), "rb")
                    r = f.read()
                    f.close()
                    shift = r[0x38] + 2 - 0x46
                    try:
                        orig = int.from_bytes(r[(0x46 + shift):(0x48 + shift)], "little")
                        teamN = eNames[orig - 0x104E]
                    except:
                        teamN = ""
                    if ((len(r) > 0x46) and (r[0x34] == 0) and ((res["jewel"] == "Yes") or (teamN != "Fossil Fighter"))):
                        f = open(os.path.join(root, file), "wb")
                        f.close()
                        f = open(os.path.join(root, file), "ab")
                        mapN = os.path.join(root, file).split("\\")[-2]
                        numVivos = r[0x58 + shift]
                        f.write(r[0:(0x70 + shift)])
                        vivoLevels = []
                        vivoNumbers = []
                        for i in range(numVivos):
                            vivoNum = int.from_bytes(r[(0x70 + shift + (i * 12)):(0x70 + shift + (i * 12) + 2)], "little")
                            listOfLists = [ [1, 149], [150, 179], [180, 183], [184, 190] ]
                            check = 0
                            newVivo = 0
                            for L in listOfLists:
                                if ((vivoNum in list(range(L[0], L[1] + 1))) and (res["team"] == "Yes")):
                                    if (res["include"] == "Yes"):
                                        newVivo = random.randint(L[0], L[1])
                                        f.write(newVivo.to_bytes(2, "little"))
                                    else:
                                        newVivo = random.randint(L[0], L[1])
                                        while (newVivo in broken):
                                            newVivo = random.randint(L[0], L[1])
                                        f.write(newVivo.to_bytes(2, "little"))
                                    check = 1
                                    break
                            if (check == 0):
                                newVivo = int.from_bytes(r[(0x70 + shift + (i * 12)):(0x70 + shift + (i * 12) + 2)], "little")
                                f.write(r[(0x70 + shift + (i * 12)):(0x70 + shift + (i * 12) + 2)])
                            vivoNumbers.append(newVivo)
                            if (levelR != 0):
                                oldLevel = int.from_bytes(r[(0x70 + shift + (i * 12) + 2):(0x70 + shift + (i * 12) + 4)], "little")
                                newLevel = max(1, min(oldLevel + levelR, 20))
                                f.write(newLevel.to_bytes(2, "little"))
                            else:
                                newLevel = int.from_bytes(r[(0x70 + shift + (i * 12) + 2):(0x70 + shift + (i * 12) + 4)], "little")
                                f.write(r[(0x70 + shift + (i * 12) + 2):(0x70 + shift + (i * 12) + 4)])
                            vivoLevels.append(newLevel)
                            f.write(r[(0x70 + shift + (i * 12) + 4):(0x70 + shift + (i * 12) + 12)])
                        f.write(r[(0x70 + shift + (numVivos * 12)):(0x70 + shift + (numVivos * 16))])
                        for i in range(numVivos):
                            vNum = vivoNumbers[i]
                            lev = vivoLevels[i]
                            fos = 0
                            if (lev < moveLevels[vNum][0]):
                                fos = 1
                            elif (lev < moveLevels[vNum][1]):
                                fos = 2
                            elif (lev < moveLevels[vNum][2]):
                                fos = 3
                            else:
                                fos = 4
                            f.write(fos.to_bytes(2, "little"))
                        f.write(r[(0x70 + shift + (numVivos * 16) + (numVivos * 2)):])
                        f.close()
                        subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/battle_param/bin/" + mapN, "-c", "None", "-c",
                            "None", "-i", "0.bin", "-o", "NDS_UNPACK/data/battle_param/" + mapN ])
        shutil.rmtree("NDS_UNPACK/data/battle_param/bin/")
        
    if (res["color"] == "Yes"):    
        subprocess.run([ "fftool.exe", "NDS_UNPACK/data/etc/creature_palet_defs" ])
        f = open("NDS_UNPACK/data/etc/bin/creature_palet_defs/0.bin", "rb")
        r = f.read()
        f.close()
        f = open("NDS_UNPACK/data/etc/bin/creature_palet_defs/0.bin", "wb")
        f.close()
        f = open("NDS_UNPACK/data/etc/bin/creature_palet_defs/0.bin", "ab")
        f.write(r[0:12])
        pal = 0
        for i in range(12, len(r), 12):
            f.write(r[i:(i + 2)])
            pal = pal + 1
            if (pal == 6):
                pal = 7
            elif (pal > 0x1F):
                pal = 1
            f.write(pal.to_bytes(2, "little"))
            f.write(r[(i + 4):(i + 12)])
        f.close()
        
        subprocess.run([ "fftool.exe", "NDS_UNPACK/data/etc/creature_defs" ])
        f = open("NDS_UNPACK/data/etc/bin/creature_defs/0.bin", "rb")
        r = f.read()
        f.close()
        f = open("NDS_UNPACK/data/etc/bin/creature_defs/0.bin", "wb")
        f.close()
        f = open("NDS_UNPACK/data/etc/bin/creature_defs/0.bin", "ab")
        one = int.from_bytes(r[44:48], "little")
        f.write(r[0:one])
        for i in range(210):
            oldOffset = int.from_bytes(r[(44 + (i * 4)):(48 + (i * 4))], "little")
            newOffset = int.from_bytes(r[(48 + (i * 4)):(52 + (i * 4))], "little")
            if (i == 209):
                newOffset = len(r)
            f.write(r[oldOffset:(oldOffset + 0x46)])
            for j in range(4):
                v = random.randint(0, 0x276)
                f.write(v.to_bytes(2, "little"))
            f.write(r[(oldOffset + 0x4E):newOffset])
        f.close()

        subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/etc/bin/creature_defs/", "-i", "0.bin", "-o",
            "NDS_UNPACK/data/etc/creature_defs" ])
        subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/etc/bin/creature_palet_defs/", "-i", "0.bin", "-o",
            "NDS_UNPACK/data/etc/creature_palet_defs" ])
        shutil.rmtree("NDS_UNPACK/data/etc/bin/")
        
    if (res["anim"] == "Yes"):
        anims = list(range(1, 205))
        random.shuffle(anims)
        anims = [0] + anims
        subprocess.run([ "fftool.exe", "NDS_UNPACK/data/etc/creature_defs" ])
        f = open("NDS_UNPACK/data/etc/bin/creature_defs/0.bin", "rb")
        r = f.read()
        f.close()
        f = open("NDS_UNPACK/data/etc/bin/creature_defs/0.bin", "wb")
        f.close()
        f = open("NDS_UNPACK/data/etc/bin/creature_defs/0.bin", "ab")
        one = int.from_bytes(r[44:48], "little")
        f.write(r[0:one])
        for i in range(210):
            oldOffset = int.from_bytes(r[(44 + (i * 4)):(48 + (i * 4))], "little")
            newOffset = int.from_bytes(r[(48 + (i * 4)):(52 + (i * 4))], "little")
            if (i == 209):
                newOffset = len(r)
            f.write(r[oldOffset:(oldOffset + 0x42)])
            oldAnim = int.from_bytes(r[(oldOffset + 0x42):(oldOffset + 0x44)], "little")
            f.write(anims[oldAnim].to_bytes(2, "little"))
            f.write(r[(oldOffset + 0x44):newOffset])
        f.close()
        subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/etc/bin/creature_defs/", "-i", "0.bin", "-o",
            "NDS_UNPACK/data/etc/creature_defs" ])
        shutil.rmtree("NDS_UNPACK/data/etc/bin/")

    subprocess.run([ "dslazy.bat", "PACK", "out.nds" ])
    subprocess.run([ "xdelta3-3.0.11-x86_64.exe", "-e", "-f", "-s", sys.argv[1], "out.nds", "out.xdelta" ])
    psg.popup("You can now play out.nds!", font = "-size 12")


    