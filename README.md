# Fossil-Fighters-Champions-Randomizer
This is a digsite and teams randomizer for FFC.

Features:
- You can only dig up the main 149
- Vivos are matched 1-to-1, so nothing is impossible to get
- The three vivosaurs listed in the box Post-Game Vivos, naturally, only appear post-game (so
  the Rainbow Canyon PTD, in FFC's case). These are Nigo, Krypto, Pacro, and Machai. All you
  need to do to change this is edit the text input, making sure to use the vivosaurs' line
  numbers in ffc_vivoNames.txt [1], and separating each by a comma and any number of spaces.
  Also, all entries after the 25th will be ignored
- DP vivos can, in fact, be dug up, and other things can turn into DP vivos accordingly,
  since I actually know where they are in FFC
- There is an option to also disallow Post-Game vivos from appearing on randomized teams,
  because if they're broken then I mean it's no fun if the enemy has 3. Other than that
  and not including or affecting Legendaries and DLC, the team randomization has no rules
- The Allo fight and all scripted battles (e.g. Rupert vs. Todd) will not be touched at
  all, both because they break if edited, and to maintain some lore-friendliness

Also, you download this by pressing the green "Code" button and choosing "Download ZIP," and
you run it by dragging and dropping an FFC ROM onto randomize.exe. You MUST put the ROM in
the same folder as the exe, or it won't work.

Finally, this normally only works on Windows. For Mac and Linux, I can only point you to
WINE: https://www.winehq.org

TIP: If the game crahses/hangs anywhere, and you have run the randomizer previously,
try manually removing the NDS_UNPACK folder, then running it again.


[1]: Because Champions, not every vivosaur's internal ID matches their Number shown in game.
It is much simpler to use the former, so just deal with having to open a text file once in 
a while.
