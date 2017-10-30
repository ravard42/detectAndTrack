pas = 8
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
	global pas, coef
	if k == ord('q'):
		return 0
	else:
		#Gestion taille des focus rectangulaires
		#	vert->HistogramMoments et bleu->ParticleTrackers
		if k == ord('9') and (pas == 8 or pas == coef * 8):
				pas = coef * 8 if pas == 8 else 8
		if k == ord('7') and (pas == 8 or pas == 8 / coef):
				pas = 8 / coef if pas == 8 else 8
		if k == ord('6'):
			env[2] += pas
		if k == ord('4') and env[2] > pas:
			env[2] -= pas
		if k == ord('8'):
			env[3] += pas
		if k == ord('2') and env[3] > pas:
			env[3] -= pas
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
