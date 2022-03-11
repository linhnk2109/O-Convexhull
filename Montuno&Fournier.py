import matplotlib.pyplot as plt
import csv
import numpy as np
import math
from datetime import datetime # To measure running time of the algorithm

#==================================BEGIN=====================================#

# Read input points

points = np.genfromtxt('/Users/user/Documents/Data/Data-PointSetinR2/Discs/1000.csv', delimiter=',')



# Time measurement starts here
startTime = datetime.now()


#=============== Start preprocessing step ==================#

#Find 8 special points


maxY = np.nanmax(points[:,1])
minY = np.nanmin(points[:,1])
maxX = np.nanmax(points[:,0])
minX = np.nanmin(points[:,0])


rightPoints = points[np.where(np.equal(points[:,0], maxX))]
leftPoints = points[np.where(np.equal(points[:,0], minX))]
topPoints = points[np.where(np.equal(points[:,1], maxY))]
bottomPoints = points[np.where(np.equal(points[:,1], minY))]

if len(topPoints) == 1:
    top = (topPoints[0],)
else:
    topPoints = sorted(topPoints, key = lambda x : x[0])
    top = (topPoints[0], topPoints[len(topPoints)-1])

    # bottom
if len(bottomPoints) == 1:
    bottom = (bottomPoints[0],)
else:
    bottomPoints = sorted(bottomPoints, key = lambda x : -x[0])
    bottom = (bottomPoints[0], bottomPoints[len(bottomPoints)-1])

    # right
if len(rightPoints) == 1:
   right = (rightPoints[0],)
else:
    rightPoints = sorted(rightPoints, key = lambda x : -x[1])
    right = (rightPoints[0], rightPoints[len(rightPoints)-1])

    # left
if len(leftPoints) == 1:
    left = (leftPoints[0],)
else:
    leftPoints = sorted(leftPoints, key = lambda x : x[1])
    left = (leftPoints[0], leftPoints[len(leftPoints)-1])

if len(top) == 1:
    q1 = qq4 = top[0]
else:
    q1 = top[0]
    qq4 = top[1]
q4 = right[0]
if len(right) == 1:
    qq3 = right[0]
else:
    qq3 = right[1]
q3 = bottom[0]
if len(bottom) == 1:
    qq2 = bottom[0]
else:
    qq2 = bottom[1]
q2 = left[0]
if len(left) == 1:
    qq1 = left[0]
else:
    qq1 = left[1]

# Separate to 4 sets of points
ULPoints = points[np.where((points[:,0] <= q1[0]) &  (points[:,1] >= qq1[1]))]
BLPoints = points[np.where((points[:,0] <= qq2[0]) &  (points[:,1]  <= q2[1]))]
BRPoints = points[np.where((points[:,0] >= q3[0]) &  (points[:,1]  <= qq3[1]))]
URPoints = points[np.where((points[:,0] >= qq4[0]) &  (points[:,1] >= q4[1]))]

#=============== Finish the preprocessing step ==================#



#===== Start to find o.convex by Montuno &  Fournier's algorithm===========#


URConvex = []
ULConvex = []
BLConvex = []
BRConvex = []
    
URPoints = sorted(URPoints, key = lambda x : -x[0]*1000 + x[1]/1000)
if len(URPoints) > 0: URConvex = [URPoints[0]]
for point in URPoints:
    current = URConvex[-1]
    if current[0] == point[0] and current[1] == point[1]: continue
    if point[1] >= current[1]: URConvex.append(point)
URConvex = [qq3, q4] + URConvex + [qq4]

ULPoints = sorted(ULPoints, key = lambda x : x[0]*1000 + x[1]/1000)
if len(ULPoints) > 0: ULConvex = [ULPoints[0]]
for point in ULPoints:
    current = ULConvex[-1]
    if current[0] == point[0] and current[1] == point[1]: continue
    if point[1] >= current[1]: ULConvex.append(point)
ULConvex.reverse()
ULConvex = [qq4, q1] + ULConvex + [qq1]

BLPoints = sorted(BLPoints, key = lambda x : x[0]*1000 - x[1]/1000)
if len(BLPoints) > 0: BLConvex = [BLPoints[0]]
for point in BLPoints:
    current = BLConvex[-1]
    if current[0] == point[0] and current[1] == point[1]: continue
    if point[1] <= current[1]: BLConvex.append(point)
BLConvex = [qq1, q2] + BLConvex + [qq2]

BRPoints = sorted(BRPoints, key = lambda x : -x[0]*1000 - x[1]/1000)
if len(BRPoints) > 0: BRConvex = [BRPoints[0]]
for point in BRPoints:
    current = BRConvex[-1]
    if current[0] == point[0] and current[1] == point[1]: continue
    if point[1] <= current[1]: BRConvex.append(point)
BRConvex.reverse()
BRConvex = [qq2, q3] + BRConvex + [qq3]

output = [URConvex, ULConvex, BLConvex, BRConvex]

#============== Finish  Montuno &  Fournier's algorithm ===============#


# Time measurement ends here
endTime = datetime.now()
timeInterval = endTime - startTime
timeInSecond = timeInterval.total_seconds()
print(f"Algorithm running time: {timeInSecond} seconds.")


#============== plot the c.o. convex hull ===============#


def convexPlot(points, drawRule):
    for i in range(len(points) - 1):
        start = points[i]
        end = points[i + 1]
        buffer = drawRule(start, end)
        plt.plot([start[0], buffer[0]], [start[1], buffer[1]], 'b-')
        plt.plot([buffer[0], end[0]], [buffer[1], end[1]], 'b-')

def drawRule1(start, end):
    return [end[0], start[1]]

def drawRule2(start, end):
    return [start[0], end[1]]


# Draw lines
fig, ax = plt.subplots()

# Input points in blue
ax.plot([x[0] for x in points], [x[1] for x in points], 'r.')

# Orthogonal convex hull in red
convexPlot(output[0], drawRule1)
convexPlot(output[1], drawRule2)
convexPlot(output[2], drawRule1)
convexPlot(output[3], drawRule2)

plt.ylabel('Y')
plt.xlabel('X')
plt.show()



