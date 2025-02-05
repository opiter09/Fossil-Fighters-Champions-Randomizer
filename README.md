# Fossil-Fighters-Champions-Randomizer
This is a digsite, color, starter, and teams randomizer for FFC.

You download this by pressing the green "Code" button and choosing "Download ZIP", and
you run it by dragging and dropping an FFC ROM onto "randomize.exe". Note that you MUST put
the ROM in the same folder as the exe, or it won't work.

Furthermore, this is only designed for Windows. For Mac and Linux, I can only point you to
WINE: https://www.winehq.org

After running the randomizer, you should receive the output ROM "out.nds". If this does not
occur, try dragging your ROM onto "DRAG_HERE_TO_SEE_ERRORS.bat" instead of "randomize.exe",
and running the randomizer again. If this yields an error message that includes a line
beginning with "PermissionError", try removing the folder "NDS_UNPACK", then drag your
ROM onto "DRAG_HERE_TO_SEE_ERRORS.bat" and try again. If this still yields a "PermissionError",
try moving the randomizer folder into your Downloads folder (if it is not there already),
removing the folder "NDS_UNPACK", and dragging your ROM onto "DRAG_HERE_TO_SEE_ERRORS.bat"
again. If you receive an error message even after that (or receive a non-"PermissionError"
message after the prior attempt), please take a screenshot of it and either post it into
the #secret-lab channel of the Fossil Fighters Discord
(https://disboard.org/server/213792669569253376), or create an Issue here on GitHub.

NOTE: If the game freezes at the Nintendo logo, this is most likely an issue with the
base ROM you are using, not the randomizer. You will have to legally acquire a ROM from
somewhere else in this case.

Features:
- You can only dig up the main 149
- Vivos are matched 1-to-1, so nothing is impossible to get
- Silver Fossils are also randomized among themselves
- Vivos which replace single-fossil ones (curious or giant) will only spawn their heads. This
  was deemed the least intrusive option, I'm afraid
- "Team Level Change:" raises or lowers (you can use negatives with a "-") the levels of all
  vivosaurs in all enemy teams. If you set "TLC on Nameless?" to "No", this will not affect
  random fighters (i.e. the ones named "Fossil Fighter")
- The six vivosaurs listed in the box Post-Game Vivos, naturally, only appear post-game (so
  the Rainbow Canyon PTDs, in FFC's case). These are Zino, Centro, Nigo, Krypto, Pacro, and
  Machai. All you need to do to change this is edit the text input, making sure to use the
  vivosaurs' line numbers in "ffc_vivoNames.txt"/"ffc_vivoNames_j.txt" [1], and separating
  each by a comma and any number of spaces. Also, all entries after the 25th will be ignored
- Related to this, setting "PGV's in Teams" to "Yes" will allow the Post-Game Vivos to appear
  in randomized enemy teams (if that feature is enabled). Otherwise, they will not show up
  anywhere
- The custom starters will use up to 5 values, for Aeros, Toba, Tsintao, Dimetro, and
  Tricera, in that order. These values can be from 1 to 210, except Tricera--the legendaries
  don't have fossils in FFC, so if you pick a number above 149 Tricera will turn into Dikelo
- If you are confused by the long names used in the game, you can consult the file
  "newStarters.txt" to see what the new starters are
- I have absolutely no idea how to deal with Treasure Lake's variable fossils, so they have
  been replaced with the fossils for whoever replaces Tricera. It's okay, though, the
  starters are still available in Hot Spring Heights
- Because I don't speak Japanese, the text editing part is ignored when randomizing Japanese
  ROMs. Therefore, in that case you will also have to consult the file "newStarters.txt". I was,
  however, able to make the names in there be Japanese if your ROM is, so that's nice
- As a further FFC-specific Japanese support problem, the anti-piracy fix I apply was made for
  the American ROM. Therefore, there is a good chance that a randomized Japanese ROM will freeze
  at the Rupert/Todd tutorial while playing on TwilightMenu++. If this comes up, you should be
  able to transfer your save to your computer, play through the segment on MelonDS, and then
  transfer the save back
- Mono-Spawn Mode makes it so each map [2] only spawns one vivo (along with jewels, Silver
  Fossils, etc.). However, to ensure all of its fossils are available whoever replaces
  Tricera still spawns in Treasure Lake instead of the variable fossils
- Said vivo is the first found in the file, so some related maps will have the same one, and
  others won't. Also, to be clear, with this on you will not be able to get every vivosaur
- The color randomization refers to the palette changes Super Fossils make. This does not
  change the VMM or lower-screen battle sprites, however, because that would be basically
  impossible to automate lol
- Particle randomizing changes an unusual value in each vivosaur's data which controls
  their moves' particle effects, camera positions, and how many hits/damage values are
  shown. This will not effect the motions of the vivosaur itself, since that is
  tied to the model, so really this is more of a joke option than anything else (it was
  requested on the Fossil Fighters Discord)
- The teams randomization randomizes regular vivos, super evolvers, boneysaurs, and
  zombiesaurs among themselves. "True" legendaries (Zongazonga, Tonzilla, etc.) are
  entirely untouched. Note that each vivosaur is randomized separately, not shuffled
  around as with the fossils
   
Finally, if you would like to see the table of new spawns, see the "newDigsiteSpawns.txt" the
randomizer generates. Unlike FF1, we don't have map names associated to everything, so
you'll have to look at the shapes of the zone maps in "FFC-E-Maps-Color.zip" to figure out
which area is which.

[1]: Because Champions, not every vivosaur's internal ID matches their Number shown in game.
It is much simpler to use the former, so just deal with having to open a text file once in 
a while.

[2]: I mean this in the more internal sense of "a continuous area with no loading zones in
between", not a whole digsite.

# Source Codes
- FFTool: https://github.com/jianmingyong/Fossil-Fighters-Tool
- NDSTool: https://github.com/devkitPro/ndstool (this is a later version; the one used here came without a license as part of DSLazy)
- xdelta: https://github.com/jmacd/xdelta-gpl

