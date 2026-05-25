from pymodbus.client import ModbusTcpClient
import logging

client = ModbusTcpClient("labs.ctfzone.com", port=8663)
client.connect()
print(f"Connected: {client.connected}")

# Read Coils (0xxxx) - discrete outputs
print("\n=== Coils (0x) ===")
try:
    rr = client.read_coils(address=0, count=100)
    if hasattr(rr, 'bits'):
        print(f"Coils 0-99: {rr.bits}")
    else:
        print(f"Coils response: {rr}")
except Exception as e:
    print(f"Coils error: {e}")

# Read Discrete Inputs (1xxxx)
print("\n=== Discrete Inputs (1x) ===")
try:
    rr = client.read_discrete_inputs(address=0, count=100)
    if hasattr(rr, 'bits'):
        print(f"Discrete Inputs 0-99: {rr.bits}")
    else:
        print(f"Discrete Inputs response: {rr}")
except Exception as e:
    print(f"Discrete Inputs error: {e}")

# Read Holding Registers (4xxxx) - read/write
print("\n=== Holding Registers (4x) ===")
for addr in range(0, 200, 20):
    try:
        rr = client.read_holding_registers(address=addr, count=20)
        if hasattr(rr, 'registers'):
            print(f"Holding {addr:3d}-{addr+19:3d}: {rr.registers}")
        else:
            print(f"Holding {addr:3d} response: {rr}")
    except Exception as e:
        print(f"Holding {addr:3d} error: {e}")

# Read Input Registers (3xxxx) - read only
print("\n=== Input Registers (3x) ===")
for addr in range(0, 200, 20):
    try:
        rr = client.read_input_registers(address=addr, count=20)
        if hasattr(rr, 'registers'):
            print(f"Input {addr:3d}-{addr+19:3d}: {rr.registers}")
        else:
            print(f"Input {addr:3d} response: {rr}")
    except Exception as e:
        print(f"Input {addr:3d} error: {e}")

client.close()
