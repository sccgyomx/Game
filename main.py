from colores import *
from MainFunciones import *
import pygame

size = (800,500)
display = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.font.init()
titulo= pygame.font.Font("JetBrainsMonoBoldItalicNerdFontCompleteMono.ttf",30)
font1= pygame.font.Font("JetBrainsMonoBoldItalicNerdFontCompleteMono.ttf",15)
font2= pygame.font.Font("JetBrainsMonoBoldItalicNerdFontCompleteMono.ttf",22)

generate_player()

run = True
while run:
    if terminar():
        run = False
    detectar_eventos()
    display.fill(background)
    drawing_and_logic_zone(display,titulo,font1,font2)
    pygame.display.flip()
    clock.tick(60)