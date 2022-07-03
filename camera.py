### MODULE CAMERA

"""
Module caméra : projection et rendu de tous les objets à l'écran (sol,
plafond, murs i.e. colonne par colonne, et sprites).
"""
import tkinter as tk
from math import pi,tan

import carte, joueur

class Camera(tk.Canvas):
	overlay_state = True
	info_state = False
	def __init__(self, master, joueur:joueur.Joueur, fov:int=60, width:int=320,height:int=200):
		super().__init__(master, width=width, height=height)
		self.grid()
		self.joueur = joueur
		self.world = joueur.world
		self.fov = fov
		self.width = width
		self.height = height

		self.renderCeiling()
		self.renderGround()
		self.createOverlay() # overlay_state = True
		self.miseAJour()

	def renderCeiling(self):
		objs = []
		for teinte in range(16):
			coul = hex(int(teinte/2))[2:]
			objs+= [self.create_rectangle(
							0,(self.height/2)-(self.height/2)*(teinte/16),
							self.width,(self.height/2)-(self.height/2)*((teinte+1)/16),
							fill='#'
							+'0'*(1-len(coul))+coul
							+'0'*1
							+'0'*1
							,outline='')]
		return objs

	def renderGround(self):
		objs = []
		for teinte in range(16):
			coul = hex(int(teinte/2))[2:]
			objs+= [self.create_rectangle(
							0,(self.height/2)+(self.height/2)*(teinte/16),
							self.width,(self.height/2)+(self.height/2)*((teinte+1)/16),
							fill='#'
							+'0'*(1-len(coul))+coul
							+'0'*1
							+'0'*1
							,outline='')]
		return objs

	def renderWall(self):
		objs = []
		rays = self.world.raycasting(self.joueur.xpos,self.joueur.ypos,self.joueur.angle, self.fov, self.width)
		delta = (self.width/2)/tan((self.fov/2)*(pi/180))
		for x in range(self.width):
			x_inter,y_inter,ang = rays[x]
			dist = (carte.distance(self.joueur.xpos,self.joueur.ypos, x_inter,y_inter) if (carte.distance(self.joueur.xpos,self.joueur.ypos, x_inter,y_inter) <= self.world.MAX_DIST) else self.world.MAX_DIST)
			hmur = (20*(delta/dist))

			# bordure et hors-champ
			if ((int(x_inter)%self.world.C_SIZE in [0, self.world.C_SIZE-1]) and (int(y_inter)%self.world.C_SIZE in [0, self.world.C_SIZE-1])):
				intensite = 0
			else:
				intensite = 15-int(15*(dist/self.world.MAX_DIST))
			coul = '#'+('0'*(1-len(hex(intensite)[2:]))+hex(intensite)[2:])*3
			objs+= [self.create_line(
							x,self.height/2-hmur/2,
							x,self.height/2+hmur/2,
							fill=coul)]
		return objs

	def renderSprite(self):
	##### TODO
		objs = []
		return objs

	def miseAJour(self):
		self.delete('render')
		Lobjs = self.renderWall() + self.renderSprite()
		for obj in Lobjs:
			self.addtag_above('render', obj)
		# overlay = last update !
		self.tag_lower('render', 'overlay')
		if self.overlay_state:
			if self.info_state:
				self.renderInfo()
		return Lobjs

	def renderInfo(self):
		# situation / carte (option de debug)
		t = self.find_withtag('info')
		ch = f"x: {round(self.joueur.xpos, 5)}\n"
		ch+= f"y: {round(self.joueur.ypos, 5)}\n"
		ch+= f"a: {round(((-self.joueur.angle+pi)%(2*pi)-pi)*(180/pi), 5)}°\n"
		self.itemconfigure(t, text=ch)

	def createInfo(self):
		# situation / carte
		obj = self.create_text(5,5,anchor="nw", fill="green", font=('Courier',12,'bold'), justify="left", tags='info')
		self.addtag_withtag('overlay', obj)
		self.renderInfo()

	def switchInfo(self):
		"""Able or disable the overlay (info only)."""
		self.info_state = not self.info_state
		if self.overlay_state:
			if self.info_state:
				self.createInfo()
			else:
				self.delete('info')

	def createOverlay(self):
		# curseur de visee
		obj = self.create_line(self.width/2-10,self.height/2,self.width/2+10,self.height/2, fill='white')
		self.addtag_withtag('overlay', obj)
		obj = self.create_line(self.width/2,self.height/2-10,self.width/2,self.height/2+10, fill='white')
		self.addtag_withtag('overlay', obj)

	def switchOverlay(self):
		"""Able or disable the overlay (info only)."""
		self.overlay_state = not self.overlay_state
		if self.overlay_state:
			self.createOverlay()
			if self.info_state:
				self.createInfo()
		else:
			self.delete('overlay')

if __name__ == "__main__":
	world = carte.Carte()
	app = tk.Tk()
	j = joueur.Joueur(world, 192+16, 192+32, 0)
	cam = Camera(app, j, 60, 35*16,35*10)

	# situation en vue de dessus
	minimap = tk.Canvas(app, width=cam.height, height=cam.height)
	minimap.grid(row=0, column=1)
	# FOV joueur
	rays = world.raycasting(j.xpos,j.ypos,j.angle, cam.fov, cam.width)
	for i in range(cam.width):
		x_inter,y_inter,ang = rays[i]
		minimap.create_line(
			cam.height*(j.xpos/(len(world.plan[0])*world.C_SIZE)),cam.height*(j.ypos/(len(world.plan)*world.C_SIZE)),
			cam.height*(x_inter/(len(world.plan[0])*world.C_SIZE)),cam.height*(y_inter/(len(world.plan)*world.C_SIZE)),
			fill='yellow')
	# mini-carte
	for y in range(len(world.plan)):
		for x in range(len(world.plan[y])):
			if world.plan[y][x] == -1:
				color = 'grey'
			else:
				color = ''
			minimap.create_rectangle(
				cam.height*(x/len(world.plan[y])),cam.height*(y/len(world.plan)),
				cam.height*((x+1)/len(world.plan[y])),cam.height*((y+1)/len(world.plan)),
				fill=color)
	# affichage du joueur
	minimap.create_oval(
		cam.height*((j.xpos-10)/(len(world.plan[0])*world.C_SIZE)),cam.height*((j.ypos-10)/(len(world.plan)*world.C_SIZE)),
		cam.height*((j.xpos+10)/(len(world.plan[0])*world.C_SIZE)),cam.height*((j.ypos+10)/(len(world.plan)*world.C_SIZE)),
		fill='red')

	app.mainloop()

	exit(0)
