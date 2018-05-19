import pygame_sdl2
import pygame
import pygame.render

import constants


pygame.init()
window = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HIGHT), pygame.RESIZABLE)
renderer = pygame.render.Renderer(None)
renderer.clear((255,255,255))
renderer.render_present()  # Draw something ASAP


class blit(pygame.render.Sprite):  # Allows for drawing render textures in a similar way to surfaces
	def __init__(self, img_tex, position):
		pygame.render.Sprite.__init__(self, img_tex)
		self.render(position)


def convert_surface(surface):  # Because typing rendering.renderer.load_texture() is annoying
	return renderer.load_texture(surface)


def present():  # Because typing rendering.renderer.render_present() is annoying
	renderer.render_present()
