# MMR-Sync
A poorly cobbled together mess that synchronizes the items, equipment, masks, abilities, etc. of multiple users playing Majora's Mask via Retroarch. Primarily designed for multiple users to play a randomized rom cooperatively but it probably also works with the original one? Maybe?

## How to use it
1. Make sure that you have Network Commands enabled for Retroarch. This option can be found in Retroarch at Network > Network Commands.
2. Make sure that you have unzipped the files into a folder. The folder should contain Server.py, Client.py, and Items.py.
3. One user should start up Server.py and input their IP address (or the IP address of a Hamachi server if applicable).
   - If this is not your first time using MMR Sync, you may have a file named MMR.json in the folder. This contains all of the data from your previous game, allowing you to continue it between multiple sessions. If you are starting a new game, delete this file before starting the server.
4. Every user, including the one running the server, should start up Client.py and input the same IP address used in the previous step.

That's it.

## FAQ
### What exactly is synced between users?
If a player finds any of the following items, they will also be added to every other players inventory:
* Ocarina of Time
* Hero's Bow
* Fire Arrow
* Ice Arrow
* Light Arrow
* Bomb
* Bombchu
* Deku Stick
* Deku Nut
* Magic Beans
* Powder Keg
* Pictograph box
* Lens of Truth
* Hookshot
* Great Fairy's Sword
* Bottles (but not bottle contents)
* Any Masks
* Any Songs
* Sword
* Shield
* Quiver
* Bomb Bag
* Wallet
* Complete Heart Containers (but not individual Heart Pieces)
* Magic Meter
* Great Spin Attack
* Double Defense
* Bomber's Notebook (but not completed quests)
* Boss remains
* Owl statues activated
* Total Stray Fairies collected
* Total Skulltula tokens collected

The following things are NOT synced:
* Moon's Tear
* Title Deeds
* Room Key
* Letter to Kafei
* Pendant of Memories
* Priority Mail
* rupees (including rupees in the bank)
* ammo
* Heart Pieces
* Bottle contents

### My friend found a sword and now my B Button has a weird garbled image on it!
Yeah, that happens. You should still be able to use the sword normally, and the image will fix itself when you enter a new area.

### Me and my friends started a new game, but we already have a whole bunch of items for some reason!
Make sure that you delete MMR.json before starting the server. Otherwise it will give you everything that you had the last time you played.

### You should sync quest items, like the Title Deeds and Room Key.
If an option to make them permanent is ever added to the randomizer, then an option to sync them will probably be added to this as well.

### Your UI is bad! Make it prettier!
I can't make the UI prettier if the program doesn't actually have one :)

### I'm a programmer and this is the most horrifying thing I've ever laid my eyes on.
I smashed my face on a keyboard until something functional came out. I wrote a program that relies heavily on networking and I still don't actually understand how network protocols actually work. The amount of Python programs I've completed before this can be counted on one hand. The fact that this actually works is a miracle of the universe.
