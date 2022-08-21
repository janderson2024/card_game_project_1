import pygame

class Gui:

	def __init__(self):
		self.objects_to_draw = []
		self.pygame_mod = pygame
		pygame.font.init()
		self.font = pygame.font.SysFont('Comic Sans MS', 30)
		print("GUI init")	

	def get_pygame(self):
		return self.pygame_mod

	def get_screen(self):
		return self.screen

	def start_gui(self, game_title, width=500, height=500, background_color=(0, 132, 64)):
		self.size = (width, height)
		self.background_color = background_color

		print("GUI start")

		pygame.init()
		self.screen = pygame.display.set_mode(self.size)
		pygame.display.set_caption(game_title)

		self.redraw()

	def redraw(self):
		self.screen.fill(self.background_color)

		for obj in self.objects_to_draw:
			obj.gui_obj.draw()

		pygame.display.update()

	def add_obj_to_be_drawn(self, obj):
		self.objects_to_draw.append(obj)
		self.redraw()

	def remove_obj_from_being_drawn(self, obj):
		self.objects_to_draw.remove(obj)
		self.redraw()

	def remove_all_obj(self):
		self.objects_to_draw.clear()
		self.redraw()

	def draw_rect(self, color, rect, width=0):
		pygame.draw.rect(self.screen, color, rect, width)

	def draw_img(self, img, x, y):
		self.screen.blit(img, (x,y))

	def create_label(self, string, text_color, background_color=None):
		return self.font.render(string, True, text_color, background_color)