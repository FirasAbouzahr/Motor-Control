import tkinter as tk
import platform
from tkinter.messagebox import askyesno
import time
import serial

'''
   
This code is used to operate a step motor which moves a Germanium-68 line source across the length of a PET scanner for calibration.
The code allows us to control the speed, distance, and # of cycles for the movement of our line source across the detector face.
A simple GUI is coded below to allow for simpler functionality.
    
'''


# logistical code for connecting to the driver
platform.system() == 'Darwin'
ser = serial.Serial()
ser.port = "/dev/cu.usbserial-AB0MICGP"
ser.baudrate = 9600 # speed of communication between computer and port
ser.bytesize = serial.EIGHTBITS # number of bits per bytes
ser.parity = serial.PARITY_NONE # parity checks wheter or not data is lost or overwritten... we dont need
ser.stopbits = serial.STOPBITS_ONE #number of stop bits
ser.timeout = 1            # time til time out

ser.xonxoff = False     #disable software flow control
ser.rtscts = False     #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2     #timeout for write

# motor commands code
def custom(speed,distance,loops, pause = 30):
    speed = speed * 200
    distance = distance * 200
    loops = loops * 2
    
    speed = "S1M" + str(speed) # set speed
    distance = "I1M" + str(-distance) # set distance per half cycle (one way)
    loop = 'L-' + str(loops) # set number of cycles
    pause = 'P' + str(pause) # pause between half cycles
    
    # writting Velmex commands in terms of our function parameters
    if loops <= 0:
        string = "F,C," + speed + "," + distance + ',R'
    
    else:
        string = "F,C," + speed + "," + distance + "," + pause +  "," + loop + ',R,'
    
    # read out information to the velmex controller
    ser.open()
    ser.write(str.encode(string))
    time.sleep(0.5)
    ser.close()

def killProgram():
    ser.open()
    ser.write(str.encode("K,C"))
    time.sleep(0.5)
    ser.close()

# code for the GUI interface itself
window = tk.Tk()
window.geometry("400x400")
window.minsize(300,300)
window.maxsize(300,300)
title = tk.Label(text = 'Welcome to the TPPT motor GUI', master = window,font='Helvetica 18 bold')
title.pack()
frame1 = tk.Frame(master = window, width = 300, height = 300,highlightbackground = 'black', highlightthickness = 1)
frame1.pack()
speedLabel = tk.Label(text = 'Enter speed in cm/s', master = frame1 )
speedEntry = tk.Entry(master = frame1)
distanceLabel = tk.Label(text = 'Enter distance in cm',master = frame1)
distanceEntry = tk.Entry(master = frame1)
loopLabel = tk.Label(text = 'Enter number of Cycles', master = frame1)
loopEntry = tk.Entry(master = frame1)

def clearD():
    speedEntry.delete(0, tk.END)
    distanceEntry.delete(0, tk.END)
    loopEntry.delete(0,tk.END)

def killConfirmed():
    answer = askyesno(title='Confirmation', message = 'Are you sure you want to stop the current run?')
    if answer == True:
        killProgram()
    else:
        pass

resetD = tk.Button(text = 'Clear', master = frame1, command = clearD)

speedLabel.pack()
speedEntry.pack()
distanceLabel.pack()
distanceEntry.pack()
loopLabel.pack()
loopEntry.pack()
resetD.pack()

rot = tk.Button(text = 'Run', command = lambda: custom(float(speedEntry.get()),float(distanceEntry.get()), int(loopEntry.get())), master = frame1)
rot.pack(side = tk.LEFT)

kill = tk.Button(text = 'Kill', command = killConfirmed, master = frame1)
kill.pack(side = tk.RIGHT)
window.mainloop()
