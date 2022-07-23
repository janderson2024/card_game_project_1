import sys
import pygame
from CardLib.Card import Card as Card

pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 600, 403

white = (255, 255, 255)
green = (53, 101, 77)
black = (0, 0, 0)
grey = (211, 211, 211)
new_card = '1,2'
card1 = Card(1, 2)

screen = pygame.display.set_mode((width, height))
icon = pygame.image.load('troll_icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Card Tester')

font = pygame.font.SysFont('Arial', 20)


card_image = pygame.image.load(f'CardLib/card_images/standard/{card1.image}')
DEFAULT_IMAGE_SIZE = (250, 363)
card_image = pygame.transform.scale(card_image, DEFAULT_IMAGE_SIZE)

objects = []
active = False


class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        objects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


def flip_card():
    global card_image, rank, suit, suit_text, color, image_display, displayable, str_display
    card1.set_display()
    card_image = pygame.image.load(f'CardLib/card_images/standard/{card1.image}')
    DEFAULT_IMAGE_SIZE = (250, 363)
    card_image = pygame.transform.scale(card_image, DEFAULT_IMAGE_SIZE)
    rank = font.render(f"Card Rank: {card1.rank}", True, white)
    suit = font.render(f"Card Suit: {card1.suit}", True, white)
    suit_text = font.render(f"Suit Text: {card1.suit_text}", True, white)
    color = font.render(f"Color: {card1.color}", True, white)
    image_display = font.render(f"Image Displayed: {card1.image}", True, white)
    displayable = font.render(f"Displayable: {card1.displayable}", True, white)
    str_display = font.render(f"__str__: {card1.__str__()}", True, white)


def change_card():
    global card1, card_image, rank, suit, suit_text, color, image_display, displayable, str_display, new_card
    del card1
    card_split = str(new_card).split(",")
    new_suit, new_rank = card_split[0], card_split[1]
    card1 = Card(new_suit, new_rank)
    card_image = pygame.image.load(f'CardLib/card_images/standard/{card1.image}')
    DEFAULT_IMAGE_SIZE = (250, 363)
    card_image = pygame.transform.scale(card_image, DEFAULT_IMAGE_SIZE)
    rank = font.render(f"Card Rank: {card1.rank}", True, white)
    suit = font.render(f"Card Suit: {card1.suit}", True, white)
    suit_text = font.render(f"Suit Text: {card1.suit_text}", True, white)
    color = font.render(f"Color: {card1.color}", True, white)
    image_display = font.render(f"Image Displayed: {card1.image}", True, white)
    displayable = font.render(f"Displayable: {card1.displayable}", True, white)
    str_display = font.render(f"__str__: {card1.__str__()}", True, white)
    new_card = f'{new_suit},{new_rank}'


Button(300, 20, 280, 30, 'Flip Card', flip_card)
Button(480, 350, 100, 30, 'Change Card',change_card)
rank = font.render(f"Card Rank: {card1.rank}", True, white)
suit = font.render(f"Card Suit: {card1.suit}", True, white)
suit_text = font.render(f"Suit Text: {card1.suit_text}", True, white)
color = font.render(f"Color: {card1.color}", True, white)
image_display = font.render(f"Image Displayed: {card1.image}", True, white)
displayable = font.render(f"Displayable: {card1.displayable}", True, white)
str_display = font.render(f"__str__: {card1.__str__()}", True, white)
new_card_input = pygame.Rect(430, 350, 10, 30)

while True:
    screen.fill(green)
    screen.blit(card_image, (20, 20))
    screen.blit(rank, (300, 60))
    screen.blit(suit, (300, 90))
    screen.blit(suit_text, (300, 120))
    screen.blit(color, (300, 150))
    screen.blit(image_display, (300, 180))
    screen.blit(displayable, (300, 210))
    screen.blit(str_display, (300, 240))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if new_card_input.collidepoint(event.pos):
                active = True
                new_card = ''
            else:
                active = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                new_card = new_card[:-1]
            else:
                new_card += event.unicode

    if active:
        box_color = grey
    else:
        box_color = white
    pygame.draw.rect(screen, box_color, new_card_input)
    text_surface = font.render(new_card, False, black)
    screen.blit(text_surface, (new_card_input.x + 5, new_card_input.y + 5))
    new_card_input.w = max(30, text_surface.get_width()+10)
    for object in objects:
        object.process()
    pygame.display.flip()
    fpsClock.tick(fps)

    pygame.display.update()
    fpsClock.tick(60)
