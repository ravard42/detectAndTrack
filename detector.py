import cv2 as cv
import math as m
from mouse import focus
from utils import dist

minArea = 25
fgbg = cv.bgsegm.createBackgroundSubtractorMOG(history=3,backgroundRatio=0.1, nmixtures=3, noiseSigma = 7)

minDist = 20

def newTrack(env):
	for p in env[6]:
		if dist(p, env[0], env[1]) < minDist:
			return 0
	return 1

def detector(env):
	fgmask = fgbg.apply(env[4])
	fgmask = cv.GaussianBlur(fgmask, (15, 15), 0)
	fgmask = cv.threshold(fgmask, 42, 255, cv.THRESH_BINARY)[1]
	fgmask = cv.dilate(fgmask, None, iterations= 2)
	img, contours, hierarchy = cv.findContours(fgmask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
	for c in contours:
		if cv.contourArea(c) < minArea:
			continue
		coord = cv.boundingRect(c)
		env[0], env[1] = int(coord[0] + coord[2] / 2), int(coord[1] + (coord[3] / 2))
		if newTrack(env):
			focus(cv.EVENT_FLAG_RBUTTON, env[0], env[1], None, env)
	cv.imshow('fgbg',fgmask)
