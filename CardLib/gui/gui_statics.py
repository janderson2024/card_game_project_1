import pygame

def create_rect(x, y, width, height):
	return pygame.Rect(x, y, width, height)

def draw_rect(screen, color, rect):
	pygame.draw.rect(screen, color, rect)