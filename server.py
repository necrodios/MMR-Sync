import socket
import json
import os.path
import sys
from time import sleep

import Items

datafile = os.path.join(sys.path[0], "MMR.json")
serverIP = (input("Enter Server IP: "), 50000)

mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mysocket.settimeout(10.0)

def send(target, message):
    mysocket.sendto(message.encode('utf-8'), target)

def receive():
    mysocket.bind(serverIP)
    print("Bound to port:" + str(mysocket.getsockname()))
    while True:
        try:
            data, server = mysocket.recvfrom(1024)
            comparedata(json.loads(data), server)
            print("Received data from " + str(server))
        except socket.timeout:
            pass

def writefile(file, data):
    f = open(file, "w")
    f.write(json.dumps(data, indent="\t", sort_keys=True))
    f.close()

def readfile(file):
    try:
        f = open(file, "r")
        return json.loads(f.read())
        f.close()
    except FileNotFoundError:
        print("\"MMR.json\" not found. A new dictionary will be created.")
        return {}

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

def comparedata(clientdata, clientIP):
    global serverdata
    newdata = False
    def updateifbetter(i, data):
        global serverdata
        nonlocal newdata
        if data > serverdata[i]: #if we have an upgrade that the server doesn't
            serverdata[i] = data
            newdata = True
    
    for i in clientdata:
        if i in Items.ADDRESSES_TO_SYNC:
            if i not in serverdata: #if the server doesnt have a value for this yet
                serverdata[i] = -1
            updateifbetter(i, clientdata[i])
        
        if i in Items.ADDRESSES_TO_MERGE:
            if i not in serverdata: #if the server doesnt have a value for this yet
                serverdata[i] = 0
            mergeddata = clientdata[i] | serverdata[i]
            updateifbetter(i, mergeddata)

        if i in Items.EQUIPMENT:
            bitshift = Items.EQUIPMENT[i]
            bitshift = Items.EQUIPMENT[i]
            if i not in serverdata: #if the server doesnt have a value for this yet
                serverdata[i] = 0
            rombytes = splitbyte(clientdata[i], bitshift)
            serverbytes = splitbyte(serverdata[i], bitshift)
            mergeddata = mergebyte(max(rombytes[0], serverbytes[0]),max(rombytes[1], serverbytes[1]), bitshift)
            updateifbetter(i, mergeddata)
        
        if i in Items.FLAGS:
            if i not in serverdata: #if the server doesnt have a value for this yet
                serverdata[i] = 0
            updateifbetter(i, clientdata[i])
                
        if i in {"Bottles", "HeartContainers"}:
            if i not in serverdata: #if the server doesnt have a value for this yet
                serverdata[i] = 0
            updateifbetter(i, clientdata[i])
    
    if "DataVersion" not in serverdata: #if the server doesnt have a value for this yet
            serverdata["DataVersion"] = clientdata["DataVersion"]
            newdata = True

    if newdata: 
        serverdata["DataVersion"] += 1
        writefile(datafile, serverdata)
        
    if clientdata["DataVersion"] < serverdata["DataVersion"]:
        send(clientIP, json.dumps(serverdata))

serverdata = readfile(datafile)
receive()