# -*- coding: UTF-8 -*-
''' 
  A_____A
 /  = . =\   < Developed by CKB >
/     w   \
current version: 1.3

update log:
ver 1.0 - initial release
ver 1.1 - fix weird acceleration
ver 1.2 - fix "ball stuck in wall" problem
ver 1.3 - add more balls, with collision

'''
from visual import *


########important variables##########
r = 0.05 #radius of ball
N = 50
#####functions#####
def dist(x1,y1,x2,y2):
    return sqrt((x1-x2)**2+(y1-y2)**2)
def reflect(w,v):   #ball hit wall
    '''
    w,v must be list/array/vector with 
    '''
    w,v = vector(w),vector(v)
    f = vector(-w[1],w[0],0) #法向量
    unit_f=f/abs(f) #法向量的單位向量
    re = v + abs(dot(v,f)/abs(f))*unit_f*2
#    return re
#'''
    if abs(abs(re)-abs(v)) <= 0.001*abs(v):
        if dot(v,f)<0:
            return re
        else:
            #print('!!!!!!!!!!!!!!!!false hit!!!!!!!!!!!!!!!')
            return v
    else:
        #print("back hit")
        w=-w
        f = vector(-w[1],w[0],0) #法向量
        unit_f=f/abs(f) #法向量的單位向量
        if dot(v,f)<0:
            re = v + abs(dot(v,f)/abs(f))*unit_f*2
            return re
        else:
            #print('!!!!!!!!!!!!!!!!false hit!!!!!!!!!!!!!!!')
            return v
#'''
def vcollision(a1p, a2p, a1v,a2v): #ball hit ball
    v1prime = a1v - (a1p - a2p)  * sum((a1v-a2v)*(a1p-a2p)) / sum((a1p-a2p)**2)
    v2prime = a2v - (a2p - a1p)  * sum((a2v-a1v)*(a2p-a1p)) / sum((a2p-a1p)**2)
    return v1prime, v2prime

def checkhit(w1,w2,b):
    wx1,wy1 = w1[0],w1[1]
    wx2,wy2 = w2[0],w2[1]
    bx ,by  =  b[0], b[1]
    area = 0.5*abs(wx1*wy2+wx2*by+bx*wy1-wy1*wx2-wy2*bx-by*wx1)
    wall = sqrt((wx1-wx2)**2+(wy1-wy2)**2)
    f = vector(-w[1],w[0],0) #法向量
    
    if ((2*area/wall)<=r or (dist(bx,by,wx1,wy1)<=r or dist(bx,by,wx2,wy2)<=r)) and not(dist(bx,by,wx1,wy1)>wall or dist(bx,by,wx2,wy2)>wall):
        '''
        print(wall)
        print(dist(bx,by,wx1,wy1))
        print(dist(bx,by,wx2,wy2))
        #'''
        return True
    else: return False    
#initialize!
scene = display(width=800, height=800,background=(0.0,0.0,0))
#wall = [[1,1],[1,-1],[-1,-1],[-0.8,0],[0,0],[0,-0.8],[1,1]]  #L shape
wall = [[2,2],[2,-2],[-2,-2],[-2,2],[2,2]]   #square
#wall = [[1,1],[1,0],[-1,-1],[-1,0],[1,2],[1,3]]
#wall = [[780,0],[1150,-140],[1180,-130],[1170,-90],[970,0],[780,0]]
#wall = [[0,60],[300,60],[850,240],[900,250],[940,220],[950,170],[940,130],[900,100],[730,60],[1170,40],
#        [1400,60],
#        [1400,0],[1070,0],[1200,-60],[1230,-90],[1240,-130],[1230,-170],[1180,-190],[1130,-180],[610,0],[300,20],
#        [0,0],[0,60]]
container = curve(pos=wall) 
random.seed(1)
v = random.uniform(-10,10,(N,3))
for i in range(len(v)):
    v[i][2] = 0
for i in range(len(wall)):
    wall[i] = vector(wall[i])

pos_arr = random.uniform(-2,2,(N,3))
for i in range(len(pos_arr)):
    pos_arr[i][2] = 0
ball = [sphere(radius = r,make_trail=False,
               color=color.yellow) for i in range(N)]

ball[0].color = color.red
ball[0].make_trail = True
for i in range(N):
    ball[i].pos = vector(pos_arr[i])
#testing area    

#main code
t = 0
dt =0.0005

while True:
    rate(500)
    t+=dt
    for j in range(N):
        for k in range(2):
            pos_arr[j][k] += v[j][k]*dt
        ball[j].pos = vector(pos_arr[j])
        #'''
        r_array = pos_arr-pos_arr[:,newaxis]            # all pairs of atom-to-atom vectors
        rmag = sum(square(r_array),-1)                      # atom-to-atom distance squared
        hit = nonzero((rmag < 4*r**2) - identity(N))
        hitlist = zip(hit[0], hit[1])     
        for p,q in hitlist:
            if sum((pos_arr[p]-pos_arr[q])*(v[p]-v[q])) < 0 :       # check if approaching
                v[p], v[q] = vcollision(pos_arr[p], pos_arr[q], v[p], v[q])
        #'''
        for i in range(len(wall)-1):
            w = wall[i]-wall[i+1]
            f = vector(-w[1],w[0]) #法向量
            if checkhit(wall[i],wall[i+1],ball[j].pos) and dot([v[j][0],v[j][1],0],f)<0:
                #print("hit: wall %d and %d"%(i,i+1))
                v[j] = reflect(wall[i]-wall[i+1],v[j])
                #print(t,abs(v))
            
