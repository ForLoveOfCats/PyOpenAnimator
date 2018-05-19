import pygame_sdl2
pygame_sdl2.import_as_pygame()

import pygame
import random

import constants
import inpp
import rendering
import svg
import scaleui
import interface


clock = pygame.time.Clock()
controller = inpp.Controller()
scaleui.init(controller)
interface.init(controller)

while True:
	controller.tick()
	interface.tick()

	if controller.events.quit() or controller.events.key(pygame.K_ESCAPE):
		break

	clock.tick(constants.FPS)
