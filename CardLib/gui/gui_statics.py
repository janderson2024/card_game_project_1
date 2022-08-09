import pygame

def create_rect(x, y, width, height):
	return pygame.Rect(x, y, width, height)

def create_img(img, x, y, width=-1, height=-1):
	image = pygame.image.load(img)

	if(width != -1 or height != -1):
		image = pygame.transform.scale(image, (width, height))

	return image