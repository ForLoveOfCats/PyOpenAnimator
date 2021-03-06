import pygame

import constants
import rendering
import svg
import scaleui


def init(controller_arg):
	global controller
	controller = controller_arg

	left_panel = scaleui.Canvas([0,25,0,20], (500,500), (50,50))
	scaleui.window_panel.add_child(left_panel)

	right_panel = scaleui.Panel([75,0,0,20], (0,0,255))
	scaleui.window_panel.add_child(right_panel)

	button_widget = scaleui.Button([20,20,45,45], 'Tis a Button')
	right_panel.add_child(button_widget)

	bottom_panel = scaleui.Panel([0,0,80,0], (255,0,0))
	scaleui.window_panel.add_child(bottom_panel)

	label = scaleui.Label([10,10,25,25], 'Hello World! I am a Label!')
	bottom_panel.add_child(label)

	# Drawing an SVG on the left_panel canvas
	smiley_svg = svg.SVG('example.svg', 100)
	left_panel.surface.blit(smiley_svg, (0,0))
	left_panel.render()


def tick():
	scaleui.tick()

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
	rendering.present()
