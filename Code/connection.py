# Oliver Weinmeier, Date: 15.4.2020
# 1. This code searches for all discoverable devices closeby and prints them.
# 2.
# Bluetooth Discovery can take quite a long time (up to 15 seconds)
# It is important to check if the nearby devices are actually discoverable
# (they are not by default, only during the pairing process and the like)
from bluetooth import *
import struct
import sys

def chooseSlave(devicesList):
    counter = 1
    nameList = list()
    for addr, name in nearbyDevices:
        print(f"[{counter}] {addr}:{name}")
        nameList.append(name)
        counter += 1
    slaveNum = int(input("Choose the slave by typing their number [x] >>"))
    counter = 1
    slaveAddress = ""
    for addr, name in nearbyDevices:
        if counter == slaveNum:
            slaveAddress = addr
            break
    #print(slaveAddress)
    return(slaveAddress)


port = 1
localBTAddress = read_local_bdaddr()
print(f"Our local Bluetooth address is {localBTAddress}")


if len(sys.argv) < 2:
  print("Usage: {sys.argv[0]} <isMaster> isMaster sets us as the active peer/ master and can be 0 or 1")
else:
  isMaster = int(sys.argv[1])
  print("<You are now {title}>".format(title = "initiating the transfer" if isMaster == 1 else "waiting for an initiation"))


print("<Scanning...Please hold...>")


if isMaster:
    nearbyDevices = discover_devices(lookup_names=True,flush_cache=True)
    print(f"<The scan has discovered {len(nearbyDevices)} (discoverable) devices nearby>")
    for addr, name in nearbyDevices:
        print(f"{addr}:{name}")
    serverAddress = chooseSlave(nearbyDevices)
    serverName = lookup_name(serverAddress)
    socket = BluetoothSocket(RFCOMM)
    #print(f"<Now connecting to {serverName}:{serverAddress}>")
    #socket.connect( (serverAddress,port) )
    #socket.send(...)
    socket.close()
else:
    backlog = 1
    serverSocket = BluetoothSocket(RFCOMM)
    serverSocket.bind( ("", port) )
    serverSocket.listen(backlog)
    clientSocket, clientInfo = serverSocket.accept()
    print(f"Accepted connection from {clientInfo}")
    #data = clientSocket.recv(...)
    #print(f"received: {data}")
    clientSocket.close()
    serverSocket.close()


print("<Program terminated>")
