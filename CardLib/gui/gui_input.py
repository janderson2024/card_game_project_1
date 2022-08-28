import pygame
import CardLib

def coords_in_obj(x, y, obj):
	gui_obj = obj.gui_obj

	xres = (x >= gui_obj.x and x <= gui_obj.width+gui_obj.x)
	yres = (y >= gui_obj.y and y <= gui_obj.height+gui_obj.y)
	return xres and yres


def get_gui_user_input(possible_inputs):
	hovered_obj = None
	got_input = False

	pygame.event.clear()
	while not got_input:
		hovered_obj = None
		(mx,my) = pygame.mouse.get_pos()

		for obj in possible_inputs:
			obj.gui_obj.has_border = True
			obj.gui_obj.has_highlight = False
			

			if coords_in_obj(mx, my, obj):
				obj.gui_obj.has_highlight = True
				hovered_obj = obj

		CardLib.gui.redraw()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				#print(event.pos) useful for testing positions
				if hovered_obj is not None:
					hovered_obj.gui_obj.has_highlight = False
					for obj in possible_inputs:
						obj.gui_obj.has_border = False
					got_input = True	
					return hovered_obj