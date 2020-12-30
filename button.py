import pygame
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Test visualize")

font = pygame.font.SystemFont("Constantia", 30)


bg = (200,200,200)
red = (255,0,0)
black = (0,0,0)
white = (255,255,255)

clicked = False
counter = 0


class Button():

    button_col = (25,190,225)
    hover_col = (75, 225, 255)
    click_col = (50,150,225)
    text_col = (255,255,255)
    width = 180
    height = 40

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def draw_button(self):

        global clicked
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        button_rect = Rect(self.x, self.y, self.width, self.height)


        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(screen, self.click_col, button_rect)
            elif: pygame.mouse.get_pressed()[0] == 0 and clicked == False:
                clicked = False
                action = True
            else:
                pygame.draw.rect(screen, self.hover_col, button_rect)
        else:
            pygame.draw.rect(screen, self.button_col, button_rect)

        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2)), self.y + 5 )
    