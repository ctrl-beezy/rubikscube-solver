def processColors(hsvals):

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
    for j, f in enumerate(hsvs):
        for i, s in enumerate(f):
            poss[j, i] = range(6)

    # we are looping different arrays based on the useRGB flag
    toloop = hsvs
    
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

    didassignments = True