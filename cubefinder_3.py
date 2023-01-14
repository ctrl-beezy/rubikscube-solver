import cv2
from math import sin,cos,pi,atan2,sqrt
import numpy as np
from time import sleep, time

capture = cv2.VideoCapture(0)
#capture.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
#capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)
cv2.namedWindow("Fig")
ret, frame = capture.read()
S2, S1 = frame.shape[:2]
den = 2
sg = np.zeros((S1//den, S2//den, 3), dtype=np.uint8)
sgc = np.zeros((S1//den, S2//den, 3), dtype=np.uint8)
hsv = np.zeros((S1//den, S2//den, 3), dtype=np.uint8)
dst = np.zeros((S1//den, S2//den, 1), dtype=np.uint8)
dst2 = np.zeros((S1//den, S2//den, 1), dtype=np.uint8)
d = np.zeros((S1//den, S2//den, 1), dtype=np.int16)
d2 = np.zeros((S1//den, S2//den, 1), dtype=np.uint8)
d3 = np.zeros((S1//den, S2//den, 1), dtype=np.uint8)
b = np.zeros((S1//den, S2//den, 1), dtype=np.uint8)
b4 = np.zeros((S1//den, S2//den, 1), dtype=np.uint8)
both = np.zeros((S1//den, S2//den, 1), dtype=np.uint8)
harr = np.zeros((S1//den, S2//den, 1), dtype=np.float32)
W, H = S1//den, S2//den
lastdetected = 0
THR = 100
dects = 50 # ideal number of number of lines detections

hue = np.zeros((S1//den, S2//den, 1), dtype=np.uint8)
sat = np.zeros((S1//den, S2//den, 1), dtype=np.uint8)
val = np.zeros((S1//den, S2//den, 1), dtype=np.uint8)

# stores the coordinates that make up the face. in order: p,p1,p3,p2 (i.e.) counterclockwise winding
prevface = [(0,0),(5,0),(0,5)]
dodetection=True

onlyBlackCubes=False

def intersect_seg(x1,x2,x3,x4,y1,y2,y3,y4):
    den= (y4-y3)*(x2-x1)-(x4-x3)*(y2-y1)
    if abs(den)<0.1: return (False, (0,0),(0,0))
    ua=(x4-x3)*(y1-y3)-(y4-y3)*(x1-x3)
    ub=(x2-x1)*(y1-y3)-(y2-y1)*(x1-x3)    
    ua=ua/den
    ub=ub/den
    x=x1+ua*(x2-x1)
    y=y1+ua*(y2-y1)
    return (True,(ua,ub),(x,y))

def ptdst(p1,p2):
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))
    
def ptdstw(p1,p2):
    #return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

    #test if hue is reliable measurement
    if p1[1]<100 or p2[1]<100:
        #hue measurement will be unreliable. Probably white stickers are present
        #leave this until end
        return 300.0+abs(p1[0]-p2[0])
    else:
        return abs(p1[0]-p2[0])
        
    
def ptdst3(p1,p2):
    dist=sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1])+(p1[2]-p2[2])*(p1[2]-p2[2]))
    if (p1[0]>245 and p1[1]>245 and p1[2]>245):
        #the sticker could potentially be washed out. Lets leave it to the end
        dist=dist+300.0
    return dist
    
def compfaces(f1,f2):
    totd=0
    for p1 in f1:
        mind=10000
        for p2 in f2:
            d=ptdst(p1,p2)
            if d<mind:
                mind=d
        totd += mind
    return totd/4

def avg(p1,p2):
    return (0.5*p1[0]+0.5*p2[0], 0.5*p2[1]+0.5*p2[1])

def areclose(t1,t2,t):
    #is t1 close to t2 within t?
    return abs(t1[0]-t2[0])<t and abs(t1[1]-t2[1])<t

def winded(p1,p2,p3,p4):
    #return the pts in correct order based on quadrants
    avg=(0.25*(p1[0]+p2[0]+p3[0]+p4[0]),0.25*(p1[1]+p2[1]+p3[1]+p4[1]))
    ps=[(atan2(p[1]-avg[1], p[0]-avg[0]), p) for p in [p1,p2,p3,p4]]
    ps.sort(reverse=True)
    return [p[1] for p in ps]
 
#return tuple of neighbors given face and sticker indeces
def neighbors(f,s):
    if f==0 and s==0: return ((1,2),(4,0))
    if f==0 and s==1: return ((4,3),)
    if f==0 and s==2: return ((4,6),(3,0))
    if f==0 and s==3: return ((1,5),)
    if f==0 and s==5: return ((3,3),)
    if f==0 and s==6: return ((1,8),(5,2))
    if f==0 and s==7: return ((5,5),)
    if f==0 and s==8: return ((3,6),(5,8))
    
    if f==1 and s==0: return ((2,2),(4,2))
    if f==1 and s==1: return ((4,1),)
    if f==1 and s==2: return ((4,0),(0,0))
    if f==1 and s==3: return ((2,5),)
    if f==1 and s==5: return ((0,3),)
    if f==1 and s==6: return ((2,8),(5,0))
    if f==1 and s==7: return ((5,1),)
    if f==1 and s==8: return ((0,6),(5,2))
    
    if f==2 and s==0: return ((4,8),(3,2))
    if f==2 and s==1: return ((4,5),)
    if f==2 and s==2: return ((4,2),(1,0))
    if f==2 and s==3: return ((3,5),)
    if f==2 and s==5: return ((1,3),)
    if f==2 and s==6: return ((3,8),(5,6))
    if f==2 and s==7: return ((5,3),)
    if f==2 and s==8: return ((1,6),(5,0))
    
    if f==3 and s==0: return ((4,6),(0,2))
    if f==3 and s==1: return ((4,7),)
    if f==3 and s==2: return ((4,8),(2,0))
    if f==3 and s==3: return ((0,5),)
    if f==3 and s==5: return ((2,3),)
    if f==3 and s==6: return ((0,8),(5,8))
    if f==3 and s==7: return ((5,7),)
    if f==3 and s==8: return ((2,6),(5,6))
    
    if f==4 and s==0: return ((1,2),(0,0))
    if f==4 and s==1: return ((1,1),)
    if f==4 and s==2: return ((1,0),(2,2))
    if f==4 and s==3: return ((0,1),)
    if f==4 and s==5: return ((2,1),)
    if f==4 and s==6: return ((0,2),(3,0))
    if f==4 and s==7: return ((3,1),)
    if f==4 and s==8: return ((3,2),(2,0))
    
    if f==5 and s==0: return ((1,6),(2,8))
    if f==5 and s==1: return ((1,7),)
    if f==5 and s==2: return ((1,8),(0,6))
    if f==5 and s==3: return ((2,7),)
    if f==5 and s==5: return ((0,7),)
    if f==5 and s==6: return ((2,6),(3,8))
    if f==5 and s==7: return ((3,7),)
    if f==5 and s==8: return ((3,6),(0,8))

def processColors(useRGB=False):
    global assigned, didassignments, cubeString

    bestj = 0
    besti = 0
    bestcon = 0
    matchesto = 0
    bestd = 10001
    taken = [0 for i in range(6)]
    done = 0
    sideDict = {
            0 : 'F',
            1 : 'R',
            2 : 'B',
            3 : 'L',
            4 : 'U',
            5 : 'D'
    }
    opposite = {0: 2, 1: 3, 2: 0, 3: 1, 4: 5, 5: 4} # dict of opposite faces
    # possibilities for each face
    poss = {}
    for j, f in enumerate(hsvs):
        for i, s in enumerate(f):
            poss[j, i] = range(6)

    # we are looping different arrays based on the useRGB flag
    toloop = hsvs
    if useRGB: 
        toloop = colors

    while done < 8*6:
        bestd = 10000
        forced = False
        for j, f in enumerate(toloop):
            for i, s in enumerate(f):
                if i != 4 and assigned[j][i] == -1 and (not forced):
                    # this is a non-center sticker.
                    # find the closest center
                    considered = 0
                    for k in poss[j, i]:
                        # all colors for this center were already assigned
                        if taken[k] < 8:
                            # use Euclidean in RGB space or more elaborate
                            # distance metric for Hue Saturation
                            if useRGB:
                                dist = ptdst3(s, toloop[k][4])
                            else:
                                dist = ptdstw(s, toloop[k][4])

                            considered += 1
                            if dist < bestd:
                                bestd = dist
                                bestj = j
                                besti = i
                                matchesto = k
                    # IDEA: ADD PENALTY IF 2ND CLOSEST MATCH IS CLOSE TO FIRST
                    # i.e. we are uncertain about it

                    if besti == i and bestj == j: 
                        bestcon = considered
                    if considered == 1:
                        # this sticker is forced! Terminate search 
                        # for better matches
                        forced = True
                        print(f'sticker {(i, j)} had color forced!')

        # assign it
        done += 1
        assigned[bestj][besti] = matchesto
        #print(bestcon)

        op = opposite[matchesto] # get the opposite side
        # remove this possibility from neighboring stickers
        # since we cant have red-red edges for example
        # also corners have 2 neighbors. Also remove possibilities
        # of edge/corners made up of opposite sides
        ns = neighbors(bestj, besti)
        for neighbor in ns:
            p = list(poss[neighbor])
            if matchesto in p:
                p.remove(matchesto)
            if op in p:
                p.remove(op)
        taken[matchesto] += 1
    cubeString = cubeString.join(map(sideDict.get,assigned,assigned))
    print(cubeString)
    didassignments = True

succ=0 #number of frames in a row that we were successful in finding the outline
tracking=0
win_size=5
flags=0
detected=0

grey = np.zeros((W,H), dtype=np.uint8)
prev_grey = np.zeros((W,H), dtype=np.uint8)
pyramid = np.zeros((W,H), dtype=np.uint8)
prev_pyramid = np.zeros((W,H), dtype=np.uint8)


counter=0 #global iteration counter
undetectednum=100

#1: learning colors
extract=False
selected=0
colors=[[] for i in range(6)]
hsvs=[[] for i in range(6)]
assigned=[[-1 for i in range(9)] for j in range(6)]
for i in range(6):
    assigned[i][4]=i
    
didassignments=False
#orange green red blue yellow white. Used only for visualization purposes
mycols=[(0,127,255), (20,240,20), (0,0,255), (200,0,0), (0,255,255), (255,255,255)]


while True:
    ret, frame = capture.read()
    if not ret:
        cv2.WaitKey(0)
        break

    # Resize the frame
    sg = cv2.resize(frame, (W, H))

    # Copy sg to sgc
    sgc = sg.copy()

    # Convert to grayscale
    grey = cv2.cvtColor(sg, cv2.COLOR_BGR2GRAY)

    # Tracking mode
    if tracking > 0:
        detected = 2
        # Compute optical flow
        features, status, track_error = cv2.calcOpticalFlowPyrLK(
            prev_grey, grey, np.array(prev_feat),np.array(features))
        # Set back the points we keep
        prev_feat = features
        features = np.array([p for (st, p) in zip(status, features) if st],dtype="float32")
        if len(features) < 4:
            tracking = 0  # we lost it, restart search
        else:
            # make sure that in addition the distances are consistent
            ds1 = ptdst(features[0], features[1])
            ds2 = ptdst(features[2], features[3])
            if max(ds1, ds2) / min(ds1, ds2) > 1.4:
                tracking = 0

            ds3 = ptdst(features[0], features[2])
            ds4 = ptdst(features[1], features[3])
            if max(ds3, ds4) / min(ds3, ds4) > 1.4:
                tracking = 0

            if ds1 < 10 or ds2 < 10 or ds3 < 10 or ds4 < 10:
                tracking = 0
            if tracking == 0:
                detected = 0

    #detection mode
    if tracking == 0:
        detected = 0
        grey = cv2.GaussianBlur(grey, (3, 3), 0)
        dst2 = cv2.Laplacian(grey, cv2.CV_8U)
        d = np.where(dst2 > 8, 255, 0)
        d = d.astype('uint8')
        if onlyBlackCubes:
            b = np.where(grey < 100, 255, 0)
            b = b.astype('uint8')
            d = cv2.bitwise_and(d, b)
        if lastdetected > dects:
            THR += 1
        if lastdetected < dects:
            THR = max(2, THR-1)
        lines = cv2.HoughLinesP(d, 1, np.pi/180, THR, minLineLength=10, maxLineGap=5)
        angs = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            a = atan2(y2-y1, x2-x1)
            if a < 0:
                a += pi
            angs.append(a)
        #lets look for lines that share a common end point
        t = 10
        totry = []
        for i in range(len(lines)):
            p1, p2 = lines[i][0][:2], lines[i][0][2:]
            for j in range(i+1, len(lines)):
                q1, q2 = lines[j][0][:2], lines[j][0][2:]
                
                dd1 = sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)
                dd2 = sqrt((q2[0]-q1[0])**2+(q2[1]-q1[1])**2)
                if max(dd1, dd2)/min(dd1, dd2) > 1.3:
                    continue
                
                matched = 0
                if areclose(p1, q2, t):
                    IT = (avg(p1, q2), tuple(p2), tuple(q1), dd1)
                    matched += 1
                if areclose(p2, q2, t):
                    IT = (avg(p2, q2), tuple(p1), tuple(q1), dd1)
                    matched += 1
                if areclose(p1, q1, t):
                    IT = (avg(p1, q1), tuple(p2), tuple(q2), dd1)
                    matched += 1
                if areclose(p2, q1, t):
                    IT = (avg(p2, q1), q2, p1, dd1)
                    matched += 1
                if matched == 0:
                    #not touching at corner... try also inner grid segments hypothesis?
                    p1 = (float(p1[0]), float(p1[1]))
                    p2 = (float(p2[0]), float(p2[1]))
                    q1 = (float(q1[0]), float(q1[1]))
                    q2 = (float(q2[0]), float(q2[1]))
                    success, (ua, ub), (x, y) = intersect_seg(p1[0], p2[0], q1[0], q2[0], p1[1], p2[1], q1[1], q2[1])
                    if success and 0 < ua < 1 and 0 < ub < 1:
                        #if they intersect
                        #cv.Line(sg, p1, p2, (255,255,255))
                        ok1 = 0
                        ok2 = 0
                        if abs(ua-1/3) < 0.05:
                            ok1 = 1
                        if abs(ua-2/3) < 0.05:
                            ok1 = 2
                        if abs(ub-1/3) < 0.05:
                            ok2 = 1
                        if abs(ub-2/3) < 0.05:
                            ok2 = 2
                        if ok1 > 0 and ok2 > 0:
                            #ok these are inner lines of grid
                            #flip if necessary
                            if ok1==2: p1,p2=p2,p1
                            if ok2==2: q1,q2=q2,q1
                            
                            #both lines now go from p1->p2, q1->q2 and 
                            #intersect at 1/3
                            #calculate IT
                            z1=(q1[0]+2.0/3*(p2[0]-p1[0]),q1[1]+2.0/3*(p2[1]-p1[1]))
                            z2=(p1[0]+2.0/3*(q2[0]-q1[0]),p1[1]+2.0/3*(q2[1]-q1[1]))
                            z=(p1[0]-1.0/3*(q2[0]-q1[0]),p1[1]-1.0/3*(q2[1]-q1[1]))
                            IT=(z,z1,z2,dd1)
                            matched=1
                #only single one matched!! Could be corner
                if matched==1:
                    
                    #also test angle
                    a1 = atan2(p2[1]-p1[1],p2[0]-p1[0])
                    a2 = atan2(q2[1]-q1[1],q2[0]-q1[0])
                    if a1<0:a1+=pi
                    if a2<0:a2+=pi
                    ang=abs(abs(a2-a1)-pi/2)
                    if ang < 0.5:
                        totry.append(IT)
                        #cv.Circle(sg, IT[0], 5, (255,255,255))
        
        
        #now check if any points in totry are consistent!
        #t=4
        res=[]
        for i in range(len(totry)):
            
            p,p1,p2,dd=totry[i]
            a1 = atan2(p1[1]-p[1],p1[0]-p[0])
            a2 = atan2(p2[1]-p[1],p2[0]-p[0])
            if a1<0:a1+=pi
            if a2<0:a2+=pi
            dd=1.7*dd
            evidence=0
            totallines=0
            
            #cv.Line(sg,p,p2,(0,255,0))
            #cv.Line(sg,p,p1,(0,255,0))
            
            #affine transform to local coords
            A = np.array([[p2[0]-p[0],p1[0]-p[0],p[0]],[p2[1]-p[1],p1[1]-p[1],p[1]],[0,0,1]])
            Ainv = np.linalg.inv(A)
            
            v = np.array([[q1[0]],[q1[1]],[1]])

            for j in range(len(lines)):
                a = angs[j]
                ang1 = abs(abs(a-a1)-np.pi/2)
                ang2 = abs(abs(a-a2)-np.pi/2)
                if ang1 > 0.1 and ang2 > 0.1:
                    continue
                
                #test position consistency.
                q1, q2 = lines[j][0][:2],lines[j][0][2:]
                qwe = 0.06

                #test one endpoint                
                v = np.array([[q1[0]],[q1[1]],[1]])                
                vp = np.dot(Ainv, v)
                if vp[0,0] > 1.1 or vp[0,0] < -0.1:
                    continue
                if vp[1,0] > 1.1 or vp[1,0] < -0.1:
                    continue
                if abs(vp[0,0]-1/3.0) > qwe and abs(vp[0,0]-2/3.0) > qwe and abs(vp[1,0]-1/3.0) > qwe and abs(vp[1,0]-2/3.0) > qwe:
                    continue
                
                #the other end point
                v = np.array([[q2[0]],[q2[1]],[1]])
                vp = np.dot(Ainv, v)
                if vp[0,0] > 1.1 or vp[0,0] < -0.1:
                    continue
                if vp[1,0] > 1.1 or vp[1,0] < -0.1:
                    continue
                if abs(vp[0,0]-1/3.0) > qwe and abs(vp[0,0]-2/3.0) > qwe and abs(vp[1,0]-1/3.0) > qwe and abs(vp[1,0]-2/3.0) > qwe:
                    continue
                evidence += 1
            #print evidence
            res.append((evidence, (p,p1,p2)))

        minch = 10000
        res.sort(key=lambda x: x[0], reverse=True)

        if len(res) > 0:
            minps = []
            for i in range(len(res)):
                if res[i][0] > 0.05 * dects:
                    p, p1, p2 = res[i][1]
                    p3 = (p2[0] + p1[0] - p[0], p2[1] + p1[1] - p[1])
                    w = [p, p1, p2, p3]
                    p3 = (prevface[2][0] + prevface[1][0] - prevface[0][0], prevface[2][1] + prevface[1][1] - prevface[0][1])
                    tc = (prevface[0], prevface[1], prevface[2], p3)
                    ch = compfaces(w, tc)
                    if ch < minch:
                        minch = ch
                        minps = (p, p1, p2)

            if len(minps) > 0:
                prevface = minps
                if minch < 10:
                    succ += 1
                    pt = prevface
                    detected = 1

            else:
                succ = 0

            if succ > 2 and 1:
                pt = []
                for i in [1.0/3, 2.0/3]:
                    for j in [1.0/3, 2.0/3]:
                        pt.append((p0[0] + i*v1[0] + j*v2[0], p0[1] + i*v1[1] + j*v2[1]))

                features = np.array(pt, dtype="float32")
                prev_feat = features
                tracking = 1
                succ = 0
    else:
        #we are in tracking mode, we need to fill in pt[] array
        #calculate the pt array for drawing from features
        p=features[0]
        p1=features[1]
        p2=features[2]
        
        v1=(p1[0]-p[0],p1[1]-p[1])
        v2=(p2[0]-p[0],p2[1]-p[1])
        
        pt=[(p[0]-v1[0]-v2[0], p[1]-v1[1]-v2[1]),
            (p[0]+2*v2[0]-v1[0], p[1]+2*v2[1]-v1[1]),
            (p[0]+2*v1[0]-v2[0], p[1]+2*v1[1]-v2[1])]

        prevface=[pt[0],pt[1],pt[2]]

    #use pt[] array to do drawing
    
    if (detected or undetectednum<1) and dodetection:
        #undetectednum 'fills in' a few detection to make
        #things look smoother in case we fall out one frame
        #for some reason
        if not detected: 
            undetectednum+=1
            pt=lastpt
        if detected: 
            undetectednum=0
            lastpt=pt

        #extract the colors
        #convert to HSV
        hsv = cv2.cvtColor(sgc, cv2.COLOR_BGR2HSV)
        hue, sat, val = cv2.split(hsv)

        #do the drawing. pt array should store p,p1,p2
        p3 = (pt[2][0] + pt[1][0] - pt[0][0], pt[2][1] + pt[1][1] - pt[0][1])
        cv2.line(sg, (int(pt[0][0]),int(pt[0][1])), (int(pt[1][0]),int(pt[1][1])), (0, 255, 0), 2)
        cv2.line(sg, (int(pt[1][0]),int(pt[1][1])), (int(p3[0]),int(p3[1])), (0, 255, 0), 2)
        cv2.line(sg, (int(p3[0]),int(p3[1])), (int(pt[2][0]),int(pt[2][1])), (0, 255, 0), 2)
        cv2.line(sg, (int(pt[2][0]),int(pt[2][1])), (int(pt[0][0]),int(pt[0][1])), (0, 255, 0), 2)
        
        #first sort the points so that 0 is BL 1 is UL and 2 is BR
        pt = winded(pt[0], pt[1], pt[2], p3)
        
        #find the coordinates of the 9 places we want to extract over
        v1=(pt[1][0]-pt[0][0], pt[1][1]-pt[0][1])
        v2=(pt[3][0]-pt[0][0], pt[3][1]-pt[0][1])
        p0=(pt[0][0],pt[0][1])
        
        ep=[]
        midpts=[]
        i=1
        j=5
        for k in range(9):
            ep.append((p0[0]+i*v1[0]/6.0+j*v2[0]/6.0, p0[1]+i*v1[1]/6.0+j*v2[1]/6.0))
            i=i+2
            if i==7:
                i=1
                j=j-2
        
        rad= int(ptdst(v1,(0.0,0.0))/6.0)
        cs=[]
        hsvcs=[]
        den=2

        for i, p in enumerate(ep):
            if rad < p[0] < W-rad and rad < p[1] < H-rad:
                col = cv2.mean(sgc[int(p[1]-rad/den):int(p[1]+rad/den),int(p[0]-rad/den):int(p[0]+rad/den)])[:3]
                cv2.circle(sg, (int(p[0]),int(p[1])), rad, tuple(col), -1)
                if i==4:
                    cv2.circle(sg, (int(p[0]),int(p[1])), rad, (0,255,255), 2)
                else:
                    cv2.circle(sg, (int(p[0]),int(p[1])), rad, (255,255,255), 2)
                
                hueavg = cv2.median(hue[int(p[1]-rad/den):int(p[1]+rad/den),int(p[0]-rad/den):int(p[0]+rad/den)])[0]
                satavg = cv2.median(sat[int(p[1]-rad/den):int(p[1]+rad/den),int(p[0]-rad/den):int(p[0]+rad/den)])[0]
                
                cv2.putText(sg, str(int(hueavg)), (int(p[0])+70,int(p[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
                cv2.putText(sg, str(int(satavg)), (int(p[0])+70,int(p[1])+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
                
                if extract:
                    cs.append(col)
                    hsvcs.append((hueavg,satavg))
                            
        if extract:
            extract = not extract
            colors[selected]=cs
            hsvs[selected]=hsvcs
            selected = min(selected+1,5)
    
    #draw faces of the extracted cubes
    x=20
    y=20
    s=13
    for i in range(6):
        if not colors[i]: 
            x+=3*s+10
            continue
        #draw the grid on top
        cv2.rectangle(sg, (x-1,y-1), (x+3*s+5,y+3*s+5), (0,0,0),-1)
        x1,y1=x,y
        x2,y2=x1+s,y1+s
        for j in range(9):
            if didassignments:
                cv2.rectangle(sg, (x1,y1), (x2,y2), mycols[assigned[i][j]],-1)
            else:
                cv2.rectangle(sg, (x1,y1), (x2,y2), colors[i][j],-1)
            x1+=s+2
            if j==2 or j==5: 
                x1=x
                y1+=s+2
            x2,y2=x1+s,y1+s
        x+=3*s+10
    
    #draw the selection rectangle
    x=20
    y=20
    for i in range(selected):
        x+=3*s+10
    
    cv2.rectangle(sg, (x-1,y-1), (x+3*s+5,y+3*s+5), (0,0,255),2)

    lastdetected= len(lines)
    
    #swapping for LK
    prev_grey, grey = grey, prev_grey
    prev_pyramid, pyramid = pyramid, prev_pyramid
    #draw img
    
    cv2.imshow("Fig", sg)

    counter += 1 # global counter
    
    
    # handle events
    c = cv2.waitKey(10) % 0x100
    if c == 27: break # ESC

    # processing depending on the character
    if 32 <= c and c < 128:
        cc = chr(c).lower()
        if cc == ' ':
            # EXTRACT COLORS!!!
            extract = True
        if cc == 'r':
            # reset
            extract = False
            selected = 0
            colors = [[] for i in range(6)]
            didassignments = False
            assigned = [[-1 for i in range(9)] for j in range(6)]
            for i in range(6):
                assigned[i][4] = i
            didassignments = False

        if cc == 'n':
            selected = selected-1
            if selected < 0: selected = 5
        if cc == 'm':
            selected = selected+1
            if selected > 5: selected = 0

        if cc == 'b':
            onlyBlackCubes = not onlyBlackCubes
        if cc == 'd':
            dodetection = not dodetection
        if cc == 'q':
            print(hsvs)
        if cc == 'p':
            # process!!!!
            processColors()
        if cc == 'u':
            didassignments = not didassignments
        if cc == 's':
            cv2.imwrite("C:\\code\\img\\pic" + str(time()) + ".jpg", sgc)
            cv2.destroyWindow("Fig")
        
