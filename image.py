### MODULE IMAGE

"""
Module image : permet de charger et de récupérer les informations
associées à un fichier image (dimensions, code RVB d'un pixel, etc.).
"""
class Image:
	def __init__(self, path):
		self.im = open(path, 'r')

	def path(self):
		return self.im.filename

	def format(self):
		"""Retourne le format du fichier image."""
		return self.im.format

	def dimensions(self):
		"""Retourne les dimensions de l'image sous la forme d'un tuple (largeur, hauteur)"""
		return self.im.size

	def largeur(self):
		"""Retourne la largeur en pixels de l'image"""
		return self.im.width

	def hauteur(self):
		"""Retourne la hauteur en pixels de l'image"""
		return self.im.height

	def couleurs(self):
		return self.im.getdata()

	def RVB(self, px):
		"""Retourne le code RGB du pixel px (x, y)."""
		if self.im.mode == "RGB":
			return self.im.getpixel(px)
		return None

	def afficher(self):
		"""Affiche l'image a l'ecran."""
		self.im.show()

if __name__ == "__main__":
	pass