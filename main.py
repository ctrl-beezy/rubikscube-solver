import numpy as np
import cv2
from kociemba import solve
import serial
import sys
import glob
import time
import random
import RPi.GPIO as GPIO

def blinkLed(pin, numBlinks, cycleTime):
    pauseTime = cycleTime/2
    for i in range(numBlinks):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(pauseTime)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(pauseTime)
    return

def scrambleCube():
    random.seed()
    sidesList = ['F', 'B', 'U', 'D', 'L', 'R', 'R2','F2', 'B2', 'U2', 'D2', 'L2', "F'", "B'", "U'", "D'", "L'", "R'"]
    string = ""
    for i in range(random.randrange(15, 25)):
        string =  string + random.choice(sidesList) + " "
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
    ( np.array([20.5, 40.0, 35.0]),np.array([52.0, 255.0, 255.0]),  "Y" ),
    ( np.array([50.5, 35.0, 40.0]), np.array([84.0, 255.0, 255.0]),"G" ),
    (np.array([0.0, 0.0, 105.0]), np.array([180.0, 65.0, 255.0]) ,"W" ),
    ( np.array([152.0, 60.0,  80.0]), np.array([180.0, 255.0, 255.0]),"R" )
    )

    for min, max, code in colorFilter:
        if ((min[0] <= v[0] <= max[0]) and (min[1] <= v[1] <= max[1]) and (min[2] <= v[2] <= max[2])):
            if code == 'R':
                #print(r)
                if (r[0] <= 100.0 or (r[0] <= 144.0 and r[1] >= 70.0 and  r[2] >= 70.0) or (r[0] <= 180 and r[1] >= 105 and r[2] >= 105)  or (r[0] <= 200 and r[1] >= 120.0 and r[2] >= 130.0 or (r[0] > 150 and r[0] <= 1.8*r[1] and r[0] <= 1.8*(r[2])))):
                    code = 'O'
            if (v[1] < 80 and v[2] > 200):
                    code ='W'
            if code == 'Y':
                if (v[0] >= 48 and v[1] > 100 and v[2] < 185):
                    code = 'G'
            return code
    return "X"

def getColors(frame, mat):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    colorSamples = []
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
                
        colorSamples.append(clrh)
        code.append(guessColor(clrh,clrr))
    return code, colorSamples



def solveCube(frameFront, frameBack):
    matBack = np.array([[496, 60], #Up
                        [459, 80],
                        [363, 114],
                        [431, 40],
                        [348, 77], #UpCenter
                        [257, 95],
                        [281, 31],
                        [250, 51],
                        [165, 80],
                        [131, 156], #Right
                        [221, 183],
                        [325, 219],
                        [138, 257],
                        [246, 279], #RightCenter
                        [332, 349],
                        [178, 394],
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
                        [524, 351]])
    matFront = np.array([[376, 58], #Front
                        [450, 107],
                        [500, 128],
                        [382, 173], 
                        [444, 239], #FrontCenter
                        [523, 273], 
                        [395, 308], 
                        [473, 338], 
                        [532, 376], 
                        [119, 131], #Left
                        [186, 106], 
                        [281, 59], 
                        [103, 269], 
                        [207, 229], #LeftCenter
                        [291, 171], 
                        [97, 354], 
                        [182, 334], 
                        [280, 301], 
                        [322, 398], #Down
                        [420, 415], 
                        [485, 430], 
                        [224, 418], 
                        [322, 421], #DownCenter
                        [393, 438],
                        [136, 431], 
                        [225, 442], 
                        [260, 453]])
    codeB, colorSamplesB = getColors(frameBack, matBack)
    codeF, colorSamplesF = getColors(frameFront, matFront)
    #print(codeF)
    #print(codeB)
    codeF[26] = 'X'
    codeB[6] = 'X'
    #for i in range(27):
        #if codeB[i] == 'W':
        #    print(colorSamplesB[i])
        #img3 = cv2.circle(frameFront,matFront[i],10,(255,0,0),1)
        #font = cv2.FONT_HERSHEY_SIMPLEX
        #img4 = cv2.putText(img3,codeF[i],matFront[i],font,0.8,(127,127,0),1,cv2.LINE_AA)
        #img5 = cv2.circle(frameBack,matBack[i],10,(255,0,0),1)
        #font = cv2.FONT_HERSHEY_SIMPLEX
        #img6 = cv2.putText(img5,codeB[i],matBack[i],font,0.8,(127,127,0),1,cv2.LINE_AA)
    #cv2.imshow('front',img4)
    #cv2.imshow('back',img6)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    colorCode = codeB[0:18] + codeF[0:9] + codeF[18:27] + codeF[9:18] + codeB[18:27]
    #len(colorCode)
    #print(colorCode)
    colorCode1 = colorCode.copy()
    colorCode2 = colorCode.copy()
    colors = ['W','B','R','O','G','Y']
    colorsReverse = list(reversed(colors))
    #print(colors)
    #print(colorsReverse)
    for i in range(54):
        if colorCode1[i] == 'X':
            for color1 in colors:
                if colorCode1.count(color1) <= 8:
                    colorCode1[i] = color1
                    print(i, color1)
                    break
        if colorCode2[i] == 'X':
            for color2 in colorsReverse:
                if colorCode2.count(color2) <= 8:
                    print(color2, i)
                    colorCode2[i] = color2
                    break

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

    cubestring1 = ""
    cubestring2 = ""
    colorstring1 = ""
    colorstring2 = ""
    colorstring1 = colorstring1.join(colorCode1)
    colorstring2 = colorstring2.join(colorCode2)
    cubestring1 = cubestring1.join(map(colorDict.get,colorCode1,colorCode1))
    cubestring2 = cubestring2.join(map(colorDict.get,colorCode2,colorCode2))
    for color in colorDict:
        print(color, '->', colorDict[color], cubestring1.count(colorDict[color]))
    print ('ColorString:',colorstring1)
    print('SidesString1:', cubestring1)
    print ('SidesString2:',cubestring2)
    
    cnt = 0
    for side in cubestring1:
        cnt = cubestring1.count(side)
        if cnt != 9:
            break
    solveString = ""
    if cnt == 9:
        try:
            solveString = solve(cubestring1)
            print('Moves to Solve:',solveString)
            #ser.write(solveString.encode())
        except:
            solveString = solve(cubestring2)
            print('Moves to Solve:', solveString)

    return(solveString)

