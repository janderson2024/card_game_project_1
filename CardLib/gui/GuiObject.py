import pygame
import CardLib


class GuiObject:
	has_highlight = False
	has_border = False
	border_width = 2;

	def __init__(self, x, y, width, height, obj_draw_method):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

		self.obj_draw_method = obj_draw_method
		

		self.setup_effects()

	def setup_effects(self):
		self.highlight = pygame.Surface((self.width, self.height))
		self.highlight.set_alpha(170)
		self.highlight.fill((255,255,255))

		self.border = pygame.Rect(self.x, self.y, self.width, self.height)

	def move(self, new_x, new_y):
		self.x = new_x
		self.y = new_y
		self.border = pygame.Rect(self.x, self.y, self.width, self.height)

	def resize(self, next_width, next_height):
		self.width = next_width
		self.height = next_height
		self.setup_effects()

	def draw(self):
		self.obj_draw_method()

		if self.has_highlight:
			self.draw_with_highlight()
		if self.has_border:
			self.draw_with_border()

	def draw_with_highlight(self):
		CardLib.gui.draw_img(self.highlight, self.x, self.y)

	def draw_with_border(self):
		CardLib.gui.draw_rect((255,0,0), self.border, 2)
