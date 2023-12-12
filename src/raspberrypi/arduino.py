from smbus import SMBus
import time
import threading

addr = 0x08
i2cbus = SMBus(1)

def busy():
    c =  i2cbus.read_byte(addr)
    time.sleep(0.01)
    return not c

def down():
    i2cbus.write_byte(addr, 0x81)
    time.sleep(0.01)

def up():
    i2cbus.write_byte(addr, 0x82)
    time.sleep(0.01)

def prev():
    i2cbus.write_byte(addr, 0x83)
    time.sleep(0.01)

def next():
    i2cbus.write_byte(addr, 0x84)
    time.sleep(0.01)

def stop():
    i2cbus.write_byte(addr, 0x01)
    time.sleep(0.01)

def play(num):
    i2cbus.write_byte(addr, 0x40|num)
    time.sleep(0.01)

def cleanup():
    print("cleanup()")
    pass

if __name__ == '__main__':
    play(1)
    time.sleep(3)
    print(busy())
    stop()
    time.sleep(3)
    print(busy())
