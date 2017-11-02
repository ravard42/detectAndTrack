import cv2 as cv
import math as m

#BGR STYLE
def histMean(hist):
	nbPix = int(sum(hist)[0])
	mean = 0
	for i in range(len(hist)):
		mean += i * hist[i][0]
	mean /= nbPix
	return mean

def histDeviation(hist, mean):
	nbPix = int(sum(hist)[0])
	dev = 0
	for i in range(len(hist)):
		dev += pow(i - mean, 2) * hist[i][0]
	dev /= nbPix
	return m.sqrt(dev)

def BGRRoiMeanSigma(roi):
	ret = []
	for channel in range(3):
		hist = cv.calcHist([roi], [channel], None, [256], [0,256])
		mu = histMean(hist)
		sigma = histDeviation(hist, mu)
		ret.append([mu,sigma])
	return ret

# LPB style
from skimage import feature as f
import numpy as np

nbPoints = 8
radius = 1
METHOD = "default"

def LBPRoiMeanSigma(roi):
	grayRoi = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
	lbp = f.local_binary_pattern(grayRoi, nbPoints, radius, METHOD)
	lbp = lbp.reshape(lbp.shape[0],lbp.shape[1],1)
	lbp = lbp.astype(np.uint8)
	hist = cv.calcHist([lbp], [0], None, [256], [0,256])
	mu = histMean(hist)
	sigma = histDeviation(hist, mu)
	return [mu, sigma]
