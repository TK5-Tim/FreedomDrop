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
import lib.pcap as pcap
import cbor2
import hashlib
import subprocess
import difflib
from pathlib import Path

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
    return(Path(fname).stat().st_size)

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


def createInventory(fname, inventoryDict):
    """
    writes the Inventory of all logs that are stored in a pcap file (fname) to the givent inventory file as txt.
    fname - pcap file
    inventroryDict - txt where the inventory should be stored in
    TODO: work with hashes of log.
    """
    log = importPCAP(fname)
    log.open('r')
    inventory = open(inventoryDict,'w+')
    for w in log:
        e = cbor2.loads(w)
        href = hashlib.sha256(e[0]).digest()
        e[0] = cbor2.loads(e[0])
        # rewrite the packet's byte arrays for pretty printing:
        e[0] = pcap.base64ify(e[0])
        fid = e[0][0]
        seq = e[0][1]
        inventory.write("%d \n" % seq)
    log.close()
    #inventory.close()

def compareInventory(inventoryint, inventoryext):
    """
    Compares two txt-files who are intended as inventories of pcap files that log the different messages.
    At the moment it only compares the indexes
    TODO: work with hashes of log.
    """
    seq_external = set()
    seq_internal = set()
    with open(inventoryint) as internal:
        for line in internal:
            seq = int(line.rstrip('\n'))
            seq_internal.add(seq)

    with open(inventoryext) as external:
        for line in external:
            seq = int(line.rstrip('\n'))
            seq_external.add(seq)
    print(seq_external)
    print(seq_internal)
    if seq_internal != seq_external:
        seq_diff = seq_external - seq_internal
        print(seq_diff)
        return seq_diff
    else:
        print("both logs are up to date!")
        return set()

def sendInventory(inventory, socket):
    """

    """
    #TODO: This code has not yet been tested
    file = open("logtextfile.txt")
    SendData = file.read(512)
    while SendData:
        socket.send(SendData.encode('utf-8'))
        SendData = file.read(512)

def receivePeerInventory(socket):
    #socket is a BluetoothSocket, not an IP socket!!!
    #peerInventoryByteSize =
    #if peerInventoryByteSize != None:
    """
    Please comment
    """
    #TODO: This code has not yet been tested
    try:
        while 1:
            peerInventory = socket.recv(2048)
            if peerInventory:
                print(peerInventory)
                return(peerInventory)
    except BluetoothError:
        print(f"<Bluetooth error: {BluetoothError}>")
    except Exception as e:
        print("Error: %s" % e)
    return

def createPayload(fname, inventoryint, inventoryext):
    """
    creates payload pcap file with the missing pcap files for the peer.
    """
    #how do we create the payload? As a clear text file just like we assume to store them locally?
    log = importPCAP(fname)
    payload = importPCAP('payload.pcap')
    seq_payload = compareInventory(inventoryint, inventoryext)
    if seq_payload == set():
        return
    log.open('r')
    payload.open('a')
    for w in log:
        e = cbor2.loads(w)
        href = hashlib.sha256(e[0]).digest()
        e[0] = cbor2.loads(e[0])
        # rewrite the packet's byte arrays for pretty printing:
        e[0] = pcap.base64ify(e[0])
        fid = e[0][0]
        seq = e[0][1]
        if seq in seq_payload:
            payload.write(w)
    payload.close()
    log.close()

def handlePayload(fname, payload, inventoryDict):
    """
    takes the Payload of the peer specified for the local log and writes
    """
    log = importPCAP(fname)
    payload = importPCAP(payload)
    log.open('a')
    payload.open('r')
    for w in payload:
        log.write(w)
    createInventory(fname,inventoryDict)

def sendPayload(socket):
    """
    Please comment
    """
    #TODO: Implement and test
    pass

def receivePeerPayload(socket):
    """
    Please comment
    """
    #Current code already deprecated
    #TODO: Implement and test
    try:
        dataReceivedFromPeer = socket.recv(4096) # receive using socket
    except BluetoothError:
        print(f"<Bluetooth error: {BluetoothError}>")
    except Error:
        print(f"Error: {Error}")

    if dataReceivedFromPeer:
        for entry in dataReceivedFromPeer:
            formattedEntry = createEntry(entry)
            processEntry(formattedEntry)
        peerPayload = "???"
        return(True,peerPayload)
    else:
        return(False,"")

def sendOk():
    pass

def terminate():
    pass
