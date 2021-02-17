import serial
from serial.tools import list_ports
import time
# import module sys to get the type of exception
import sys

# FINDING THE ARDUINO COM PORT AUTOMATICALLY
# import win32com.client
available_ports = list_ports.comports()
arduinoCOMport = ""
for com in available_ports:
    if "Arduino" in str(com.manufacturer):
        print(com.device)
        arduinoCOMport = com.device

if arduinoCOMport == "":
    print("NO ARDUINO FOUND")
    arduinoCOMport = input("Please enter Arduino COM port (COMx)")
try:
    ser = serial.Serial(
        port=arduinoCOMport,
        baudrate=9600,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS
    )

    ser.flush()
    ser.flushInput()
    ser.flushOutput()
    time.sleep(1)

    userinput = input("enter number of steps to move (no value = 5 steps): ")
    print("Please wait...")

    if userinput != "":
        steps = userinput

    else:
        steps = 5

    ser.write((str(steps) + "\x04").encode("utf-8"))

    while True:

        inputfromarduino = ser.readline()
        if inputfromarduino:
            inputfromarduino = inputfromarduino.decode("utf-8")
            inputfromarduino = inputfromarduino.strip()

        if "potentio" in inputfromarduino:  # to print potentiometer value
            print(inputfromarduino)

        if (inputfromarduino == 'DONE'):
            print("Completed " + str(steps) + " steps")
            userinput = input("enter number of steps to move (no value = 5 steps): ")
            print("Please wait...")

            if userinput != "":
                steps = userinput

            else:
                steps = 5

            ser.write((str(steps) + "\x04").encode("utf-8"))


except Exception as e:

    print(sys.exc_info()[1])

input()
