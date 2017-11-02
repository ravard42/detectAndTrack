import numpy as np
import cv2 as cv
import math as m
from random import random as r
from random import gauss as g
from histo import BGRRoiMeanSigma
from histo import LBPRoiMeanSigma
from utils import outOfRange
from utils import gaussian
from utils import dist

	
class newParticleTracker:
	nbPart = 50
	stdMove = 2.3
	seqFrame = 20
	maxDisp = 140
	
	def __init__(self, x, y, w2, h2, histMoments):
		self.x = x
		self.y = y
		self.w2 = w2
		self.h2 = h2
		self.BGRHMs = histMoments[0]
		#self.LBPHMs = histMoments[1]
		self.particle = self.randParticles()
		self.disp = [0, 0]

	#def refreshHisto(self, frame):
	#	roi = frame[int(self.y-6):int(self.y+7), int(self.x-2):int(self.x+3)]
	#	BGRHMs = RGBRoiMeanSigma(roi)	
	#	LBPHMs = LBPRoiMeanSigma(roi)

	def randParticles(self):
		ret = (np.random.rand(self.nbPart, 3)).astype(np.float32)
		ret[...,0] *= self.w2 * 2 - 1
		ret[...,0] += self.x - self.w2 + 1
		ret[...,1] *= self.h2 * 2 - 1
		ret[...,1] += self.y - self.h2 + 1

		return ret
	
	def moveP(self, prvs, nxt, env):
		a,b,c,d = self.y-self.h2+1,self.y+self.h2,self.x-self.w2+1,self.x+self.w2
		if outOfRange(env, c, a, self) or outOfRange(env, d, b, self):
			return -42
		else:
			flow = cv.calcOpticalFlowFarneback(prvs[a:b,c:d],nxt[a:b,c:d], None, 0.5, 3, 15, 3, 5, 1.2, 0)
			dx = np.mean(flow[...,0])
			dy = np.mean(flow[...,1])
			for i in range(self.nbPart):
				self.particle[i][0] += g(dx, self.stdMove)
				self.particle[i][1] += g(dy, self.stdMove)
		return 1

	def gaussianWeight(self, env):
		bgr = env[4]
		#lbp = env[8]
		i = 0
		for p in self.particle:
			x,y,w = p.ravel()
			x,y = int(x), int(y)
			w = 1.0
			if outOfRange(env, x, y, self):
				return -42
			else:
				for chan in range(3):
					w *= gaussian(bgr[y][x][chan], self.BGRHMs[chan][0], self.BGRHMs[chan][1])
				#w *= gaussian(lbp[y][x], self.LBPHMs[0], self.LBPHMs[1])
				self.particle[i][2] = w
				i += 1
		return 1
	
	def calcParticleDispersion(self, particles):
		if self.disp[0] < self.seqFrame:
			self.disp[1] += np.std(self.particle[...,0]) + np.std(self.particle[...,1])
			self.disp[0] += 1
		else:
			if self.disp[1] > self.maxDisp:
				particles.remove(self)
			else:
				self.disp[1] = 0
				self.disp[0] = 0

	def resample(self):
		reWeight = 1
		for p in self.particle:
			if p[2] != 0:
				reWeight = 0
				break
		if reWeight == 1:
			self.particle[...,2] = 42


		index = int(r() * self.nbPart)
		beta = 0.0
		mw = max(self.particle[...,2])
	
		tmp = (np.random.rand(self.nbPart, 3)).astype(np.float32)
		for i in range(self.nbPart):
			beta += r() * 2.0 * mw
	
			while beta > self.particle[index][2]:
				beta -= self.particle[index][2]
				index = (index + 1) % self.nbPart
			
			tmp[i][0] = self.particle[index][0]
			tmp[i][1] = self.particle[index][1]
		self.particle = tmp

	def draw(self, env):
		pX, pY = 0, 0
		for p in self.particle:
			x,y,w = p.ravel()
			pX += x
			pY += y
			cv.circle(env[4],(int(x),int(y)),0,(255,0,0),-1)
		self.x = int(pX)/self.nbPart
		self.y = int(pY)/self.nbPart
		a,b,c,d = self.y-self.h2,self.y+self.h2,self.x-self.w2,self.x+self.w2
		cv.rectangle(env[4], (c,a), (d,b), (255,0,255), 1)
