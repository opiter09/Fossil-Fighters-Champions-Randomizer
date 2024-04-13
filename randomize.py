import os
import shutil
import subprocess
import random
import sys
import PySimpleGUI as psg

def digsiteOutput():
    text = open("ffc_digsiteOutput.txt", "wt")
    text.close()
    text = open("ffc_digsiteOutput.txt", "at")
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
                    text.write("Zone " + str(index).zfill(2) + ":\n")
                    # maxFos = int.from_bytes(r[(val + 12):(val + 16)], "little")
                    # text.write("\tMax Spawns: " + str(maxFos) + "\n")
                    numTables = int.from_bytes(r[(val + 12):(val + 16)], "little")
                    point3 = int.from_bytes(r[(val + 16):(val + 20)], "little")
                    for i in range(numTables):
                        text.write("\tFossil Chip " + str(i) + ":\n")
                        point4 = int.from_bytes(r[(val + point3 + (i * 4)):(val + point3 + (i * 4) + 4)], "little")
                        point5 = int.from_bytes(r[(val + point4 + 12):(val + point4 + 16)], "little")
                        numWeird = int.from_bytes(r[(val + point4 + point5 + 8):(val + point4 + point5 + 12)], "little")
                        numSpawns = int.from_bytes(r[(val + point4 + point5 + 16):(val + point4 + point5 + 20)], "little")
                        startSpawns = val + point4 + point5 + 24 + (numWeird * 2)
                        for j in range(numSpawns):
                            thisStart = startSpawns + (j * 8)
                            vivoNum = int.from_bytes(r[(thisStart + 2):(thisStart + 4)], "little")
                            # chance = int.from_bytes(r[(val + point4 + 4):(val + point4 + 8)], "little")
                            text.write("\t\t" + "[0x" + hex(thisStart + 2).upper()[2:] + "] " + vivoNames[vivoNum] + "\n")
                if (check == 1):
                    text.write("\n")
    text.close()

