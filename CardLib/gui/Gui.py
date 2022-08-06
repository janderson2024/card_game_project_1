import pygame

class Gui:
	size = (width, height) = (500, 500)
	background_color = (53, 101, 77)



	def __init__(self):
		self.objects_to_draw = []
		self.pygame_mod = pygame
		print("GUI init")
		

	def get_pygame(self):
		return self.pygame_mod

	def start_gui(self, game_title):
		print("GUI start")
		pygame.init()
		self.screen = pygame.display.set_mode(self.size)
		pygame.display.set_caption(game_title)
		self.redraw()

	def redraw(self):
		self.screen.fill(self.background_color)

		for obj in self.objects_to_draw:
			obj.draw()

		pygame.display.update()

	def add_obj_to_be_drawn(self, obj):
		self.objects_to_draw.append(obj)

	def remove_obj_from_being_drawn(self, obj):
		self.objects_to_draw.remove(obj)

	def create_rect(self, x, y, width, height):
		return pygame.Rect(x, y, width, height)

	def draw_rect(self, color, rect):
		pygame.draw.rect(self.screen, color, rect)
