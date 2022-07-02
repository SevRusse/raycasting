### MODULE CARTE

"""
Module carte : génération d'une map, gestion de lancer de rayons,
détection de collisions.
"""
from math import pi, tan, sqrt, cos, sin

class Carte:
	"""Une carte est representee par une matrice carree 2D.
	Chaque cellule est representee par un nombre qui determine ce qu'elle
	contient.

	-1 : mur
	0 : sol"""
	C_SIZE = 64
	MAX_DIST = 256
	def __init__(self, path:str = 'sample_map0.txt'):
		self.plan = self.lire_carte(path)

	def lire_carte(self, path:str = 'sample_map0.txt'):
		M = []
		src = open(path, 'r')
		for ligne in src:
			M+= [[int(el) for el in ligne.split()]]
		return M

	def afficher(self):
		for ligne in self.plan:
			print(ligne)

	def isInMap(self, x,y):
		return (0<= x <=len(self.plan[0])*self.C_SIZE-1) and (0<= y <=len(self.plan)*self.C_SIZE-1)

	def nextVerticalBorder(self, x,y, ang):
		ang = (ang+pi)%(2*pi)-pi # normalisation [-pi, pi[
		tang = ang%pi
		if (-pi/2< ang <0) or (pi/2< ang <pi):
			tang = pi-tang
		if (-pi< ang <0):
			tang*= -1
		xv = ((len(self.plan[0])*self.C_SIZE-1) if (-pi/2< ang <pi/2) else 0)
		yv = y + abs(x-xv)*tan(tang)
		return (xv,yv)

	def nextHorizontalBorder(self, x,y, ang):
		ang = (ang+pi)%(2*pi)-pi # normalisation [-pi, pi[
		tang = (ang-(pi/2))%pi
		if (-pi< ang <-pi/2) or (0< ang <pi/2):
			tang = pi-tang
		if (-pi< ang <-pi/2) or (pi/2< ang <pi):
			tang*= -1
		yh = ((len(self.plan)*self.C_SIZE-1) if (0< ang <pi) else 0)
		xh = x + abs(y-yh)*tan(tang)
		return (xh,yh)

	def findBorder(self, x,y, ang):
		ang = (ang+pi)%(2*pi)-pi # normalisation [-pi, pi[
		if ang not in [-pi, 0]:
			xh,yh = self.nextHorizontalBorder(x,y, ang)
		if ang not in [-pi/2, pi/2]:
			xv,yv = self.nextVerticalBorder(x,y, ang)
			if ang in [-pi, 0]:
				return (xv,yv)
		else:
			return (xh,yh)

		# ici, les deux points coexistent mais un seul est dans les
		# limites de la carte (sauf si confondus dans un coin)
		return ((xv,yv) if self.isInMap(xv,yv) else (xh,yh))

	def collision(self, x,y):
		return self.isInMap(x,y) and self.plan[int(y//self.C_SIZE)][int(x//self.C_SIZE)] == -1

	def genererRayonVuePixel(self, x1,y1, ang):
		x2,y2 = self.findBorder(x1,y1, ang)
		dx = (x2-x1)
		dy = (y2-y1)
		step = int(max(abs(dx), abs(dy)))
		dx/= step
		dy/= step
		x = x1
		y = y1
		for i in range(step):
			if self.collision(x,y):
				break
			x+= dx
			y+= dy
		return x,y

	def raycasting(self, xcam,ycam, ocam, camfov, wcam):
		L = []
		for x in range(wcam):
			# calcul de l'angle du rayon de vue en x
			# normalisation [-pi, pi[
			ang = ocam+(x/(wcam/2)-1)*((camfov/2)*(pi/180))
			x1,y1 = self.genererRayonVuePixel(xcam,ycam, ang)
			L+= [(x1,y1,ang)]
		return L

def sq(x):
	return x*x

def distance(x1,y1, x2,y2):
	return sqrt(sq(x2-x1)+sq(y2-y1))

if __name__ == "__main__":
	c = Carte()
	c.afficher()
	jx,jy,o = 192,192,0
	fov = 60
	Lr = c.raycasting(jx,jy,o, fov,320)
	for pt_inter in Lr:
		print(pt_inter)
