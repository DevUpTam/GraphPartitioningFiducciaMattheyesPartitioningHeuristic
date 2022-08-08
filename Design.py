G = dict()
fp = open("Sample1.txt", 'r')
for line in fp:
    inputs1 = line.split(" ")
    if inputs1[0][0] == 'I' or inputs1[0][0] == 'O':
        j = inputs1[0].index('(')
        k = inputs1[0].index(')')
        inputs1 = inputs1[0][j+1:k]
        G[inputs1] = []
        continue

    if inputs1[0].isdigit() is True:
        inputs1.remove('=')
        inputs1[1] = inputs1[1][0: len(inputs1[1]) - 1]
        for i in range(0, len(inputs1[1]), 1):
            if inputs1[1][i].isdigit():
                inputs1[1] = inputs1[1][i:]
                break

        for i in range(0, len(inputs1[2]), 1):
            if not inputs1[2][i].isdigit():
                inputs1[2] = inputs1[2][0:i]
                break

        if inputs1[0] in G.keys():
            G[inputs1[0]].append(inputs1[1])
            G[inputs1[0]].append(inputs1[2])

        if inputs1[1] in G.keys():
            G[inputs1[1]].append(inputs1[0])
            G[inputs1[1]].append(inputs1[2])

        if inputs1[2] in G.keys():
            G[inputs1[2]].append(inputs1[0])
            G[inputs1[2]].append(inputs1[1])

        if inputs1[0] not in G.keys():
            G[inputs1[0]] = [inputs1[1]]
            G[inputs1[0]].append(inputs1[2])

        if inputs1[1] not in G.keys():
            G[inputs1[1]] = [inputs1[0]]
            G[inputs1[1]].append(inputs1[2])

        if inputs1[2] not in G.keys():
            G[inputs1[2]] = [inputs1[0]]
            G[inputs1[2]].append(inputs1[1])

# Let the graph be represented as G

#G = {'A': ['C'], 'B': ['C', 'D'], 'C': ['A', 'B'], 'D': ['B']}

# maxGain = 2
# G = {'A': ['D'], 'B': ['C'], 'C': ['B', 'D', 'E'], 'D': ['A', 'C', 'E'], 'E': ['C', 'D']}
# maxGain = 3
# G = {'A': ['P', 'Q', 'S'], 'B': ['E', 'P', 'Q'], 'C': ['R', 'S'], 'D': ['E', 'R', 'S'], 'E': ['B', 'D'],
#     'P': ['A', 'B', 'I1'],
#     'Q': ['A', 'B', 'I2'], 'R': ['C', 'D', 'I3'], 'S': ['A', 'C', 'D'], 'I1': ['P'], 'I2': ['Q'], 'I3': ['R']}

maxGain = 0

#------------------------------------------

for i in G.keys():
    if len(G[i])>maxGain:
        maxGain = len(G[i])

bestSolution = [[], []]

leftGainBucket = dict()
rightGainBucket = dict()

leftBucket = list()
rightBucket = list()

lockedVertices = dict()
balanceFactor = []

# Dividing the vertices into buckets

count = 0
for i in G.keys():
    if count % 2 == 0:
        leftBucket.append(i)
    else:
        rightBucket.append(i)
    count+=1

# initialising Gain Buckets
def initialiseBucket():
    for i1 in range(maxGain, -maxGain-1, -1):
        leftGainBucket[i1] = list()
        rightGainBucket[i1] = list()


def FindCut():
    netCut = 0
    for i1 in leftBucket:
        for j1 in G[i1]:
            if j1 in rightBucket:
                netCut+=1
    return netCut

