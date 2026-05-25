from pymodbus.client import ModbusTcpClient
import time

client = ModbusTcpClient("labs.ctfzone.com", port=8663)
client.connect()
print(f"Connected: {client.connected}")

# Read all holding registers 0-1000
print("\n=== Holding Registers (4x) - Extended ===")
for addr in range(0, 1000, 50):
    try:
        rr = client.read_holding_registers(address=addr, count=50)
        if hasattr(rr, 'registers'):
            regs = rr.registers
            non_zero = [(i, v) for i, v in enumerate(regs) if v != 0]
            if non_zero:
                print(f"Holding {addr:3d}-{addr+49:3d}: non-zero at {[(addr+i,v) for i,v in non_zero]}")
        else:
            print(f"Holding {addr:3d} response: {rr}")
    except Exception as e:
        print(f"Holding {addr:3d} error: {e}")

# Read all input registers 0-1000
print("\n=== Input Registers (3x) - Extended ===")
for addr in range(0, 1000, 50):
    try:
        rr = client.read_input_registers(address=addr, count=50)
        if hasattr(rr, 'registers'):
            regs = rr.registers
            non_zero = [(i, v) for i, v in enumerate(regs) if v != 0]
            if non_zero:
                print(f"Input {addr:3d}-{addr+49:3d}: non-zero at {[(addr+i,v) for i,v in non_zero]}")
        else:
            print(f"Input {addr:3d} response: {rr}")
    except Exception as e:
        print(f"Input {addr:3d} error: {e}")

# Read coils extended
print("\n=== Coils (0x) - Extended ===")
try:
    rr = client.read_coils(address=0, count=1000)
    if hasattr(rr, 'bits'):
        coils = rr.bits
        true_indices = [i for i, v in enumerate(coils) if v]
        print(f"True coils: {true_indices}")
except Exception as e:
    print(f"Coils error: {e}")

# Try reading various slave IDs
print("\n=== Different Slave IDs ===")
for slave in range(0, 10):
    try:
        rr = client.read_holding_registers(address=0, count=5, slave=slave)
        if hasattr(rr, 'registers'):
            print(f"Slave {slave}: {rr.registers}")
    except Exception as e:
        print(f"Slave {slave} error: {e}")

client.close()
