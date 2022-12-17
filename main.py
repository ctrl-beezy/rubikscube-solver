import numpy as np
import cv2
from kociemba import solve
import serial
import sys
import glob
import time
import random
import RPi.GPIO as GPIO


def scrambleCube():
    random.seed()
    sidesList = ['F', 'B', 'U', 'D', 'L', 'R', 'R2','F2', 'B2', 'U2', 'D2', 'L2', "F'", "B'", "U'", "D'", "L'", "R'"]
    string = ""
    for i in range(random.randrange(5, 20)):
        string.append(random.choice(sidesList))
        string.append(" ")
    return string


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def guessColor( v, r ):
    colorFilter = (
    ( np.array([85.0, 75.0, 60.0]), np.array([150.0, 225.0, 255.0]),'B'),
    ( np.array([0.0, 70.0, 70.0]), np.array([20.0, 255.0, 255.0]),"O" ),
    ( np.array([20.5, 40.0, 35.0]),np.array([45.0, 255.0, 255.0]),  "Y" ),
    ( np.array([45.5, 35.0, 40.0]), np.array([84.0, 255.0, 255.0]),"G" ),
    (np.array([0.0, 0.0, 105.0]), np.array([180.0, 60.0, 255.0]) ,"W" ),
    ( np.array([160.0, 60.0,  80.0]), np.array([180.0, 255.0, 255.0]),"R" )
    )

    for min, max, code in colorFilter:
        if ((min[0] <= v[0] <= max[0]) and (min[1] <= v[1] <= max[1]) and (min[2] <= v[2] <= max[2])):
            if code == 'R':
                #print(r)
                if (r[0] <= 100.0 or (r[0] <= 144.0 and r[1] >= 70.0 and  r[2] >= 70.0) or (r[0] <= 200 and r[1] >= 120.0 and r[2] >= 130.0)):
                    code = 'O'
            return code
    return "X"

