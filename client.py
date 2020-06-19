import socket
import json
import os.path
import sys
from time import sleep
import configparser

import Items

config = configparser.ConfigParser()
config.read(os.path.join(sys.path[0], 'config.ini'))

serverIP = (config['Server']['ip'], 
            config['Server'].getint('port'))
retroarchIP = (config['Retroarch']['ip'], 
               config['Retroarch'].getint('port'))

print("Server IP: " + str(serverIP))
print("Retroarch IP: " + str(retroarchIP))

romdata = {'DataVersion': 0} #romdata = {}
serverdata = {'DataVersion': 0}
mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mysocket.settimeout(10.0)

def readloop():
    pingserver(romdata)
    while True:
        sleep(5)
        comparedata()

def send(target, message):
    mysocket.sendto(message.encode('utf-8'), target)

def readaddress(address, numtoread):
    send(retroarchIP, 'READ_CORE_RAM ' + address  + ' ' + str(numtoread))
    try:
        data, server = mysocket.recvfrom(1024)
        return data.split()[2:]
    except socket.timeout:
        print('No response received from Retroarch.')
        return b"[-1]"*numtoread
    except ConnectionResetError:
        print("Cannot connect to Retroarch")
        return [b"-1"]*numtoread

def writeaddress(address, value):
    send(retroarchIP, 'WRITE_CORE_RAM ' + address  + ' ' + hex(value)[2:])

def readrom(start, end):
    totaladdresses = end - start + 1
    addresses = readaddress(hex(start), totaladdresses)
    for i in range(totaladdresses):
        romdata[hex(start + i)[2:].upper()] = int(addresses[i].decode('utf-8'),16)

def pingserver(sentdata):
    global serverdata
    send(serverIP, json.dumps(sentdata))
    try:
        data, server = mysocket.recvfrom(1024)
        serverdata = json.loads(data)
        print("Data sent to " + str(serverIP))
    except ConnectionResetError:
        print("Cannot connect to server")
        sleep(5)
        pingserver(sentdata)
    except socket.timeout:
        pass

