import subprocess


def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])

def createEntry(rawEntry):
    #return(entryTuple)
    pass

def processEntry(formattedEntry):
    try:
      if formattedEntry.seq_num == inventory[str(formattedEntry.feed_id)]:
          pass
    except KeyError:
      inventory[str(formattedEntry.feed_id)].append(formattedEntry)

def createInventory(inventoryDict):
    #return inventory
    pass

def sendInventory(inventoryDict):
    pass

def receivePeerInventory():
    pass

def createPayload(fromPeerInventoryDict, inventory):
    #how do we create the payload? As a clear text file just like we assume to store them locally?
    pass

def sendPayload():
    pass

def receivePeerPayload(toPeerPayload):
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
