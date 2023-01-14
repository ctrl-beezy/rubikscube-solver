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

def processColors(hsvals):
    assigned=[[-1 for i in range(9)] for j in range(6)]
    useRGB = False
    bestj = 0
    besti = 0
    bestcon = 0
    matchesto = 0
    bestd = 10001
    taken = [0 for i in range(6)]
    done = 0
    opposite = {0: 2, 1: 3, 2: 0, 3: 1, 4: 5, 5: 4} # dict of opposite faces
    # possibilities for each face
    poss = {}
    for j, f in enumerate(hsvals):
        for i, s in enumerate(f):
            poss[j, i] = range(6)

    toloop = hsvals
    
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

    return assigned