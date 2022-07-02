### MODULE JOUEUR

"""
Module joueur : gestion des paramètres caractéristiques d'un joueur dans
le contexte du raycasting (position, orientation) ainsi que des contrôles
associés.
"""
import carte

import tkinter as tk
from math import cos, sin, pi

class Joueur:
	def __init__(self, world:carte.Carte, xpos:int=1, ypos:int=1, angle:float=0):
		self.world = world

		self.xpos = xpos
		self.ypos = ypos
		self.angle = angle

	def avancer(self):
		"""Met a jour la position du joueur."""
		if self.world.isInMap(self.xpos,self.ypos):
			nx = self.xpos + cos(self.angle)
			ny = self.ypos + sin(self.angle)
			if not self.world.collision(nx,ny):
				self.xpos = nx
				self.ypos = ny

	def reculer(self):
		"""Met a jour la position du joueur."""
		if self.world.isInMap(self.xpos,self.ypos):
			nx = self.xpos - cos(self.angle)
			ny = self.ypos - sin(self.angle)
			if not self.world.collision(nx,ny):
				self.xpos = nx
				self.ypos = ny

	def gauche(self):
		"""Met a jour la position du joueur."""
		if self.world.isInMap(self.xpos,self.ypos):
			nx = self.xpos + sin(self.angle)
			ny = self.ypos - cos(self.angle)
			if not self.world.collision(nx,ny):
				self.xpos = nx
				self.ypos = ny

	def droite(self):
		"""Met a jour la position du joueur."""
		if self.world.isInMap(self.xpos,self.ypos):
			nx = self.xpos - sin(self.angle)
			ny = self.ypos + cos(self.angle)
			if not self.world.collision(nx,ny):
				self.xpos = nx
				self.ypos = ny

	def pivoter_gauche(self):
		"""Met a jour l'angle de rotation du joueur."""
		self.angle-= 3/self.world.C_SIZE

	def pivoter_droite(self):
		"""Met a jour l'angle de rotation du joueur."""
		self.angle+= 3/self.world.C_SIZE

if __name__ == "__main__":
	m = carte.Carte()
	j = Joueur(m, 96,96,-pi/2)
	print(j.vitesse, j.xpos, j.ypos, j.angle)
	j.avancer()
	print(j.vitesse, j.xpos, j.ypos, j.angle)
	j.gauche()
	print(j.vitesse, j.xpos, j.ypos, j.angle)
	j.reculer()
	print(j.vitesse, j.xpos, j.ypos, j.angle)
	j.droite()
	print(j.vitesse, j.xpos, j.ypos, j.angle)