def FindGain():
    leftGainBucket.clear()
    rightGainBucket.clear()
    initialiseBucket()
    for i1 in rightBucket:
        if i1 not in lockedVertices.keys():
            sameSideEdge = 0
            oppSideEdge = 0
            adjacentVertices = G[i1]
            for i2 in adjacentVertices:
                if i2 in rightBucket:
                    sameSideEdge += 1
                else:
                    oppSideEdge += 1

            gain = oppSideEdge - sameSideEdge
            rightGainBucket[gain].append(i1)

    for i1 in leftBucket:
        if i1 not in lockedVertices.keys():
            sameSideEdge = 0
            oppSideEdge = 0
            adjacentVertices = G[i1]
            for i2 in adjacentVertices:
                if i2 in leftBucket:
                    sameSideEdge += 1
                else:
                    oppSideEdge += 1
            gain = oppSideEdge - sameSideEdge
            leftGainBucket[gain].append(i1)


def FMpass(gainBucket, typeOfBucket):
    list1 = list()
    list2 = list()
    vertex = ''
    if typeOfBucket == 'Left':
        list1 = leftBucket
        list2 = rightBucket
    else:
        list1 = rightBucket
        list2 = leftBucket

    for i1 in range(maxGain, -maxGain-1, -1):
        if len(gainBucket[i1])>0:
            vertex = gainBucket[i1].pop(0)
            break
    # print(vertex, typeOfBucket, leftBucket, rightBucket, leftGainBucket, rightGainBucket)
    list1.remove(vertex)
    list2.append(vertex)
    netCut = FindCut()
    print(leftBucket, rightBucket, netCut)
    lockedVertices[vertex] = netCut
    z = abs(len(leftBucket) - len(rightBucket))
    balanceFactor.append(z)
    FindGain()


def FeducciMathyyes():
    initialLeftBucketLength = len(leftBucket)
    initialRightBucketLength = len(rightBucket)
    if initialLeftBucketLength>initialRightBucketLength:
        for i1 in range(0, initialRightBucketLength, 1):
            FMpass(leftGainBucket, 'Left')
            FMpass(rightGainBucket, 'Right')
        FMpass(leftGainBucket, 'Left')
    elif initialRightBucketLength>initialLeftBucketLength:
        for i1 in range(0, initialLeftBucketLength, 1):
            FMpass(rightGainBucket, 'Right')
            FMpass(leftGainBucket, 'Left')
        FMpass(rightGainBucket, 'Right')
    else:
        for i1 in range(0, len(rightBucket), 1):
            FMpass(rightGainBucket, 'Right')
            FMpass(leftGainBucket, 'Left')

def BackTrack():
    balanceVar = min(balanceFactor)
    minCut = lockedVertices[list(lockedVertices.keys())[0]]
    for i1 in list(lockedVertices.keys()):
        if lockedVertices[i1] < minCut:
            minCut = lockedVertices[i1]
    list1 = list(lockedVertices.keys())
    list1.reverse()
    #print(leftBucket, rightBucket)
    #print(list1)
    iterVar = 0
    for i1 in list1:
        if i1 in leftBucket:
            leftBucket.remove(i1)
            rightBucket.append(i1)
        else:
            rightBucket.remove(i1)
            leftBucket.append(i1)

        if lockedVertices[i1]==minCut:

            bestSolution[0] = leftBucket
            bestSolution[1] = rightBucket

            if balanceFactor[iterVar]==balanceVar:
                break

        iterVar+=1
    print("Final Net Cut: ", minCut)


initialCut = FindCut()
initialiseBucket()
FindGain()
# print(leftGainBucket)
# print(rightGainBucket)
print("Initial Net Cut: ", initialCut)
print("Initial left Side Of Partition: ", leftBucket)
print("Initial right Side Of Partition: ", rightBucket)
FeducciMathyyes()
print("Locked Vertices and Associated Net Cut : ", lockedVertices)
# print(leftBucket)
# print(rightBucket)
print("\nAfter FM Partitioning Heuristic Applied: ")
BackTrack()
print("Left Side of the Partition: ", bestSolution[0])
print("Right Side of the Partition: ", bestSolution[1])