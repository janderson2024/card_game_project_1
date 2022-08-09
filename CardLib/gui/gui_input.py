import pygame


def get_gui_user_input():
	got_input = False
	while not got_input:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				print(event.pos)
				got_input = True
				return event.pos
				## NOT FINAL. just for testing