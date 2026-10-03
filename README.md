# Surface Hub v1 RS-232 Control Utility

A robust, production-ready Python utility to control and monitor a Microsoft Surface Hub v1 via its serial management port (RS-232 / RJ11).

---

## ⚠️ Important Technical Prerequisites (The Hardware Catch)

Before attempting any software communication, you must ensure your physical hardware chain handles the **correct electrical voltage levels**. 

* **The Problem:** Many cheap cables (like standard USB-to-RJ11/RJ12 cables built for battery management systems or microcontrollers) operate on **TTL levels ($3.3\text{V}$ or $5\text{V}$)**. The Surface Hub v1 requires true **RS-232 bipolar voltage levels ($\pm 12\text{V}$)**. Using a TTL-only cable will result in silent communication failures.
* **The Solution:** You must use a true **USB-to-RS-232 hardware converter** combined with a serial breakout/RJ11 adapter.

### Correct Cabling Chain
$$\text{Host PC (USB)} \xrightarrow{\text{USB}} \underbrace{\text{USB-to-RS-232 Adapter (e.g., FTDI/PL2303)}}{\text{Generates $\pm 12\text{V}$ levels}} \xrightarrow{\text{DB9}} \underbrace{\text{DB9-to-RJ11 Adapter}}{\text{Pins transmission}} \xrightarrow{\text{RJ11}} \text{Surface Hub Management Port}$$

---

## Hardware Requirements

1. **Host Computer:** Windows, Linux (Ubuntu), or Raspberry Pi (Raspberry Pi OS).
2. **USB-to-RS-232 Serial Converter:** 
   * *Recommended:* DSD TECH or StarTech adapter featuring an **FTDI chipset** (e.g., FT232RL) for superior driver stability.
3. **DB9 to RJ11/RJ12 Adapter Cable:** 
   * A 6P6C (RJ12) or 6P4C (RJ11) serial control cable to bridge the DB9 connector to the Surface Hub's management port.

---

## Installation & Setup

### 1. Python Dependencies
Ensure you have Python 3.8+ installed. Install the official `pyserial` library:

```bash
pip install pyserial
```

### 2. Operating System Configuration (Linux / Raspberry Pi)
If you are running the script on a Linux host (like a Raspberry Pi or Ubuntu PC), ensure your user account has permissions to access the serial port (typically `/dev/ttyUSB0`):

```bash
sudo usermod -a -G dialout $USER
```
*(Log out and back in for changes to take effect).*

---

## Surface Hub v1 Power States Reference

According to the official Microsoft Surface Hub v1 documentation, the power management states are defined as follows:

| State Code | Energy Star | Description | Meaning |
| :--- | :--- | :--- | :--- |
| **0** | S5 | Off | The device/display is completely shut down. |
| **1** | - | Power up (indeterminate) | Boot sequence or transitional state. |
| **2** | S3 | Sleep | Standby energy-saving mode. |
| **5** | S0 | Ready | The device is fully active and powered on. |

> **Note for Replacement PC Mode:** In Replacement PC mode, the power states toggle strictly between **0 (Off)** and **5 (Ready)**, affecting the display and management layer only. The management port cannot be used to remotely power *on* an external replacement PC.

---
