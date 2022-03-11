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

set1 = points[np.where((points[:,0] <= q1[0]) &  (points[:,1] >= qq1[1]))]
set2 = points[np.where((points[:,0] <= qq2[0]) &  (points[:,1]  <= q2[1]))]
set3 = points[np.where((points[:,0] >= q3[0]) &  (points[:,1]  <= qq3[1]))]
set4 = points[np.where((points[:,0] >= qq4[0]) &  (points[:,1] >= q4[1]))]


#=============== Finish the preprocessing step ==================#



#============ Start to find o.convex by O-Quickhull ===============#

def find_o_hull1(set1, q1, qq1):
    if len(set1) == 0:
        return []
    
    key1 = (set1[:,0] - q1[0])*(set1[:,0] - q1[0]) + (set1[:,1] - qq1[1])*(set1[:,1] - qq1[1])
    maxset1 = np.nanmax(key1)
    new_point1 = set1[np.where(key1 == maxset1)][0]
    
    new_set11 = set1[np.where(set1[:,1] > new_point1[1])]
    new_set12 = set1[np.where(set1[:,0] < new_point1[0])]
    
    
    return find_o_hull1(new_set11, q1, new_point1) + [new_point1] + find_o_hull1(new_set12, new_point1, qq1)

#####################################################

def find_o_hull2(set2, q2, qq2):
    if len(set2) == 0:
        #po = ortho(pf, pt, xInc, yInc) # SUPPORT POINTS
        return []

    
    key2 = (set2[:,0] - qq2[0])*(set2[:,0] - qq2[0]) + (set2[:,1] - q2[1])*(set2[:,1] - q2[1])
    maxset2 = np.nanmax(key2)
    new_point2 = set2[np.where(key2 == maxset2)][0]
    
    new_set21 = set2[np.where(set2[:,0] < new_point2[0])]
    new_set22 = set2[np.where(set2[:,1] < new_point2[1])]
    
    
    return find_o_hull2(new_set21, q2, new_point2) + [new_point2] + find_o_hull2(new_set22, new_point2, qq2)

#####################################################
def find_o_hull3(set3, q3, qq3):
    if len(set3) == 0:
        #po = ortho(pf, pt, xInc, yInc) # SUPPORT POINTS
        return []
 
    key3 = (set3[:,0] - q3[0])*(set3[:,0] - q3[0]) + (set3[:,1] - qq3[1])*(set3[:,1] - qq3[1])
    maxset3 = np.nanmax(key3)
    new_point3 = set3[np.where(key3 == maxset3)][0]
    
    new_set31 = set3[np.where(set3[:,1] < new_point3[1])]
    new_set32 = set3[np.where(set3[:,0] > new_point3[0])]
    
    return find_o_hull3(new_set31, q3, new_point3) + [new_point3] + find_o_hull3(new_set32, new_point3, qq3)

#####################################################

def find_o_hull4(set4, q4, qq4):
    if len(set4) == 0:
        return []

    key4 = (set4[:,0] - qq4[0])*(set4[:,0] - qq4[0]) + (set4[:,1] - q4[1])*(set4[:,1] - q4[1])
    maxset4 = np.nanmax(key4)
    new_point4 = set4[np.where(key4 == maxset4)][0]
    
    new_set41 = set4[np.where(set4[:,0] > new_point4[0])]
    new_set42 = set4[np.where(set4[:,1] > new_point4[1])]
    
    return find_o_hull4(new_set41, q4, new_point4) + [new_point4] + find_o_hull4(new_set42, new_point4, qq4)
 
 #####################################################

arranged_points = []
arranged_points = arranged_points + [q1] + find_o_hull1(set1, q1, qq1) + [qq1]
arranged_points = arranged_points + [q2] + find_o_hull2(set2, q2, qq2) + [qq2]
arranged_points = arranged_points + [q3] + find_o_hull3(set3, q3, qq3) + [qq3]
arranged_points = arranged_points + [q4] + find_o_hull4(set4, q4, qq4) + [qq4]


#============== Finish  O-Quickhull ===============#


# Time measurement ends here
endTime = datetime.now()
timeInterval = endTime - startTime
timeInSecond = timeInterval.total_seconds()
print(f"Algorithm running time: {timeInSecond} seconds.")


#============== plot the c.o. convex hull ===============#

# adding points (angle 270)

arranged_points.append(arranged_points[0])
S = []
n = len(arranged_points)

#print("number points to plot: ", n)
for i in range(0, n-1):
    
    if arranged_points[i+1][0] > arranged_points[i][0] and arranged_points[i+1][1] > arranged_points[i][1]:
        
        p3 = [arranged_points[i][0], arranged_points[i+1][1]]
        
        S.append([i+1, p3])

    elif arranged_points[i+1][0] > arranged_points[i][0] and arranged_points[i+1][1] < arranged_points[i][1]:
        
        p3 = [arranged_points[i+1][0], arranged_points[i][1]]
        
        S.append([i+1, p3])

    elif arranged_points[i+1][0] < arranged_points[i][0] and arranged_points[i+1][1] < arranged_points[i][1]:
    
        p3 = [arranged_points[i][0], arranged_points[i+1][1]]
    
        S.append([i+1, p3])

    elif arranged_points[i+1][0] < arranged_points[i][0] and arranged_points[i+1][1] > arranged_points[i][1]:
        
        p3 = [arranged_points[i+1][0], arranged_points[i][1]]
        
        S.append([i+1, p3])



for i in range(len(S)):
    arranged_points.insert(S[i][0]+i, S[i][1])
arranged_points.append(arranged_points[0])
############################################################
# Draw lines
fig, ax = plt.subplots()

# Input points in red 
ax.plot([x[0] for x in points], [x[1] for x in points], 'r.')

# Orthogonal convex hull points in blue
ax.plot([x[0] for x in arranged_points], [x[1] for x in arranged_points], 'b-')

plt.ylabel('Y')
plt.xlabel('X')
plt.show()




