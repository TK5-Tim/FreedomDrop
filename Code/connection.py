import bluetooth

nearbyDevices = bluetooth.discover_devices(lookup_names=True)
print(f"The scan has discovered {len(nearbyDevices)} devices")

for addr, name in nearbyDevices:
    print(f"{addr}:{name}")
