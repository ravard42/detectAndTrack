import math as m

fusionDist = 5

def dist(p, x, y):
	return m.sqrt(pow(p.x - x, 2) + pow(p.y - y, 2))

def outOfRange(env, x, y, particle):
	if y < 0 or y >= env[4].shape[0] or x < 0 or x >= env[4].shape[1]:
		if particle is not None:
			env[6].remove(particle)
		return 1
	return 0

def gaussian(x,mu,sigma):
	return 1/(sigma * m.sqrt(2*m.pi))*m.exp(-pow(x-mu,2)/(2*pow(sigma,2)))

def killMulti(part):
	toKill = []
	for i in range(len(part)):
		if toKill.count(i):
			continue
		for j in range(i+1, len(part)):
			if dist(part[i], part[j].x, part[j].y) < fusionDist:
				toKill.append(j)
	for index, value in enumerate(toKill):
		part.remove(part[value - index])
