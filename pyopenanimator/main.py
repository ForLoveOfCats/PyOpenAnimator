import pygame_sdl2
pygame_sdl2.import_as_pygame()

import pygame
from pygame.render import *
import random

import inpp
import scaleui
import svg
import constants


pygame.init()
window = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HIGHT), pygame.RESIZABLE)
renderer = Renderer(None)
renderer.clear((255,255,255))
renderer.render_present()

clock = pygame.time.Clock()
controller = inpp.Controller()
scaleui.init(window, renderer, controller)

right_panel = scaleui.Panel([0,25,0,20], (0,255,0))
scaleui.window_panel.add_child(right_panel)

button_widget = scaleui.Button([20,20,45,45], 'Tis a Button')
right_panel.add_child(button_widget)

left_panel = scaleui.Panel([75,0,0,20], (0,0,255))
scaleui.window_panel.add_child(left_panel)

bottom_panel = scaleui.Panel([0,0,80,0], (255,0,0))
scaleui.window_panel.add_child(bottom_panel)

label = scaleui.Label([10,10,25,25], 'Hello World! I am a Label!')
bottom_panel.add_child(label)

scaleui.update()
while True:
	controller.tick()
	scaleui.tick()

	if controller.events.quit() or controller.events.key(pygame.K_ESCAPE):
		break

	for current_event in controller.events.raw():
		if current_event.type == pygame.VIDEORESIZE:
			window_width, window_height = current_event.w, current_event.h
			if window_width < constants.MINIMUM_WINDOW_SIZE:
				window_width = constants.MINIMUM_WINDOW_SIZE
			if window_height < constants.MINIMUM_WINDOW_SIZE:
				window_height = constants.MINIMUM_WINDOW_SIZE

			window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
			scaleui.window_panel.parent_size = (window_width, window_height)
			scaleui.window_size = [window_width, window_height]
			scaleui.window_panel.update()
			scaleui.resizing_timer = constants.RESIZING_SECONDS*constants.FPS

	scaleui.draw()
	renderer.render_present()
	clock.tick(constants.FPS)
