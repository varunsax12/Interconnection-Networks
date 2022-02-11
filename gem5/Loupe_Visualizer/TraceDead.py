from operator import attrgetter
from flit import Flit

class routes:
    def __init__(self, srcID, destID, srcDir, destDir):
        self.srcID = srcID
        self.destID = destID
        self.srcDir = srcDir
        self.destDir = destDir


def findLoop(flitIn, flitsList, routesList, loopedRouters, numVC):
    flitIn.traversed = True
    outBlockFlits = []
    # find which port this 
    nextPort = next((x for x in routesList if (x.srcID == flitIn.router)and(x.srcDir == flitIn.outport)), None)
    destDir = nextPort.destDir
    destRID = nextPort.destID

    for flit in flitsList:
        if(flit.router == destRID)and(flit.in_dir == destDir):
            outBlockFlits.append(flit)
    strOut = "Flit " + str(flitIn.id) + " at R" + str(flitIn.router) + " waiting for "
    if(len(outBlockFlits) != numVC):
        return False
    for flit in outBlockFlits:
        if(flit.router not in loopedRouters):
            loopedRouters.append(flit.router)
        
        strOut2 = strOut + "Flit " + str(flit.id) + " at R" + str(flit.router)
        # print(strOut2)
    
    
    loopFlags =[]
    for flit in outBlockFlits:
        if flit.traversed == 0:
            loopfound = findLoop(flit, flitsList, routesList,loopedRouters, numVC)
            loopFlags.append(loopfound)
    if(0 in loopFlags):
        return False
    else:
        return True
    

def flit_trace_no_file(flitSet, num_rows, num_cols, flitID, numVC):

    # print("Finding flit: " + str(flitID))

    

    # read in the router configuration file
    routerMapFileName = "routerConfig/Mesh_"+str(num_cols)+"_"+str(num_rows)
    routerMapList = []
    with open(routerMapFileName, 'r') as routerMapFile:
        routerMapList = routerMapFile.readlines()
        routerMapFile.close()

    if (len(routerMapList) == 0):
        print("Error reading router config file")
        return None, False

    routesList = []

    # Convert to flit directly
    for eachFlit in flitSet:
        eachFlit.traversed = False

    for line in routerMapList:
        lineSplit1 = line.split(':')
        lineSplit2 = lineSplit1[0].split('->')
        lineSplit3 = lineSplit1[1].split('->')
        lineSplit3[1] = lineSplit3[1].replace('\n', '')
        routesList.append(routes(int(lineSplit2[0]), int(lineSplit2[1]), lineSplit3[0], lineSplit3[1]))

    # print(flitSet)

    # get flit to be observed
    flit2look = next((x for x in flitSet if x.id == flitID), None)
    if(flit2look is None):
        print("No ID Found or Flit is in link")
        return None, False

    # start looking at which flit is max flit waiting for.

    loopedRouters = []
    loopFound = findLoop(flit2look, flitSet, routesList, loopedRouters, numVC)

    return loopedRouters, loopFound
