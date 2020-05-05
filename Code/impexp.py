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
    - receivePeerPayload()
    - sendOk()                  TODO
    - terminate()               TODO
### NOTICE: Everything is still a work-in-progress functions in this module might later be
moved to a more appropriate module
### TODO: It would probably be good to create a Python method which turns .pcap files
into Python objects which can then be parsed and handled easier (i.e. JSON objects)
"""

import lib.pcap as pcap
import cbor2
import hashlib
import subprocess
import difflib


def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])

def importPCAP(fname): 
    log = pcap.PCAP(fname)
    return log

def importInventory(fname):
    inventory = open(fname)
    return inventory

def createEntry(rawEntry):
    #return(entryTuple)
    pass

def processEntry(formattedEntry):
    try:
      if formattedEntry.seq_num == inventory[str(formattedEntry.feed_id)]:
          pass
    except KeyError:
      inventory[str(formattedEntry.feed_id)].append(formattedEntry)

def createInventory(fname, inventoryDict):
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
    with open(inventoryint) as internal:
        seq_internal = [line.rstrip('\n') for line in internal]
    with open(inventoryext) as external:
        seq_external = [line.rstrip('\n') for line in external]
    if seq_internal != seq_external: 
        seq_diff = set(seq_external) - set(seq_internal)
        print(seq_diff)
    else:
        print("both logs are up to date!")

def sendInventory(inventoryDict):
    pass

def receivePeerInventory():
    pass

def createPayload(fromPeerInventoryDict, inventory):
    #how do we create the payload? As a clear text file just like we assume to store them locally?
    pass

def sendPayload():
    pass

def receivePeerPayload():
  dataReceivedFromPeer = "" # receive
  if dataReceivedFromPeer:
    for entry in dataReceivedFromPeer:
      formattedEntry = createEntry(entry)
      processEntry(formattedEntry)
      return True
  else:
    return False

def sendOk():
    pass

def terminate():
    pass
