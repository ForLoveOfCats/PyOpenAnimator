'''Pygame's input system sucks. Lets fix that!

PyInput++ is a single file library allows for an easier and more abstract interface to pygame's event module.
It works when you call its update() function *instead* of pygame's pygame.event.get() function.

See example.py for an example usage case.'''

import pygame_sdl2
import pygame


class Controller:
	"""Main class containing all internal data and all functions for external use."""

	class _Events:
		"""Contains all one off events."""
		def __init__(self, controller):
			self.controller = controller


		def key(self, button):
			"""Takes an integer and return a boolean.

			Tests if the supplied integer matches the integer code for any keydown events and returns a boolean accordingly."""
			if not isinstance(button, int):
				raise TypeError('''"%s" is not a valid input. Integer required''' % (button))
			return button in self.controller._triggered


		def mouse(self, button):
			"""Takes a string and returns a boolean.

			Possible inputs are "Left", "Middle", and "Right".
			Tests if the specified mouse button fired a press down event and returns a boolean accordingly."""
			if not isinstance(button, str):
				raise TypeError('''"%s" is not a valid input. String required''' % (button))

			if button not in ['Left', 'Middle', 'Right']:
				raise ValueError('''"%s" is not a valid input. Accepted inputs are: "Left", "Middle", and "Right"''' % (button))

			if button == 'Left' and self.controller._mouse_triggered[0]:
					return True

			if button == 'Middle' and self.controller._mouse_triggered[1]:
					return True

			if button == 'Right' and self.controller._mouse_triggered[2]:
					return True

			return False


		def scroll(self, direction):
			"""Takes a string and returns a boolean.

			Possible inputs are "Up" and "Down".
			Tests if mouse wheel scrolled in specified direction and returns a boolean accordingly."""
			if not isinstance(direction, str):
				raise TypeError('''"%s" is not a valid input. String required''' % (direction))

			if direction not in ['Up', 'Down']:
				raise ValueError('''"%s" is not a valid input. Accepted inputs are: "Up" and "Down"''' % (direction))

			if direction == self.controller._scroll:
				return True

			return False


		def quit(self):
			"""Takes no arguments and returns a boolean.

			Tests if a pygame.QUIT event ever took place and returns a boolean accordingly."""
			return self.controller._quit


		def raw(self):
			"""Takes no arguments and returns a list of pygame events."""
			return self.controller._raw



	class _Repeats:
		"""Contains all events that can span multiple updates."""
		def __init__(self, controller):
			self.controller = controller


		def key(self, button):
			"""Takes an integer and return a boolean.

			Tests if the supplied integer matches the integer code for any keys that are currently depressed and returns a boolean accordingly."""
			if not isinstance(button, int):
				raise TypeError('''"%s" is not a valid input. Integer required''' % (button))
			return button in self.controller._held


		def mouse(self, button):
			"""Takes a string and returns a boolean

			Possible inputs are "Left", "Middle", and "Right"
			Tests if the specified mouse button is currently depressed and returns a boolean accordingly."""
			if button == 'Left' and self.controller._mouse_held[0]:
				return True

			if button == 'Middle' and self.controller._mouse_held[1]:
				return Truee

			if button == 'Right' and self.controller._mouse_held[2]:
				return True




	def __init__(self):
		self._triggered = []  # Keydown events
		self._held = []  # Depressed keys
		self._mouse_triggered = [False, False, False]  # Mouse button press events
		self._mouse_held = [False, False, False]  # Depressed mouse buttons
		self._scroll = None  # Direction of scroll
		self._raw = []  # All pygame events
		self._quit = False  # Did pygame.QUIT fire

		pygame.event.get()  # Clears pygame's event queue

		self.events = self._Events(self)  # Bind Events class to variable for external access
		self.repeats = self._Repeats(self)  # Bind Repeats class to variable for external access



	def tick(self):
		# Reset to blank states
		self._triggered = []
		self._raw = []
		self._scroll = None

		self._raw = pygame.event.get()  # Save all events to _raw and clear the event queue
		for event in self._raw:
			if event.type == pygame.KEYDOWN:
				if event.key != 1073741824:  # pygame_sdl2 has a bug that causes this "key" to be randomly pressed. Unfortunately this key does not exist therefore it throws an error once it reaches the held checking code so it is filtered out here.
					self._triggered.append(event.key)
					self._held.append(event.key)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 4:
					self._scroll = 'Up'
				elif event.button == 5:
					self._scroll = 'Down'
			elif event.type == pygame.QUIT:
				self._quit = True

		temp_held = []
		for current_held in self._held:
			if pygame.key.get_pressed()[current_held] == 1:  # If key is *actually* being pressed currently
				temp_held.append(current_held)  # Add it to temp list
		self._held = temp_held  # Overwrite _held with temp list

		self._mouse_triggered = [pygame.mouse.get_pressed()[button] and not self._mouse_held[button] for button in range(3)]
		self._mouse_held = [bool(pygame.mouse.get_pressed()[0]), bool(pygame.mouse.get_pressed()[1]), bool(pygame.mouse.get_pressed()[2])]
