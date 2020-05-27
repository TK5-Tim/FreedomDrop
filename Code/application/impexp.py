#!/usr/bin/env python3
"""Import/Export module

This module contains the function definitions use for:
    - importing the peers Inventory (list of all the logs the peer has) and their
      Payload(all the peers logs relevant for us) as well as
    - exporting our own Inventory and Payload information during the exchange.
Functions contained in this module are:
    - file_len(fname)
    - createEntry()
    - processEntry()
    - createInventory()
    - sendInventory()
    - receivePeerInventory()
    - createPayload()
    - sendPayload()             TODO
    - receivePeerPayload()      TODO, Current implementation depracated
    - sendOk()                  TODO
    - terminate()               TODO
### NOTICE: Everything is still a work-in-progress functions in this module might later be
moved to a more appropriate module
### TODO: It would probably be good to create a Python method which turns .pcap files
into Python objects which can then be parsed and handled easier (i.e. JSON objects)
"""
from bluetooth import *
import lib.Tschudin.pcap as pcap
import cbor2
import hashlib
import subprocess
import difflib
from pathlib import Path
import os
from lib.Tschudin import event
from logMerge import LogMerge
from logMerge.PCAP import PCAP

payloadDir = "payload"
peerPayloadDir = "peerPayload"
lm = LogMerge.LogMerge()


def file_len(fname):
    """
    Function from Stack Overflow
    Simply returns the amount of lines in the given file fname
    It is possible that the file has to be a .txt
    """
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])


def filesize(fname):
    """
    Simply returns the size of the file fname in bytes
    """
    return (Path(fname).stat().st_size)


def importPCAP(fname):
    """
    Imports the pcap file in the specific format specified int the pcap.PCAP function from the demo files of Professor Tschudin.
    """
    log = pcap.PCAP(fname)
    return log


def importInventory(fname):
    """
    Imports a specifed txt-file.
    """
    inventory = open(fname)
    return inventory


'''
def createEntry(rawEntry):
    #return(entryTuple)
    pass

def processEntry(formattedEntry):
    """
    Please comment
    """
    try:
      if formattedEntry.seq_num == inventory[str(formattedEntry.feed_id)]:
          pass
    except KeyError:
      inventory[str(formattedEntry.feed_id)].append(formattedEntry)
'''


def createInventory():
    """
    writes the Inventory of all logs that are stored in a pcap file (fname) to the givent inventory file as txt.
    fname - pcap file
    inventroryDict - txt where the inventory should be stored in
    """
    status_dictionary = lm.get_database_status()
    return status_dictionary

def compareInventory(inventoryint, inventoryext):
    """
    Compares two txt-files who are intended as inventories of pcap files that log the different messages.
    At the moment it only compares the indexes
    TODO: Testing. Möglicherweise kleine Anpassungen LogMerge Connect
    """
    diff = {k: -1 for k in inventoryint if k not in inventoryext}
    diff_seq = {k: inventoryext[k] for k in inventoryint if k in inventoryext and inventoryext[k] < inventoryint[k]}
    diff.update(diff_seq)
    return diff

def sendInventory(inventory, socket):
    """

    """
    # TODO: MÖglichereweise Anpassen Logmerge
    try:
        inventory_keys = inventory.keys()
        inventory_vals = inventory.values()
        for key in inventory_keys:
            socket.send(key)
        socket.send(b'finkeys')
        for val in inventory_vals:
            socket.send(int.to_bytes(val, 1, "little"))
        socket.send(b'finvals')
    except Exception as e:
        print("Error: %s" % e)


def receivePeerInventory(socket):
    # socket is a BluetoothSocket, not an IP socket!!!
    # peerInventoryByteSize =
    # if peerInventoryByteSize != None:
    """
    Please comment
    """
    peer_key = list()
    peer_vals = list()
    try:
        keys = True
        while 1:
            receivedInventory = socket.recv(2048)
            if receivedInventory == b'finkeys':
                keys = False
            
            if receivedInventory == b'finvals':
                return

            if keys:
                peer_key.append(receivedInventory)
            else:
                peer_vals.append(int.from_bytes(receivedInventory, byteorder= "little"))
    
    except BluetoothError:
        print(f"<Bluetooth error: {BluetoothError}>")
    except Exception as e:
        print("Error: %s" % e)
    
    peerInventory = dict(zip(peer_key, peer_vals))

    return peerInventory


def createPayload(inventoryint, inventoryext):
    """
    creates payload pcap file with the missing pcap files for the peer.
    """
    # TODO: Anbindung LogMerge Methode export_logs
    diff = compareInventory(inventoryint, inventoryext)
    lm.export_logs("payload", diff)


def handlePayload():
    """
    takes the Payload of the peer specified for the local log and writes
    """
    lm.import_logs(peerPayloadDir)
    print("<wrote peerPayload to log>")



def sendPayload(socket):
    """
    Please comment
    """
    # TODO: Implement and test
    try:
        if not os.listdir("payload"):
            socket.send(b"False")
            print("<no payload to sent>")
            return

        # payload exists
        socket.send(b"True")
        for file in os.listdir("payload"):
            socket.send(file.encode('utf-8'))
            packets_list = PCAP.read_pcap(file)
            for packet in packets_list:
                socket.send(packet)
            socket.send(b'EOF')
        socket.send(b"fin")
    except Exception as e:
        print("Error: %s" % e)


def receivePeerPayload(socket):
    """
    Please comment
    """
    # Current code already deprecated
    # TODO: Implement and test
    payloadInfo = socket.recv(4096)

    if payloadInfo == b"False": 
        print("<no payload expected. logs are up to date.>")
        return 0

    packets_list = list()
    
    try:
        peerPayloadLines = socket.recv(4096)
        filename = peerPayloadLines.decode('utf-8')
        while 1:
            peerPayloadLines= socket.recv(4096)  # receive using socket
            if peerPayloadLines:
                if peerPayloadLines == b"EOF":
                    PCAP.write_pcap("peerPayload/" + filename, packets_list)
                    packets_list.clear()
                    filename = peerPayloadLines.decode('utf-8')
                if peerPayloadLines == b"fin":
                    return 1
                packets_list.append(peerPayloadLines)
        
    except BluetoothError:
        print(f"<Bluetooth error: {BluetoothError}>")
    except Exception as e:
        print("Error #1: %s" % e)

"""
    if dataReceivedFromPeer:
        for entry in dataReceivedFromPeer:
            formattedEntry = createEntry(entry)
            processEntry(formattedEntry)
        peerPayload = "???"
        return(True,peerPayload)
    else:
        return(False,"")
"""

def cleanUpPayloads():
    for file in os.listdir("peerPayload"):
        os.remove("peerPayload/" + file)
    for file in os.listdir("payload"):
        os.remove("payload/" + file)
    

def sendOk():
    pass


def terminate():
    pass
