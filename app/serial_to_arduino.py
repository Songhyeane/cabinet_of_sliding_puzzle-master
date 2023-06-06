import serial
import time
import numpy as np
import threading
import time


steps = [[1, 1, 3], [2, 4, 2], [3, 5, 3], [4, 2, 0], [5, 4, 1], [6, 5, 2], [7, 3, 1], [8, 1, 0], [9, 5, 3]]



def push_orders(steps):
    exitTread = False

    steps = np.array(steps)
    string_rep = ''.join(''.join(map(str, step)) for step in steps)

    ser = serial.Serial('COM7', 9600)  # Replace 'COMX' with your Arduino's serial port
    time.sleep(1)  # Allow time for the serial connection to establish


    while True:

        # Send string to Arduino
        ser.write(string_rep.encode())
        # Read the string sent back from Arduino
        received_string = ser.readline().decode().strip()

        if received_string :
            #print("Received String:", received_string)
            break


    ser.close()

    return received_string

#push_orders(steps)
