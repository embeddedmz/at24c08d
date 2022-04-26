# import the needed packages
import smbus
import datetime
import sys
import os
import time

def printHelp():
    print(sys.argv[0] + " [w startAddr string][r startAddr count]")
    print("w startAddr string - Writes 'string' to the EEPROM memory starting from the address 'startAddr'")
    print("r startAddr count - Reads 'count' bytes from the adress 'startAddr' of the EEPROM memory")

# create a varible to handle the bus
bus = smbus.SMBus(1)

if len(sys.argv) == 4:
    if sys.argv[1] == "w":
        startAddr = int(sys.argv[2])
        if startAddr < 0 or startAddr > 1023:
            print("ERROR - Incorrect byte address ! It should be defined between 0 and 1023")
            sys.exit()
            
        data = sys.argv[3]
        dataLen = len(data)
        if dataLen == 0:
            print("ERROR - String is empty !") # if it's empty we should not have len(sys.argv) == 4 but let's be careful 
            sys.exit()
            
        if startAddr + dataLen > 1024:
            print("ERROR - String cannot be copied entirely from memory address '{}' !".format(startAddr))
            sys.exit()
        #print(data)
        #sys.exit()
        
        for characterIndex in range(0, dataLen):
            charAddr = startAddr + characterIndex
            byte_address_a0_a7 = charAddr & 0xFF
            byte_address_a8_a9 = (charAddr & 0x300) >> 8
            device_address = 0xA0 + (byte_address_a8_a9 << 1) # we assume that A-2 pin (not an address) is always set to GND (0) - please refer to the datasheet
            byte_data = ord(data[characterIndex])
            #print("a0-a7:'{}' - a8-a9:'{}' - device_address:'{}' - byte_data:'{}'".format(byte_address_a0_a7, byte_address_a8_a9, device_address, byte_data))
            bus.write_byte_data(device_address >> 1, byte_address_a0_a7, byte_data) # we shift 1 byte to the right for the API (R/W bit is the LSB and will be managed by the API).
            time.sleep(0.01) # MANDATORY otherwise smbus won't do its job correctly
            #rcvdByte = bus.read_byte_data(device_address >> 1, byte_address_a0_a7)
            #print("rcvdByte: {}".format(rcvdByte))

        
        print("INFO - String written to the EEPROM, please check if all the bytes have been written correctly !")
    
    elif sys.argv[1] == "r":
        startAddr = int(sys.argv[2])
        if startAddr < 0 or startAddr > 1023:
            print("ERROR - Incorrect byte address ! It should be defined between 0 and 1023")
            sys.exit()
            
        count = int(sys.argv[3])
        if count <= 0:
            print("ERROR - read count must be greater than zero !")
            sys.exit()
            
        if startAddr + count > 1024:
            print("ERROR - Requested count '{}' from  memory address '{}' exceeds memory size !".format(count, startAddr))
            sys.exit()
            
        rcvdBytes = []
        for byteIndex in range(0, count):
            charAddr = startAddr + byteIndex
            byte_address_a0_a7 = charAddr & 0xFF
            byte_address_a8_a9 = (charAddr & 0x300) >> 8
            device_address = 0xA0 + (byte_address_a8_a9 << 1) # we assume that A-2 pin (not an address) is always set to GND (0) - please refer to the datasheet
            rcvdByte = bus.read_byte_data(device_address >> 1, byte_address_a0_a7)
            #print("a0-a7:'{}' - a8-a9:'{}' - device_address:'{}' - rcvd_byte:'{}'".format(byte_address_a0_a7, byte_address_a8_a9, device_address, rcvdByte))
            rcvdBytes.append(int(rcvdByte))
            time.sleep(0.01) # MANDATORY otherwise smbus won't do its job correctly
        
        print("Received '{}' bytes".format(len(rcvdBytes)))
        print("Data read in hex format: {}".format(''.join('0x{:02x} - '.format(x) for x in rcvdBytes)))
        print("Data read in string format: {}".format(''.join(chr(x) for x in rcvdBytes)))
    
    else:
        printHelp()
else:
    printHelp()