def comparedata():
    global romdata
    global serverdata

    readrom(0x1F3310, 0x1F3310)
    if romdata[Items.LOADED_FILE] in {0,1}: #Only run this if a proper file is actually loaded
        readrom(0x1EF6A6, 0x1EF747)
        readrom(0x1F0530, 0x1F057C)
        readrom(0x1F359C, 0x1F359C)
        newdata = {'DataVersion': romdata['DataVersion']}
        for i in Items.ADDRESSES_TO_SYNC:
            if romdata[i] == 0xFF: #if the romdata has a value of 0xFF, we want it to be treated as lower than a non-0xFF number
                romdata[i] = -1
            if i not in serverdata or serverdata[i] == 0xFF: #if the server doesnt have a value for this yet, or if that value is 0xFF
                serverdata[i] = -1
            if (i == Items.GREAT_FAIRYS_SWORD and romdata[Items.STOLEN_ITEM] == 0x10): #if we're comparing the GFS, and it's been stolen, compare as if we still have it
                romdata[i] = 0x10
            if romdata[i] > serverdata[i]: #if we have an upgrade that the server doesn't
                newdata[i] = romdata[i]
            elif romdata[i] < serverdata[i]: #if the server has an upgrade that we don't
                writeaddress(i, serverdata[i])
                if i == Items.MAGIC[0] and Items.DEKU_B_BUTTON_ITEM == 0xFD: #if we're getting magic for the first time, we have to manually enable the Deku bubbles
                    writeaddress(Items.DEKU_B_BUTTON_ITEM, 0x09)
    
        for i in Items.ADDRESSES_TO_MERGE:
            if i not in serverdata: #if the server doesnt have a value for this yet
                serverdata[i] = 0
            if romdata[i] == -1: #if the romdata had a null value during read, treat it as 0
                romdata[i] = 0
            mergeddata = romdata[i] | serverdata[i]
            if mergeddata > serverdata[i]: #if we have an upgrade that the server doesn't
                newdata[i] = mergeddata
            if mergeddata > romdata[i]: #if the server has an upgrade that we don't
                writeaddress(i, mergeddata)
    
        for i in Items.EQUIPMENT:
            bitshift = Items.EQUIPMENT[i]
            if i not in serverdata: #if the server doesnt have a value for this yet
                serverdata[i] = 0
            if romdata[i] == -1: #if the romdata had a null value during read, treat it as 0
                romdata[i] = 0
            rombytes = splitbyte(romdata[i], bitshift)
            serverbytes = splitbyte(serverdata[i], bitshift)
            comparingsword = (i in Items.SHIELDSWORD)
            if comparingsword and romdata[Items.STOLEN_ITEM] >= 0x4D: #if we're comparing the sword, and it's been stolen, compare as if we still have it
                rombytes[1] = romdata[Items.STOLEN_ITEM] - 0x4C
            mergeddata = mergebyte(max(rombytes[0], serverbytes[0]),max(rombytes[1], serverbytes[1]), bitshift)
            if mergeddata > serverdata[i]: #if we have an upgrade that the server doesn't
                newdata[i] = mergeddata
            if mergeddata > romdata[i]: #if the server has an upgrade that we don't
                if comparingsword:
                    bettersword = (rombytes[1] < serverbytes[1])
                    if romdata[Items.STOLEN_ITEM] >= 0x4D: #if the sword is stolen, don't readd it to the inventory, update the stolen version instead
                        mergeddata = mergebyte(max(rombytes[0], serverbytes[0]),0)
                        if bettersword:
                            writeaddress(Items.STOLEN_ITEM, serverbytes[1] + 0x4C)
                    elif bettersword and romdata[Items.HUMAN_B_BUTTON_ITEM] in {0x4D, 0x4E, 0x4F, 0xFF}: #if we got a better sword and we have a sword (or nothing) equipped
                        writeaddress(Items.HUMAN_B_BUTTON_ITEM, serverbytes[1] + 0x4C) #update our equipped sword, since the game won't do it automatically
                writeaddress(i, mergeddata)

        for i in Items.FLAGS:
            bitshift = Items.FLAGS[i]
            if romdata[i] == -1: #if the romdata had a null value during read, treat it as 0
                romdata[i] = 0
            romrawdata = romdata[i]
            romdata[i] = getflag(romrawdata, bitshift)
            if i not in serverdata: #if the server doesnt have a value for this yet
                serverdata[i] = 0
            if romdata[i] > serverdata[i]: #if we have an upgrade that the server doesn't
                newdata[i] = romdata[i]
            elif romdata[i] < serverdata[i]: #if the server has an upgrade that we don't
                writeaddress(i, romrawdata | serverdata[i])
                

        romdata["Bottles"] = sum(romdata[i] not in {0xFF,-1} for i in Items.BOTTLES) + (romdata[Items.STOLEN_ITEM] == 0x12) #count the bottle slots, plus any stolen bottle
        if "Bottles" not in serverdata: #if the server doesnt have a value for this yet
            serverdata["Bottles"] = 0
        if romdata["Bottles"] > serverdata["Bottles"]: #if we have more bottles than the server
            newdata["Bottles"] = romdata["Bottles"]
        elif romdata["Bottles"] < serverdata["Bottles"]: #if we have less bottles than the server
            missingbottles = serverdata["Bottles"] - romdata["Bottles"]
            for i in Items.BOTTLES:
                if missingbottles > 0 and romdata[i] == 0xFF:
                    writeaddress(i, 0x12)
                    missingbottles -= 1
                    
        for i in Items.HEART_CONTAINERS:
            if romdata[i] == -1: #if the romdata had a null value during read, treat it as 0
                romdata[i] = 0
        romdata["HeartContainers"] = romdata[Items.HEART_CONTAINERS[0]] + (romdata[Items.HEART_CONTAINERS[1]]*0x100)
        if "HeartContainers" not in serverdata: #if the server doesnt have a value for this yet
            serverdata["HeartContainers"] = 0
        if min(romdata["HeartContainers"], 320) > serverdata["HeartContainers"]: #if we have more hearts than the server
            newdata["HeartContainers"] = romdata["HeartContainers"]
        if romdata["HeartContainers"] > 320: #if we have more hearts than we're supposed to, do some janky shit to fix that
            romdata["HeartContainers"] = 0
            serverdata["HeartContainers"] = 320
        if romdata["HeartContainers"] < serverdata["HeartContainers"]: #if we have less hearts than the server
            writeaddress(Items.HEART_CONTAINERS[0], serverdata["HeartContainers"] & 0xFF)
            writeaddress(Items.HEART_CONTAINERS[1], serverdata["HeartContainers"] >> 8)
        
        if romdata["DataVersion"] < serverdata["DataVersion"]:
            romdata["DataVersion"] = serverdata["DataVersion"]
            
        pingserver(newdata)

def splitbyte(value,bits):
    leftbyte = value >> bits & (2**bits-1)
    rightbyte = value & (2**bits-1)
    return [leftbyte, rightbyte]

def mergebyte(leftbyte, rightbyte, bits):
    return (leftbyte<<bits) + rightbyte

def getflags(value):
    flags = []
    for _ in range(8):
        flags = [value & 1] + flags
        value >>= 1
    return flags or [0]

def getflag(value,bit):
    return value & (2**bit)

readloop()
