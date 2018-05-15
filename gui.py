import pygame_sdl2
import pygame
from pygame.render import *
import inpp
import constants


activatable_widgets = []
resizing_timer = 0


class blit(pygame.render.Sprite):
	def __init__(self, img_tex, position):
		if isinstance(img_tex, pygame_sdl2.surface.Surface):
			img_tex = renderer.load_texture(img_tex)
		pygame.render.Sprite.__init__(self, img_tex)
		self.render(position)


def return_font_size(text, space):
	space = [space[0]*0.95, space[1]*0.95]
	size = base_font.size(text)
	overflow = [space[0]-size[0], space[1]-size[1]]

	x_size = int((constants.BASE_FONT_SIZE/size[0])*space[0])
	y_size = int((constants.BASE_FONT_SIZE/size[1])*space[1])

	if x_size < y_size:
		return x_size
	else:
		return y_size


def return_outline_size():
	return ((sum(window_size)/2)/100)*constants.BUTTON_OUTLINE_THICKNESS


def init(window_surface, renderer_arg, controller_arg):
	global window, window_size, window_panel, renderer, controller, font_name, base_font
	window = window_surface
	window_size = window.get_size()
	renderer = renderer_arg
	window_panel = Root([0,0,0,0])
	window_panel.parent_size = window.get_size()
	controller = controller_arg

	font_name = pygame.font.get_default_font()
	base_font = pygame.font.SysFont(font_name, constants.BASE_FONT_SIZE)


def draw():
	window_panel.draw()


def update():
	window_panel.update()


def tick():
	global resizing_timer

	if resizing_timer > 0:
		resizing_timer -= 1

	else:
		mouse_pos = pygame.mouse.get_pos()

		for current_widget in activatable_widgets:
			widget_pos = [current_widget.return_offset()[0]+current_widget.parent_pos[0], current_widget.return_offset()[1]+current_widget.parent_pos[1]]
			widget_size = current_widget.return_size()
			overlap_x, overlap_y = False, False

			if mouse_pos[0] >= widget_pos[0] and mouse_pos[0] <= widget_pos[0]+widget_size[0]:
				overlap_x = True
			if mouse_pos[1] >= widget_pos[1] and mouse_pos[1] <= widget_pos[1]+widget_size[1]:
				overlap_y = True

			if overlap_x and overlap_y:
				if not current_widget.is_mouse_over:
					if constants.DEBUG:
						print ('Mouse Over')
					current_widget.is_mouse_over = True
					current_widget.call_callbacks('mouse_over')  # Mouse Over
					if current_widget.is_mouse_down:
						current_widget.mouse_down()
					else:
						current_widget.mouse_over()

				if controller.events.mouse("Left"):
					if constants.DEBUG:
						print ('Mouse Down')
					current_widget.is_mouse_down = True
					current_widget.call_callbacks('mouse_over')  # Mouse Down
					current_widget.mouse_down()

				if not controller.repeats.mouse("Left") and current_widget.is_mouse_down:
					if constants.DEBUG:
						print ('Mouse Up')
					current_widget.is_mouse_down = False
					current_widget.call_callbacks('mouse_up')  # Mouse Up
					current_widget.mouse_up()

			elif current_widget.is_mouse_over:
				if constants.DEBUG:
					print ('Mouse Off')
				current_widget.is_mouse_over = False
				current_widget.call_callbacks('mouse_off')  # Mouse Off
				current_widget.mouse_off()

			if controller.repeats.mouse("Left"):
				if constants.DEBUG:
					print ('Mouse Held')
				current_widget.call_callbacks('mouse_held')  # Mouse Held
				current_widget.mouse_held()
			else:
				current_widget.is_mouse_down = False




class _BaseWidget:
	def __init__(self, anchors):
		self.children = []  # All child widgets and panels
		self.anchors = anchors  # List of 4 ints
		self.parent_size = [1,1]
		self.parent_offset = [0,0]
		self.parent_pos = [0,0]
		self.texture = renderer.load_texture(pygame.Surface([1,1]))
		self.parent = None
		self.callbacks = {}
		self.call_arguments = {}
		self.is_mouse_over = False
		self.is_mouse_down = False

	def add_child(self, child):
		child.parent = self
		self.children.append(child)  # Not actually saving child to the list, just a pointer to the object
		self.update_children()

	def set_anchors(self, anchors):
		self.anchors = anchors
		self.render()

	def return_size(self):
		return [round((100-(self.anchors[0]+self.anchors[1]))*(self.parent_size[0]/100)), round((100-(self.anchors[2]+self.anchors[3]))*(self.parent_size[1]/100))]

	def return_pos(self):
		return [self.parent_pos[0]+self.return_offset()[0], self.parent_pos[1]+self.return_offset()[1]]

	def return_offset(self):
		return [round((self.parent_size[0]/100)*self.anchors[0]), round((self.parent_size[1]/100)*self.anchors[2])]

	def update_children(self):
		for current_child in self.children:
			current_child.parent_size = self.return_size()
			current_child.parent_offset = self.return_offset()
			current_child.parent_pos = self.return_pos()
			current_child.update()

	def update(self):
		self.is_mouse_over = False
		self.render()
		self.update_children()

	def draw(self):
		blit(self.texture, self.return_pos())

		for current_child in self.children:
			current_child.draw()

	def set_callback(self, call, function, arguments=[]):
		self.callbacks[call] = function
		self.call_arguments[call] = arguments

	def get_callbacks(self, call):
		try:
			return self.callbacks[call]
		except:
			return None

	def get_call_args(self, call):
		try:
			return self.call_arguments[call]
		except:
			return []

	def call_callbacks(self, call):
		try:
			self.get_callbacks(call)(*self.get_call_args(call))
		except:
			pass

	def render(self):
		pass

	def mouse_over(self):
		pass

	def mouse_off(self):
		pass

	def mouse_down(self):
		pass

	def mouse_up(self):
		pass

	def mouse_held(self):
		pass



