import pygame_sdl2
pygame_sdl2.import_as_pygame()

import pygame
from pygame.render import *
import random

import inpp
import gui
import svg
import constants


pygame.init()
window = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HIGHT), pygame.RESIZABLE)
renderer = Renderer(None)
renderer.clear((255,255,255))
renderer.render_present()

clock = pygame.time.Clock()
controller = inpp.Controller()
gui.init(window, renderer, controller)

right_panel = gui.Panel([0,25,0,20], (0,255,0))
gui.window_panel.add_child(right_panel)

button_widget = gui.Button([20,20,45,45], 'Tis a Button')
right_panel.add_child(button_widget)

left_panel = gui.Panel([75,0,0,20], (0,0,255))
gui.window_panel.add_child(left_panel)

bottom_panel = gui.Panel([0,0,80,0], (255,0,0))
gui.window_panel.add_child(bottom_panel)

label = gui.Label([10,10,25,25], 'Hello World! I am a Label!')
bottom_panel.add_child(label)

gui.update()
while True:
	controller.tick()
	gui.tick()

	if controller.events.quit() or controller.events.key(pygame.K_ESCAPE):
		break

	for current_event in controller.events.raw():
		if current_event.type == pygame.VIDEORESIZE:
			window = pygame.display.set_mode((current_event.w, current_event.h), pygame.RESIZABLE)
			gui.window_panel.parent_size = (current_event.w, current_event.h)
			gui.window_size = [current_event.w, current_event.h]
			gui.window_panel.update()
			gui.resizing_timer = constants.RESIZING_SECONDS*constants.FPS

	gui.draw()
	renderer.render_present()
	clock.tick(constants.FPS)
