import cv2 as cv
import numpy as np
from mouse import focus
from keyboard import loop
import time 
from detector import detector
from skimage import feature as f
from particleClass import newParticleTracker 
from utils import killMulti

#cap = cv.VideoCapture(0)
#time.sleep(0.5)
#cap.set(3, winSize)
#cap.set(4, winSize)
cap = cv.VideoCapture("../mp4/foot.mp4")


# => env= [x,y,w/2,h/2,bgrFrame,roiMeanSigmaTmp,particleTrackers, PAUSE, lbpFrame]
env = [-42,-42,2,2,None,[],[], 0, None]
cv.namedWindow('win', 0)
cv.setMouseCallback('win', focus, env)

prvs = None
nxt = None

nbPoints = 8
radius = 1
METHOD = "default"

while 1:
	if env[7] == 0:
		if nxt is not None:
			prvs = nxt
		ret, env[4] = cap.read()
		gray = cv.cvtColor(env[4], cv.COLOR_BGR2GRAY)
		#env[8] = f.local_binary_pattern(gray, nbPoints, radius, METHOD)
		#env[8] = env[8].astype(np.uint8)
		#cv.imshow("lbpFrame", env[8])
		if not ret:
			break
		save = env[4].copy()
		nxt = gray
		#if len(env[5]) != 0:
		#	detector(env)
		if len(env[6]) != 0:	
			for pTrack in env[6]:
				if pTrack.moveP(prvs, nxt, env) != -42:
					if pTrack.gaussianWeight(env) != -42:
						pTrack.resample()
						pTrack.calcParticleDispersion(env[6])
			killMulti(env[6])
			for pTrack in env[6]:
				pTrack.draw(env)

	a,b,c,d = env[1]-env[3],env[1]+env[3],env[0]-env[2],env[0]+env[2]
	if len(env[5]) == 0:
		cv.rectangle(env[4], (c,a), (d,b), (0,255,0), 1)
	else:
		cv.rectangle(env[4], (c,a), (d,b), (255,0,0), 1)
	
	cv.imshow('win', env[4])
	env[4] = save.copy()
	
	if not loop(cv.waitKey(30), env):
		break

#cap.release()
cv.destroyAllWindows()
