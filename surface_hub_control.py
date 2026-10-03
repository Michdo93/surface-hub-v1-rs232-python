#!/usr/bin/env python3
"""
Surface Hub v1 RS-232 Control Script
Author: Senior Editor & Writing Coach
Description: Establishes a reliable serial connection to a Surface Hub v1,
sends power management commands, and verifies state changes based on documentation.
"""

import serial
import time
import sys
from typing import Optional, Tuple

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------
# Use 'COM3' (or similar) on Windows, or '/dev/ttyUSB0' on Linux/Raspberry Pi
SERIAL_PORT = 'COM3'  
BAUD_RATE = 115200
TIMEOUT_SEC = 1.0

# Protocol commands and expectations
CMD_POWER_OFF = "PowerOff"
CMD_POWER_QUERY = "Power?"
EXPECTED_OFF_RESPONSE = "Power=0"
EXPECTED_READY_RESPONSE = "Power=5"
LINE_ENDING = "\n"

# -----------------------------------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------------------------------

def send_serial_command(ser: serial.Serial, command: str) -> str:
    """
    Sends a command string appended with the correct line ending 
    and reads the immediate response line.
    """
    ser.reset_input_buffer()
    payload = f"{command}{LINE_ENDING}".encode('ascii')
    ser.write(payload)
    
    # Give the hardware a brief moment to process and respond
    time.sleep(0.1)
    
    response_bytes = ser.readline()
    return response_bytes.decode('ascii', errors='ignore').strip()

def check_power_status(ser: serial.Serial) -> Tuple[bool, str]:
    """
    Queries the current power status of the Surface Hub.
    Returns a tuple of (is_reachable, status_response).
    """
    try:
        response = send_serial_command(ser, CMD_POWER_QUERY)
        if not response:
            return False, "TIMEOUT: No data received from device."
        return True, response
    except Exception as e:
        return False, f"ERROR during status check: {e}"

def execute_power_off(ser: serial.Serial) -> None:
    """
    Sends the PowerOff command and validates the transition to state S5 (Off).
    """
    print(f"[*] Sending '{CMD_POWER_OFF}' command to Surface Hub...")
    off_ack = send_serial_command(ser, CMD_POWER_OFF)
    print(f"[*] Device acknowledgment: '{off_ack}' (Note: might be empty or an echo)")

    # Allow transition time
    print("[*] Waiting for state transition...")
    time.sleep(0.5)

    # Verify final state
    success, status = check_power_status(ser)
    if success:
        print(f"[*] Current status query result: {status}")
        if status == EXPECTED_OFF_RESPONSE:
            print("[✅] SUCCESS: Surface Hub has successfully entered Off state (Power=0).")
        else:
            print(f"[!] WARNING: Device responded, but target state not reached. Current: {status}")
    else:
        print(f"[❌] FAILED: {status}")

# -----------------------------------------------------------------------------
# MAIN EXECUTION
# -----------------------------------------------------------------------------
def main():
    print("-------------------------------------------------------------")
    print(" Surface Hub v1 RS-232 Control Utility")
    print(f" Target Port: {SERIAL_PORT} @ {BAUD_RATE} baud")
    print("-------------------------------------------------------------")

    ser: Optional[serial.Serial] = None

    try:
        # Initialize serial connection with robust parameters
        ser = serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUD_RATE,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=TIMEOUT_SEC
        )
        
        if ser.is_open:
            print(f"[+] Successfully opened port {SERIAL_PORT}.")
            
            # 1. Pre-check current status
            reachable, initial_status = check_power_status(ser)
            if not reachable:
                print(f"[❌] Communication check failed: {initial_status}")
                print("[!] Please check your physical DB9-to-RJ11 pin wiring and baud rate settings.")
                sys.exit(1)
                
            print(f"[+] Device online. Initial state: {initial_status}")
            
            # 2. Execute Power-Off sequence
            execute_power_off(ser)

    except serial.SerialException as e:
        print(f"[❌] Serial Port Exception: {e}")
        print("[!] Ensure no other software (like a terminal monitor) is locking the port.")
    except KeyboardInterrupt:
        print("\n[!] Operation aborted by user.")
    finally:
        if ser and ser.is_open:
            ser.close()
            print("[+] Serial port closed safely.")

if __name__ == "__main__":
    main()
```
