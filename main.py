import cv2 as cv
import numpy as np
from mouse import focus
from keyboard import loop
import time 
from detector import detector
from skimage import feature as f
from particleClass import newParticleTracker 
from utils import killMulti
import histo

cap = cv.VideoCapture("./foot.mp4")

#Description de la variable d'environnement{
#	=> env= [x,y,w/2,h/2,bgrFrame,roiMeanSigmaTmp,particleTrackers, PAUSE, lbpFrame]
#		x, y 					:	coords curseur souris temps reel
#		w/2, h/2				:	demi-largeur et demi-hauteur respectives du rectangle de focus
#		bgrFrame				:	frame principale de lecture en canaux rgb
#		roiMeanSigmaTmp	:	pointeur de stockage des moments
#		particleTrackers	:	pointeur de stockage des instances de la classe particleTracker
#		LECTURE				:	1 <=> LECTURE / 0 <=> PAUSE -_-'
#		lbpFrame				:	frame de lecture en mode LBP <-> local Binary Pattern
#}

env = [-42,-42,2,2,None,[],[], 1, None]
cv.namedWindow('win', 0)
cv.setMouseCallback('win', focus, env)

# soustraction temporelle pour denseOpticalFlow (cf moveP in particleClass.py)
prvsGray = None
nxtGray = None

while 1:
	#<--LECTURE-->
	if env[7] == 1:
		if nxtGray is not None:
			prvsGray = nxtGray

		ret, env[4] = cap.read()
		if not ret:
			break
		savedForPause = env[4].copy()
		nxtGray = cv.cvtColor(env[4], cv.COLOR_BGR2GRAY)
		
		#<--playerSubtractDetector-->
		#if len(env[5]) != 0:
		#	detector(env)
		#<-->

		#<--particleFilter-->
		if len(env[6]) != 0:	
			for pTrack in env[6]:
				if pTrack.moveP(prvsGray, nxtGray, env) != -42:
					if pTrack.gaussianWeight(env) != -42:
						pTrack.resample()
						#gere "a deux trois vaches pret" les trackers divergents
						pTrack.calcParticleDispersion(env[6])
			#gere la superposition des trackers
			killMulti(env[6])
		#<-->
		
		#<--LPBFrame-->
		#env[8] = f.local_binary_pattern(nxtGray, histo.nbPoints, histo.radius, histo.METHOD)
		#env[8] = env[8].astype(np.uint8)
		#<-->

	#<--LECTURE-->
	
	#<--Draw and display-->
	a,b,c,d = env[1]-env[3],env[1]+env[3],env[0]-env[2],env[0]+env[2]
	if len(env[5]) == 0:
		cv.rectangle(env[4], (c,a), (d,b), (0,255,0), 1)
	else:
		cv.rectangle(env[4], (c,a), (d,b), (255,0,0), 1)
	if len(env[6]) != 0:
		for pTrack in env[6]:
			pTrack.draw(env)
	cv.imshow('win', env[4])
	if env[8] is not None:
		cv.imshow("LBPFrame", env[8])
	#<-->

	env[4] = savedForPause.copy()
	if not loop(cv.waitKey(30), env):
		break

cv.destroyAllWindows()