layout = [
    [ psg.Text("Randomize Fossils?", size = 17), psg.Button("Yes", key = "dig", size = 5) ],
    [ psg.Text("Randomize Teams?", size = 17), psg.Button("No", key = "team", size = 5) ],
    [ psg.Text("Randomize Colors?", size = 17), psg.Button("No", key = "color", size = 5) ],
    [ psg.Text("Post-Game Vivos:", size = 17), psg.Input(default_text = "105, 114, 119, 128", key = "broken",
        size = 20, enable_events = True) ],
    [ psg.Text("PGV's in Teams?", size = 17), psg.Button("No", key = "include", size = 5) ],
    [ psg.Text("Team Level Change:", size = 17), psg.Input(default_text = "0", key = "level", size = 5, enable_events = True) ],
    [ psg.Text("TLC on Nameless?", size = 17), psg.Button("Yes", key = "jewel", size = 5) ],
    [ psg.Button("Run") ]
]
window = psg.Window("", layout, grab_anywhere = True, resizable = True, font = "-size 12")
good = 0
res = { "dig": "Yes", "include": "No", "team": "No", "color": "No", "jewel": "Yes" }
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
        
    vivoNames = list(open("ffc_vivoNames.txt", "rt").read().split("\n")[0:149])
    fossilNames = list(open("ffc_kasekiNames.txt", "rt").read().split("\n"))
    fossilTable = { "Head": [0], "Body": [0], "Arms": [0], "Legs": [0] }
    for v in vivoNames:
        for k in fossilTable.keys():
            if ((v + " " + k) in fossilNames):
                fossilTable[k].append(fossilNames.index(v + " " + k))
            else:
                fossilTable[k].append(fossilNames.index(v + " Single"))
    # print(fossilTable["Head"])

    if (os.path.exists("NDS_UNPACK/y7.bin") == True):
        shutil.rmtree("./NDS_UNPACK/")
    if (os.path.exists("out.nds") == True):
        os.remove("out.nds")
    subprocess.run([ "dslazy.bat", "UNPACK", sys.argv[1] ])
    
    if (res["dig"] == "Yes"):
        subprocess.run([ "fftool.exe", "NDS_UNPACK/data/map/m" ])
        for root, dirs, files in os.walk("NDS_UNPACK/data/map/m/bin"):
            for file in files:
                if (file == "0.bin"):
                    used = {}
                    f = open(os.path.join(root, file), "rb")
                    r = f.read()
                    f.close()
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
                    singles = {}
                    for fos in fossilTable["Head"]:
                        singles[fos] = -1
                    for i in range(0, len(r), 2):
                        if (i in used.keys()):
                            check = 0
                            temp = ["Head", "Body", "Arms", "Legs"]
                            for p in temp:
                                if (used[i] in fossilTable[p]):
                                    if (fossilNames[used[i]].endswith("Single") == True):
                                        singles[used[i]] = singles[used[i]] + 1
                                        if (singles[used[i]] >= 4):
                                            singles[used[i]] = 0
                                        old = fossilTable[p].index(used[i])
                                        new = fossilTable[temp[singles[used[i]]]][vivos[old]]
                                        # print(fossilNames[used[i]])
                                        # print(fossilNames[new])
                                        # print("\n")
                                    else:
                                        old = fossilTable[p].index(used[i])
                                        new = fossilTable[p][vivos[old]]
                                    f.write(new.to_bytes(2, "little"))
                                    check = 1
                                    break
                                elif (used[i] in [900, 901, 902, 903]):
                                    new = random.randint(900, 903)
                                    f.write(new.to_bytes(2, "little"))
                                    check = 1
                                    break
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
                        for i in range(numVivos):
                            vivoNum = int.from_bytes(r[(0x70 + shift + (i * 12)):(0x70 + shift + (i * 12) + 2)], "little")
                            listOfLists = [ [1, 149], [150, 179], [180, 183], [184, 190] ]
                            check = 0
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
                                f.write(r[(0x70 + shift + (i * 12)):(0x70 + shift + (i * 12) + 2)])
                            if (levelR != 0):
                                oldLevel = int.from_bytes(r[(0x70 + shift + (i * 12) + 2):(0x70 + shift + (i * 12) + 4)], "little")
                                newLevel = max(1, min(oldLevel + levelR, 20))
                                f.write(newLevel.to_bytes(2, "little"))
                            else:
                                f.write(r[(0x70 + shift + (i * 12) + 2):(0x70 + shift + (i * 12) + 4)])
                            f.write(r[(0x70 + shift + (i * 12) + 4):(0x70 + shift + (i * 12) + 12)])
                        f.write(r[(0x70 + shift + (numVivos * 12)):(0x70 + shift + (numVivos * 16))])
                        # for i in range(numVivos):
                            # f.write((4).to_bytes(2, "little"))
                        f.write(r[(0x70 + shift + (numVivos * 16)):])
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
        for i in range(12, len(r), 12):
            f.write(r[i:(i + 2)])
            pal = 6
            while (pal == 6):
                pal = random.randint(1, 0x1F)
            f.write(pal.to_bytes(2, "little"))
            f.write(r[(i + 4):(i + 12)])
        f.close()
        subprocess.run([ "fftool.exe", "compress", "NDS_UNPACK/data/etc/bin/creature_palet_defs/", "-i", "0.bin", "-o",
            "NDS_UNPACK/data/etc/creature_palet_defs" ])
        shutil.rmtree("NDS_UNPACK/data/etc/bin/")

    subprocess.run([ "dslazy.bat", "PACK", "out.nds" ])
    subprocess.run([ "xdelta3-3.0.11-x86_64.exe", "-e", "-f", "-s", sys.argv[1], "out.nds", "out.xdelta" ])
    psg.popup("You can now play out.nds!", font = "-size 12")


    