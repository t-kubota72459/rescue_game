from smbus import SMBus
import time
import threading

addr = 0x08
i2cbus = SMBus(1)

BACKGROUND = False

def busy():
    time.sleep(0.1)
    return i2cbus.read_byte(addr)

def down():
    i2cbus.write_byte(addr, 0x81)
    time.sleep(0.1)

def up():
    i2cbus.write_byte(addr, 0x82)
    time.sleep(0.1)

def play(num):
    i2cbus.write_byte(addr, 0x40|num)
    time.sleep(0.1)

def prev():
    i2cbus.write_byte(addr, 0x21)
    time.sleep(0.1)

def next():
    i2cbus.write_byte(addr, 0x22)
    time.sleep(0.1)

def stop():
    i2cbus.write_byte(addr, 0x00)
    time.sleep(0.1)

def cleanup():
    print("cleanup()")
    pass

if __name__ == '__main__':
    play(1)
