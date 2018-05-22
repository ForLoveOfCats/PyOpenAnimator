import pygame
import cairosvg
import io

import constants


class SVG(pygame.Surface):
	def __init__(self, file, scale_arg):
		self.file_path = file  # Set path to file for loading
		self.reload_file()  # Inital file load
		self.scale(scale_arg)  # Set scale and inital render

	def reload_file(self):  # Reload file from path
		self.file = open(self.file_path, "rb")

	def render(self):
		image = pygame.image.load(io.BytesIO(cairosvg.svg2png(file_obj=self.file, dpi=(constants.SVG_BASE_DPI/100)*self.render_scale)), "")  # Parse and render SVG
		pygame.Surface.__init__(self, image.get_size(), pygame.SRCALPHA, 32)  # Convert rendered image to surface
		self.blit(image, (0,0))  # Blit to self for external use

	def scale(self, scale_arg):
		if scale_arg <= 0:  # Throw error if scale is invalid
			raise ValueError('''Value "%s" is to low. SVG render scale must be higher than 0.''' % scale)
		self.render_scale = scale_arg  # Set scale
		self.render()  # Rerender SVG to surface
