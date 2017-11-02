Petite explication du fonctionnement et de l'architecture du programme.

<------------------------------>

main.py
		->	A-playerSubtractDetector:	off
		->	B-LBPFrame:						off
		->	C-particleFilter:				on
	NB	: le script est dans cet etat par default pour une meilleure prise en main... ahaha ^^

	voir le script et ses #comms pour plus de details 

<------------------------------>

keyboard.py
	gere les appels clavier
		1) taille de la fenetre de focus:
			(step=8, coef=4) par default
				touches	|	action
				------------------
					4		|	-step horizontally
					6		|	+step horizontally
					2		|	-step vertically
					8		|	+step vertically
					7		|	apply tinyStep (step /= coef)
					9		|	apply bigStep	(step *= coef)
					0		|	apply defaultStep (retour a la valeur de depart)
		2) autres:
				touches	|	action
				------------------
				 espace	|	lecture on/off
				 	h		|	clear env[5]
				 	p		|	clear env[6]
				 	i		|	print info env
				 	q		|	exit


<------------------------------>

mouse.py
	gere les appels souris
		1)click gauche(focus vert):
			selection des histogrammes R,G,B (et LBP si actif) 
			a partir desquels on calculera les moments (moyenne et ecartype)
			-> cf histo.py
		2)click droit(focus bleu):
			envoi des particleTrackers
			-> cf particleClass.py


<------------------------------>

histo.py
	calcule les moments a partir des histogrammes selectionnes
		1) BGRRoiMeanSigma 
				renvoie les moyennes et ecarts types respectifs des canaux B G et R 
				de la RegionOfImage (ROI) selectionnee
		2) LBPRoiMeanSigma
				renvoie la moyenne et l'ecart du LBP
				de la ROI selectionnee

<------------------------------>

particleClass.py
	patron de classe des particleTrackers
	trois etapes fondamentales dans l'elaboration d'un particleFilter
		
		1) modeliser le mouvement des particules
				
				principe				: denseOpticalFlow
				methode de class 	: moveP
		
		2) donner un poids probabiliste a chacune des particules du tracker 
				fonction des mesures respectives des particules
					B, G, R (et LBP si actif)
				et des moments retenus pour le tracking
					(self.BGRHMs et self.LBPHMs si actif) 
				
				note : LBP mal gerE donc desactivE
				
				principe				: central limit theorem ? 
				methode de classe : gaussianWeight
		
		3) redistribuer les particlues en fonction de leur poids 
				
				principe 			: cf https://salzis.wordpress.com/2015/05/25/particle-filters-with-python/
				methode de classe : resample
		
		parametres:
			1) particules par tracker (default nbPart=50)
			2) constante de dispersion gaussienne dans moveP (default stdMove = 2.3)
			3) seqFrame et maxDisp dans calcParticleDispersion (default 20 et 140)


<------------------------------>

detector.py
	detecte le mouvement par soustraction de frame et tente une automatisation de l'envoi des trackers

		parametres:
			1) minArea, representant l'amplitude que le mouvement doit avoir pour etre retenu (default 25)
			2) toutes les options du createBackgroundSubtractorMOG (default (3,0.1,3,7))
			3) l'amplitude du gaussianBlur, du threshold et du dilate ((15,15), 42, 2)
			4) minDist requise avec les trackers avoisinant pour en creer un nouveau (default 20) 
				fusionDist dans utils.py definissant la distance max de fusion des trackers (default 5)
