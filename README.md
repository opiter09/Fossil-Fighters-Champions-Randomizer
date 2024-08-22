# Fossil-Fighters-Champions-Randomizer
This is a digsite, color, starter, and (hopefully) teams randomizer for FFC.

You MUST put the ROM in the same folder as the exe, or it won't work.

Features:
- You can only dig up the main 149
- Vivos are matched 1-to-1, so nothing is impossible to get
- Silver Fossils are also randomized among themselves
- The three vivosaurs listed in the box Post-Game Vivos, naturally, only appear post-game (so
  the Rainbow Canyon PTD, in FFC's case). These are Nigo, Krypto, Pacro, and Machai. All you
  need to do to change this is edit the text input, making sure to use the vivosaurs' line
  numbers in ffc_vivoNames.txt [1], and separating each by a comma and any number of spaces.
  Also, all entries after the 25th will be ignored
- The custom starters will use up to 5 values, for Aeros, Toba, Tsintao, Dimetro, and
  Tricera, in that order. These values can be from 1 to 210, except Tricera--the legendaries
  don't have fossils in FFC, so if you pick a number above 149 Tricera will turn into Dikelo
- Due to how text replacing works, you may see multiple starters listed as the same one in
  the rare case where one vanilla starter turns into another one that comes after it
  If that happens, you can consult the file "newStarters.txt" to see which is which
- I have absolutely no idea how to deal with Treasure Lake's variable fossils, so they have
  been replaced with the fossils for whoever replaces Tricera. It's okay, though, the
  starters are still available in Hot Spring Heights
- Because of this text editing, this randomizer will only work on the English version of the
  game, gomen'nasai
- The color randomization refers to the palette changes Super Fossils make. Due to
  complications with editing individual creature data, many vivosaurs which changed to
  the same palette before will change to the same different one after
- Team Randomization is HIGHLY experimental. If you get crashes on story fights, please
  let me know and...well I'll just have to disable it again, lol
- The teams randomization randomizes regular vivos, super evolvers, boneysaurs, and
  zombiesaurs among themselves. "True" legendaries (Zongazonga, Tonzilla, etc.) are
  entirely untouched
   
If you would like to see the table of new spawns, see the "ffc_digsiteOutput.txt" the
randomizer generates. Unlike FF1, we don't have map names associated to everything, so
you'll have to look at the shapes of the zone maps in FFC-E-Maps-Color.zip to figure out
which area is which.

Also, you download this by pressing the green "Code" button and choosing "Download ZIP," and
you run it by dragging and dropping an FFC ROM onto randomize.exe.

Finally, this normally only works on Windows. For Mac and Linux, I can only point you to
WINE: https://www.winehq.org

[1]: Because Champions, not every vivosaur's internal ID matches their Number shown in game.
It is much simpler to use the former, so just deal with having to open a text file once in 
a while.

# Source Codes
- FFTool: https://github.com/jianmingyong/Fossil-Fighters-Tool
- NDSTool: https://github.com/devkitPro/ndstool (this is a later version; the one used here came without a license as part of DSLazy)
- xdelta: https://github.com/jmacd/xdelta-gpl

