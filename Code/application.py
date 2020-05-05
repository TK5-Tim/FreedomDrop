#!/usr/bin/python 
import cbor2
import hashlib
import impexp 
import lib.pcap as pcap

log = impexp.importPCAP('test.pcap')
impexp.createInventory('test.pcap','logtextfile.txt')
impexp.compareInventory('logtextfile2.txt','logtextfile.txt')
