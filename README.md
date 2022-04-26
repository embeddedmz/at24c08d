# AT24C08D - I²C-Compatible (2-Wire) Serial EEPROM 8-Kbit (1,024 x 8 bits)

Short python code to read and write to the EEPROM (1024 Kbytes) from a GNU/Linux system.

<h2>Description</h2>
This code is a simple easy way to read and write bytes from/to the EEPROM AT24C08D. I have written it as a prototype before writing a C# Core code that makes use of C functions (open, close, ioctl etc...) to interact with the I2C bus (e.g. [DllImport("libc.so.6", EntryPoint = "open")]...).

<h2>How to use ?</h2>
To use this program you have to be running Python. It only accepts 2 arguments in the command line.
<br>
<b>w startingAdress "string to be written"</b>  : This is for writing a string of characters to the EEPROM memory starting from the address 'startingAdress'. If you need to store a file into a shell variable you can use this trick : https://stackoverflow.com/questions/4749905/how-can-i-read-a-file-and-redirect-it-to-a-variable and then use the prefix '$' to pass the variable to the script.
<br>
<br>
<b>r startingAdress count</b>  : This is for reading 'count' characters from the adress 'startingAdress' of the EEPROM memory.
<br>
A proper writing of a string starting at address 0 of the EEPROM memory will be:
<br>
<b>python3 at24c08d.py w 0 "Hello world"</b>
<br>
A proper reading of characters from the adress 0 of the EEPROM memory of 11 characters will be:
<br>
<b>python3 at24c08d.py r 0 11</b>

You can also manage the EEPROM using the kernel and access it using the file system (sysfs). Here are some resources :

- https://stackoverflow.com/questions/52499762/linux-instantiate-from-user-space-eeprom-new-device
- https://erlerobotics.gitbooks.io/erle-robotics-erle-brain-a-linux-brain-for-drones/content/en/tutorials/i2c.html
- https://community.nxp.com/t5/i-MX-Processors/I2C1-interface-for-EEPROM-RTC/m-p/246128 (mtd-utils package)
- https://connect.ed-diamond.com/GNU-Linux-Magazine/GLMF-208/Mise-en-aeuvre-du-protocole-Modbus-RTU-sur-WaRP7-via-Qt5 (in french but look at the source code/commands related to the EEPROM)
