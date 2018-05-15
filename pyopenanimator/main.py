import pygame_sdl2
pygame_sdl2.import_as_pygame()

import pygame
from pygame.render import *
import random

import constants
import inpp
import svg
import scaleui
import interface


pygame.init()
window = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HIGHT), pygame.RESIZABLE)
renderer = Renderer(None)
renderer.clear((255,255,255))
renderer.render_present()

clock = pygame.time.Clock()
controller = inpp.Controller()
scaleui.init(window, renderer, controller)
interface.init(renderer,controller)

while True:
	controller.tick()
	interface.tick()

	if controller.events.quit() or controller.events.key(pygame.K_ESCAPE):
		break

	clock.tick(constants.FPS)
