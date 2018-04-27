# -*- coding: UTF-8 -*-
''' 
  A_____A
 /  = . =\   < Developed by CKB >
/     w   \
current version: 1.2

update log:
ver 1.0 - initial release
ver 1.1 - fix weird acceleration
ver 1.2 - fix "ball stuck in wall" problem

'''
from visual import *
########important variables##########
r = 0.05

#####functions#####
def dist(x1,y1,x2,y2):
    return sqrt((x1-x2)**2+(y1-y2)**2)
def reflect(w,v):   #ball hit wall
    f = vector(-w[1],w[0],0) #法向量
    unit_f=f/abs(f) #法向量的單位向量
    re = v + abs(dot(v,f)/abs(f))*unit_f*2
#    return re
#'''
    if abs(abs(re)-abs(v)) <= 0.001*abs(v):
        if dot(v,f)<0:
            return re
        else:
            print('!!!!!!!!!!!!!!!!false hit!!!!!!!!!!!!!!!')
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
            print('!!!!!!!!!!!!!!!!false hit!!!!!!!!!!!!!!!')
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
wall = [[1,1],[1,-1],[-1,-1],[-0.8,0],[0,0],[0,-0.8],[1,1]]  #L shape
#wall = [[1,1],[1,-1],[-1,-1],[-1,1],[1,1]]   #square
#wall = [[1,1],[1,0],[-1,-1],[-1,0],[1,2],[1,3]]
#wall = [[780,0],[1150,-140],[1180,-130],[1170,-90],[970,0],[780,0]]
#wall = [[0,60],[300,60],[850,240],[900,250],[940,220],[950,170],[940,130],[900,100],[730,60],[1170,40],
#        [1400,60],
#        [1400,0],[1070,0],[1200,-60],[1230,-90],[1240,-130],[1230,-170],[1180,-190],[1130,-180],[610,0],[300,20],
#        [0,0],[0,60]]
container = curve(pos=wall) 

v    = vector(-10,10)
for i in range(len(wall)):
    wall[i] = vector(wall[i])

ball = sphere(pos = vector(0.5,-0.5,0),radius = r,make_trail=True,retain=100,color=color.yellow)
#testing area    

#main code
t = 0
dt =0.0005
while True:
    rate(500)
    t+=dt
    ball.pos += v*dt
    for i in range(len(wall)-1):
        w = wall[i]-wall[i+1]
        f = vector(-w[1],w[0],0) #法向量
        if checkhit(wall[i],wall[i+1],ball.pos) and dot(v,f)<0:
            print("hit: wall %d and %d"%(i,i+1))
            v = reflect(wall[i]-wall[i+1],v)
            print(t,abs(v))
            
