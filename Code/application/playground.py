"""
from logMerge.PCAP import PCAP
import os

for file in os.listdir("payload"):
    print(file[:-5])

"""
"""
try:
    print("eigene DB")
    packets_list = PCAP.read_pcap("payload/6b1349f67abde08e88bb9051d23561c806f0b581aed923fab97268e6db94e6a7_v.pcap")
    PCAP.write_pcap("tester", packets_list)
except Exception as e: 
    print(e)
"""

"""
inventoryext = {"eins" : 1}
inventoryint = {"eins" : 3, "zwei" : 2} 
seq_external = set()
seq_internal = set()

diff = {k: -1 for k in inventoryint if k not in inventoryext}
print(diff)

diff1 = {k: inventoryext[k] for k in inventoryint if k in inventoryext and inventoryext[k] < inventoryint[k]}
print(diff1)

diff.update(diff1)
print(diff)
"""

test = bytearray(b'k\x13I\xf6z\xbd\xe0\x8e\x88\xbb\x90Q\xd25a\xc8\x06\xf0\xb5\x81\xae\xd9#\xfa\xb9rh\xe6\xdb\x94\xe6\xa7')
print(test)
test2 = bytes(test)
print(test2)