# Define the function to run when the button is pressed
def button_press(channel):
    # wait because library debounce does not work
    time.sleep(.01)
    # if press was rising edge return
    if (GPIO.input(channel) == GPIO.HIGH):
            return
    # Start a timer
    start_time = time.time()

        # Wait for the button to be released
    while GPIO.input(channel) == GPIO.LOW:
        pass

        # Stop the timer and calculate the duration of the press
    end_time = time.time()
    duration = end_time - start_time

        # Determine if the press was long or short based on the duration
    if duration < 2:
        print('solving cube')
        blinkLed(17,3,0.25)
        #print(capFront.read())
        retB, frameBack = capBack.read()
        retF, frameFront = capFront.read()
        #print(retB, retF)
        if retB and retF:
            solveString = solveCube(frameFront, frameBack)
            if solveString :
                blinkLed(17,6,0.25)
                ser.write(solveString.encode())
                time.sleep(7)
            else:
                print("Fehler Scan nicht korrekt. Versuche es erneut")
                blinkLed(17,12,0.125)
    else:
        print('scrambling cube')
        blinkLed(17,3,1)
        scrambleString = scrambleCube()
        print('Scramble Moves:',scrambleString)
        ser.write(scrambleString.encode())
        time.sleep(6)

def main():
    #global variable declarations
    global capFront 
    global capBack
    global ser
    
    #logfile = open("logfile.txt","w")
    #sys.stdout = logfile
    
    capFront = cv2.VideoCapture(2)
    capBack = cv2.VideoCapture(0)
    if (not(capFront.isOpened()) or not(capBack.isOpened())):
        raise IOError('Kann Kamera nicht oeffnen')
    capFront.set(cv2.CAP_PROP_BRIGHTNESS,       140.0 )
    capFront.set(cv2.CAP_PROP_CONTRAST,         90.0 )
    capFront.set(cv2.CAP_PROP_SATURATION,       120.0 )
    #capFront.set(cv2.CAP_PROP_HUE, 1.0)
    #capFront.set(cv2.CAP_PROP_FOCUS, 2.5) 
    #print(capFront.get(cv2.CAP_PROP_GAMMA))

    capBack.set(cv2.CAP_PROP_BRIGHTNESS,      140.0 )
    capBack.set(cv2.CAP_PROP_CONTRAST,        90.0 )
    capBack.set(cv2.CAP_PROP_SATURATION,      120.0 )
    #capBack.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    for i in range(9):
        ret, frame = capBack.read()
        ret, frame = capFront.read()
    portList = serial_ports()
    if(len(portList) == 0):
        raise IOError('Fehler kann keinen seriellen Port finden')
    ser = serial.Serial()
    ser.baudrate = 115200
    print(portList)
    ser.port = portList[0]
    ser.open()
   
    #setup GPIO PINS
    # Pin 4 is Push Button, Pin 17 i status Led
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, GPIO.LOW)
    GPIO.add_event_detect(4, GPIO.BOTH, callback=button_press, bouncetime=300)
    while True:
        ret, Frame = capFront.read()
        ret, Frame = capBack.read()
        pass

    ser.close()
    capFront.release()
    capBack.release()
    GPIO.cleanup()


if __name__ == "__main__":
    main()
