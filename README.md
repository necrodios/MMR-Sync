# MMR-Sync
A poorly cobbled together mess that synchronizes the items, equipment, masks, abilities, etc. of multiple users playing Majora's Mask via Retroarch. Primarily designed for multiple users to play a randomized rom cooperatively but it probably also works with the original one? Maybe?

## How to use it
1. Make sure that you have Network Commands enabled for Retroarch. This option can be found in Retroarch at Network > Network Commands.
2. Make sure that you have unzipped the files into a folder. The folder should contain Server.py, Client.py, Config.ini, and Items.py.
3. All users should open Config.ini and ensure that the Server IP is set to the IP address of the user who will run the server (the server is the program that will synchromnize everyone's data. It doesn't matter who runs it as long as everyone else can connect to it).
   - If this is not your first time using MMR Sync, you may have a file named MMR.json in the folder. This contains all of the data from your previous game, allowing you to continue it between multiple sessions. If you are starting a new game, delete this file before starting the server.
4. That user should run Server.py now.
4. Every user, including the one running the server, should start up Client.py now.

That's it.

## FAQ
### What exactly is synced between users?
If a player finds any of the following items, they will also be added to every other player's inventory:
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
Maybe in a future version.

### I don't like Retroarch, can I use something else?
Unfortunately, the client is only capable of communicating with Retroarch.<br />
The server, however, doesn't communicate directly with the emulator at all, so if somebody wishes to write a program or script for another emulator that sends the proper data to the server, it should be possible for that emulator to sync with the server.

### Your UI is bad! Make it prettier!
I'll consider making a proper UI when there's something worth displaying.

### I'm a programmer and this is the most horrifying thing I've ever laid my eyes on.
I smashed my face on a keyboard until something functional came out. I wrote a program that relies heavily on networking and I still don't actually understand how network protocols actually work. The amount of Python programs I've completed before this can be counted on one hand. The fact that this actually works is a miracle of the universe.
