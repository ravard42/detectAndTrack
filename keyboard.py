step = 8
saveStep = step
coef = 4

def printEnvInfos(env):
	print "(x,y) = ({},{})".format(env[0], env[1])
	print "(w/2,h/2) = ({},{})".format(env[2], env[3])
	nbPix = (env[2] * 2 - 1)*(env[3] * 2 - 1)
	print "nbPixel in hist : {}".format(nbPix)
	if env[5]:
		print "<----ENV5----->\nHistogram moments"
		for i in range(3):
			print "	CANAL {}".format(i)
			print "		----> mu = {}".format(env[5][0][i][0])
			print "		----> sigma = {}".format(env[5][0][i][1])
		print "	LBP"
		print "	   	----> mu = {}".format(env[5][1][0])
		print "	   	----> sigma = {}".format(env[5][1][1])
		
	if len(env[6]) > 0:
			print "<----ENV6----->\nparticle trackers"
			print "nombre de trackers en action : {}".format(len(env[6]))

def loop(k, env):
	global step, coef
	if k == ord('q'):
		return 0
	else:
		#Gestion taille des focus rectangulaires
		#	vert->HistogramMoments et bleu->ParticleTrackers
		if k == ord('9'):
				step = saveStep * coef
		if k == ord('7'):
				step = saveStep / coef
		if k == ord('0'):
				step = saveStep
		if k == ord('6'):
			env[2] += step
		if k == ord('4') and env[2] > step:
			env[2] -= step
		if k == ord('8'):
			env[3] += step
		if k == ord('2') and env[3] > step:
			env[3] -= step
		#Print infos env
		if k == ord('i'):
			printEnvInfos(env)
		#Reset histogramMoments
		if k == ord('h'):
			env[5] = []
		#Destruction de tous les trackers
		if k == ord('p'):
			env[6] = []
		#Lecture/Pause
		if k == ord(' '):
			env[7] = 1 if env[7] == 0 else 0
		return 1
