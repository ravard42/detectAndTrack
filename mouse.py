import cv2 as cv
import numpy as np

from histo import BGRRoiMeanSigma
from histo import LBPRoiMeanSigma

from particleClass import newParticleTracker
from utils import outOfRange

def focus(event, x, y, flags,  env):
	if event == cv.EVENT_MOUSEMOVE:
		env[0], env[1] = x, y
	if event == cv.EVENT_FLAG_LBUTTON and len(env[5]) == 0:
		a,b,c,d = env[1]-env[3]+1,env[1]+env[3],env[0]-env[2]+1,env[0]+env[2]
		if outOfRange(env, c, a, None) or outOfRange(env, d, b, None):
			print "outOfRange"
		else:
			roi = env[4][a:b,c:d]
			env[5].append(BGRRoiMeanSigma(roi))
			env[5].append(LBPRoiMeanSigma(roi))
			env[2], env[3] = 4, 8
	if event == cv.EVENT_FLAG_RBUTTON and len(env[5]) != 0:
		env[6].append(newParticleTracker(env[0], env[1], env[2], env[3], env[5]))
