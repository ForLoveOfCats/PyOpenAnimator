import pygame
import cairosvg
import io
import constants

def render(file, scale):
	if scale <= 0:
		raise ValueError('''Value "%s" is to low. SVG render scale must be higher than 0.''' % scale)
	return pygame.image.load(io.BytesIO(cairosvg.svg2png(file_obj=open(file, "rb"), dpi=(constants.SVG_BASE_DPI/100)*scale)), "")