class _TextRendering():
	def __init__(self, text):
		self.text = text
		self.font_size = constants.BASE_FONT_SIZE
		self.size_at_text_render = [1,1]
		self.font_obj = pygame.font.SysFont(font_name, self.font_size)

	def set_text(self, text):
		if text != self.text:
			self.text = text
			self.render()

	def render_text(self, draw_surface):
		if draw_surface.get_size() != self.size_at_text_render:
			self.size_at_text_render = draw_surface.get_size()
			font_size = return_font_size(self.text, self.return_size())
		else: font_size = self.font_size

		if font_size != self.font_size:
			self.font_size = font_size
			self.font_obj = pygame.font.SysFont(font_name, self.font_size)
		font_surf = self.font_obj.render(self.text, True, constants.GLOBAL_FONT_COLOR)
		draw_surface.blit(font_surf, [(self.return_size()[0]/2)-(font_surf.get_width()/2), (self.return_size()[1]/2)-(font_surf.get_height()/2)+(return_outline_size()/2)])  # Don't question it



class Root(_BaseWidget):
	def __init__(self, anchors):
		_BaseWidget.__init__(self, anchors)

	def draw(self):
		renderer.clear(constants.BACKGROUND)

		for current_child in self.children:
			current_child.draw()



class Panel(_BaseWidget):
	def __init__(self, anchors, color):
		_BaseWidget.__init__(self, anchors)
		self.color = color

	def render(self):
		draw_surface = pygame.Surface(self.return_size())
		pygame.draw.rect(draw_surface, self.color, [0,0]+self.return_size())
		self.texture = renderer.load_texture(draw_surface)



class Label(_BaseWidget, _TextRendering):
	def __init__(self, anchors, text):
		_BaseWidget.__init__(self, anchors)
		_TextRendering.__init__(self, text)

	def render(self):
		draw_surface = pygame.Surface(self.return_size())
		draw_surface.fill(constants.LABEL_BACKGROUND_COLOR)
		self.render_text(draw_surface)
		self.texture = renderer.load_texture(draw_surface)



class Button(_BaseWidget, _TextRendering):
	def __init__(self, anchors, text):
		global activatable_widgets
		activatable_widgets.append(self)
		_BaseWidget.__init__(self, anchors)
		_TextRendering.__init__(self, text)

	def draw_outline(self, draw_surface):  # Draw with lines because draw.line is less weird than draw.rect
		# This function sucks
		pygame.draw.line(draw_surface, constants.BUTTON_OUTLINE_COLOR, (0,return_outline_size()/2), (self.return_size()[0], return_outline_size()/2), return_outline_size())  # Top
		pygame.draw.line(draw_surface, constants.BUTTON_OUTLINE_COLOR, (0,self.return_size()[1]-return_outline_size()/2), (self.return_size()[0], self.return_size()[1]-return_outline_size()/2), return_outline_size())  # Bottom
		pygame.draw.line(draw_surface, constants.BUTTON_OUTLINE_COLOR, (return_outline_size()/2,0), (return_outline_size()/2,self.return_size()[0]), return_outline_size())  # Right
		pygame.draw.line(draw_surface, constants.BUTTON_OUTLINE_COLOR, (self.return_size()[0]-return_outline_size()/2,0), (self.return_size()[0]-return_outline_size()/2,self.return_size()[0]), return_outline_size())  # Left

	def render(self):
		draw_surface = pygame.Surface(self.return_size())
		draw_surface.fill(constants.BUTTON_BASE_COLOR)
		self.draw_outline(draw_surface)
		self.render_text(draw_surface)
		self.texture = renderer.load_texture(draw_surface)

	def mouse_over(self):
		draw_surface = pygame.Surface(self.return_size())
		draw_surface.fill(constants.BUTTON_HOVER_COLOR)
		self.draw_outline(draw_surface)
		self.render_text(draw_surface)
		self.texture = renderer.load_texture(draw_surface)

	def mouse_down(self):
		draw_surface = pygame.Surface(self.return_size())
		draw_surface.fill(constants.BUTTON_PRESS_COLOR)
		self.draw_outline(draw_surface)
		self.render_text(draw_surface)
		self.texture = renderer.load_texture(draw_surface)

	def mouse_up(self):
		if self.is_mouse_over:
			self.mouse_over()
		else:
			self.mouse_off()


	def mouse_off(self):
		self.render()