def getColors(frame, mat):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #colorSamplesB = []
    code = []
    w = 8
    h = 8

    for lines in mat:
        x1,y1 = lines
        blockHSV = hsv[(y1-h//2):(y1+h//2),(x1-w//2):(x1+w//2)]
        block_h = blockHSV[:,:, 0 ]
        block_s = blockHSV[:,:, 1 ]
        block_v = blockHSV[:,:, 2 ]
        blockRGB = rgb[(y1-h//2):(y1+h//2),(x1-w//2):(x1+w//2)]
        block_r = blockRGB[:,:, 0 ]
        block_g = blockRGB[:,:, 1 ]
        block_b = blockRGB[:,:, 2 ]
        #print(block_h)
        clrh = np.array((np.median(block_h),np.median( block_s ), np.median( block_v ))) 
        clrr = np.array((np.median(block_r),np.median( block_g ), np.median( block_b ))) 
                
        #colorSamplesB.append(clrh)
        code.append(guessColor(clrh,clrr))
        return code



def solveCube(frameFront, frameBack):
    matBack = np.array([[496, 60], #Up
                        [459, 80],
                        [363, 114],
                        [431, 40],
                        [351, 80], #UpCenter
                        [257, 95],
                        [280, 37],
                        [250, 51],
                        [170, 80],
                        [131, 156], #Right
                        [221, 183],
                        [325, 219],
                        [138, 257],
                        [246, 279], #RightCenter
                        [332, 349],
                        [180, 386],
                        [237, 402],
                        [331, 448],
                        [419, 220], #Back
                        [498, 160],
                        [550, 117],
                        [421, 332],
                        [470, 255], #BackCenter
                        [542, 220],
                        [427, 434],
                        [482, 376],
                        [524, 355]])
    matFront = np.array([[376, 58], #Front
                        [450, 107],
                        [505, 128],
                        [382, 173], 
                        [444, 239], #FrontCenter
                        [528, 273], 
                        [398, 308], 
                        [473, 338], 
                        [532, 376], 
                        [119, 131], #Left
                        [186, 106], 
                        [281, 59], 
                        [103, 269], 
                        [207, 229], #LeftCenter
                        [291, 171], 
                        [100, 354], 
                        [193, 334], 
                        [295, 301], 
                        [322, 398], #Down
                        [411, 417], 
                        [480, 425], 
                        [224, 418], 
                        [322, 421], #DownCenter
                        [395, 442],
                        [136, 431], 
                        [225, 444], 
                        [260, 453]])
    codeB = getColors(frameBack, matBack)
    codeF = getColors(frameFront, matFront)
    codeF[26] = 'X'
    for i in range(27):
        img3 = cv2.circle(frameFront,matFront[i],10,(255,0,0),1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        img4 = cv2.putText(img3,codeF[i],matFront[i],font,0.8,(127,127,0),1,cv2.LINE_AA)
        img5 = cv2.circle(frameBack,matBack[i],10,(255,0,0),1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        img6 = cv2.putText(img5,codeB[i],matBack[i],font,0.8,(127,127,0),1,cv2.LINE_AA)
    cv2.imshow('front',img4)
    cv2.imshow('back',img6)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    colorCode = codeB[0:18] + codeF[0:9] + codeF[18:27] + codeF[9:18] + codeB[18:27]
    #len(colorCode)
    #print(colorCode)

    colors = ['W','B','R','O','G','Y']
    for color in colors:
        if colorCode.count(color) == 8:
            colorCode = list(map(lambda x: x.replace('X', color), colorCode))
        #if colorCode.count(color) >= 10:
            #ser.write('F U B D L R'.encode())
    colorDict = {
        colorCode[4] : 'U',
        colorCode[13] : 'R',
        colorCode[22] : 'F',
        colorCode[31] : 'D',
        colorCode[40] : 'L',
        colorCode[49] : 'B'
    }

    cubestring = ""
    colorstring = ""
    colorstring = colorstring.join(colorCode)
    cubestring = cubestring.join(map(colorDict.get,colorCode,colorCode))
    for color in colorDict:
        print(color, '->', colorDict[color], cubestring.count(colorDict[color]))
    print (colorstring, cubestring)
    
    for side in cubestring:
        cnt = cubestring.count(side)
        if cnt != 9:
            break
    solveString = ""
    if cnt == 9:
        solveString = solve(cubestring)
        print(solveString)
        #ser.write(solveString.encode())
    return(solveString)

# Define the function to run when the button is pressed
def button_press(channel):
    # Start a timer
    start_time = time.time()

    # Wait for the button to be released
    while GPIO.input(channel) == GPIO.LOW:
        pass

    # Stop the timer and calculate the duration of the press
    end_time = time.time()
    duration = end_time - start_time

    # Determine if the press was long or short based on the duration
    if duration < 5:
        retB, frameBack = capBack.read()
        retF, frameFront = capFront.read()
        if retB and retF:
            solveString, cubestring = solveCube(frameFront, frameBack)
            ser.write(solveString.encode())
            return
    else:
        ser.write(scrambleCube())
        return

def main():
    global capFront = cv2.VideoCapture(2)
    global capBack = cv2.VideoCapture(0)
    if (not(capFront.isOpened()) or not(capBack.isOpened())):
        raise IOError('Kann Kamera nicht oeffnen')
    capFront.set(cv2.CAP_PROP_BRIGHTNESS,       130.0 )
    capFront.set(cv2.CAP_PROP_CONTRAST,         90.0 )
    capFront.set(cv2.CAP_PROP_SATURATION,       115.0 )
    
    capBack.set(cv2.CAP_PROP_BRIGHTNESS,      130.0 )
    capBack.set(cv2.CAP_PROP_CONTRAST,        90.0 )
    capBack.set(cv2.CAP_PROP_SATURATION,      115.0 )
    for i in range(9):
        ret, frame = capBack.read()
        ret, frame = capFront.read()
    portList = serial_ports()
    if(len(portList) == 0):
        raise IOError('Fehler kann keinen seriellen Port finden')
    global ser = serial.Serial()
    ser.baudrate = 115200
    #print(portList)
    ser.port = portList[0]
    ser.open()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(4, GPIO.FALLING, callback=button_press, bouncetime=200)
    
    while True:
        pass

    ser.close()
    capFront.release()
    capBack.release()


if __name__ == "__main__":
    main()
