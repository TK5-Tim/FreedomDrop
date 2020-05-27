dict1 = {"eins" : 1}
dict2 = {"eins" : 1, "zwei" : 2} 
seq_external = set()
seq_internal = set()
seq_external.add(dict1.values())
seq_internal.add(dict2.values())
print(seq_external)
print(seq_internal)