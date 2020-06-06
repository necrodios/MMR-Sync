#ADDRESSES_TO_SYNC
ITEMS = ["1EF6E0", "1EF6E1", "1EF6E2", "1EF6E3", "1EF6E4", "1EF6E5", "1EF6E7", "1EF6E9", "1EF6EA", "1EF6EB", "1EF6EC", "1EF6ED", "1EF6EE", "1EF6EF", "1EF6F3"]
MASKS = ["1EF6F8", "1EF6F9", "1EF6FA", "1EF6FB", "1EF6FC", "1EF6FD", "1EF6FE", "1EF6FF", "1EF700", "1EF701", "1EF702", "1EF703", "1EF704", "1EF705", "1EF706", "1EF707", "1EF708", "1EF709", "1EF70A", "1EF70B", "1EF70C", "1EF70D", "1EF70E", "1EF70F"]
MAGIC = ["1EF6AB", "1EF6B2", "1EF6B3", "1F359C"]
STRAY_FAIRIES = ["1EF744", "1EF745", "1EF746", "1EF747"]
SKULLTULAS = ["1F0530", "1F0532"]
DOUBLE_DEFENSE = ["1EF6B1", "1EF740"]

GREAT_FAIRYS_SWORD = "1EF6F3" #included in the ITEMS, but also separate because it needs an extra exception

#ADDRESSES_TO_MERGE
SONGS = ["1EF72C", "1EF72D", "1EF72E"]
OWL_STATUES = ["1EF6B4", "1EF6B5"]

#bitflags
GREAT_SPIN_ATTACK = {"1F057C": 1} #00000010
CT_STRAY_FAIRY = {"1F0573": 7} #10000000
FLAGS = {**GREAT_SPIN_ATTACK, **CT_STRAY_FAIRY}

#splitbytes
SHIELDSWORD = {"1EF6DE": 4} #0010 0011
BOMBARROW = {"1EF728": 3} #00011 011
WALLET = {"1EF729": 4} #0010 ????
EQUIPMENT = {**SHIELDSWORD, **BOMBARROW, **WALLET}

#Things that require unique calculations/conditions
BOTTLES = ["1EF6F1", "1EF6F0", "1EF6F7", "1EF6F6", "1EF6F5", "1EF6F4"]
HEART_CONTAINERS = ["1EF6A6", "1EF6A7"]

#Things that aren't currently synchronized
QUEST_ITEMS = ["1EF6E6", "1EF6E8", "1EF6F2"]

#Miscellaneous addresses
LOADED_FILE = "1F3310"
STOLEN_ITEM = "1F0547"
HUMAN_B_BUTTON_ITEM = "1EF6BF"
DEKU_B_BUTTON_ITEM = "1EF6CB"

ADDRESSES_TO_SYNC = ITEMS + MASKS + MAGIC + STRAY_FAIRIES + SKULLTULAS + DOUBLE_DEFENSE
ADDRESSES_TO_MERGE = SONGS + OWL_STATUES