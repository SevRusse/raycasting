#!/usr/bin/env python3

### MODULE PRINCIPAL

"""
Module principal : boucle de scrutation, gestion des évènements,
mise à jour et rendu.
"""
import tkinter as tk
import camera, carte, image, joueur

class Application(tk.Tk):
	def __init__(self):
		super().__init__()

		self.title("Raycasting")
		controles = [25,38,39,40, 83,85]
		self.etat = dict.fromkeys(controles, False)

		self.carte = carte.Carte()
		self.joueur = joueur.Joueur(self.carte, 192+16,192+32,0)
		self.camera = camera.Camera(self, self.joueur, 60, 20*16,20*10)

		def handler():
			if True in self.etat.values():
				# mise a jour
				if self.etat[25]: # z
					self.joueur.avancer()
				if self.etat[38]: # q
					self.joueur.gauche()
				if self.etat[39]: # s
					self.joueur.reculer()
				if self.etat[40]: # d
					self.joueur.droite()

				if self.etat[83]: # NPAD_4
					self.joueur.pivoter_gauche()
				if self.etat[85]: # NPAD_6
					self.joueur.pivoter_droite()

				self.camera.miseAJour() # redessine la vue
			self.after(1000//60, handler) # FPS ?

		def pression(event=None):
#			print(event.keycode)
			if event.keycode in self.etat and not self.etat[event.keycode]:
				self.etat[event.keycode] = True
			else: # interrupteurs
				if event.keycode == 67: # F1
					self.camera.switchOverlay()
				if event.keycode == 69: # F3
					self.camera.switchInfo()

		def relachement(event=None):
			if event.keycode in self.etat and self.etat[event.keycode]:
				self.etat[event.keycode] = False

		self.bind_all("<Escape>", lambda e: self.destroy())
		self.bind_all("<KeyPress>", pression)
		self.bind_all("<KeyRelease>", relachement)
		handler()

		self.mainloop()

if __name__ == "__main__":
	app = Application()
	exit(0) # liberer les ressources
