import pygame,sys
from PIL import ImageColor

pygame.init()

#definimos colores
background = ImageColor.getcolor("#282a36", "RGB")
white = ImageColor.getcolor("#f8f8f2", "RGB")
red = ImageColor.getcolor("#ff5555", "RGB")
blue = ImageColor.getcolor("#8be9fd", "RGB")
green = ImageColor.getcolor("#50fa7b", "RGB")

size = (800,500) #definimos el tamaño de la ventana

screen = pygame.display.set_mode(size) #creamos la ventana
#definimos el reloj para controlar los FPS
clock = pygame.time.Clock()


#tamaño
tam = 10

# mouse invisible => pygame.mouse.set_visible(0)
# mouse visible => pygame.mouse.set_visible(1)

#definimos la posicion y velocidad inicial del circulo
circle_posix = 30
circle_posiy = 250
speedX = 0
speedY = 0

#definimos la la direccion del tiro
rateOnFireX=0
rateOnFireY=0

shot_direction=[-10,-10]

enemyPositionX=0
enemyPositionY=0

count_direction=0

def detect_movement():
    global speedX, speedY
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            speedX = -3
        if event.key == pygame.K_d:
            speedX = 3
        if event.key == pygame.K_w:
            speedY = -3
        if event.key == pygame.K_s:
            speedY = 3
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
            speedX = 0
        if event.key == pygame.K_d:
            speedX = 0
        if event.key == pygame.K_w:
            speedY = 0
        if event.key == pygame.K_s:
            speedY = 0


def detect_shot():
    global rateOnFireX, rateOnFireY, enemyPositionX, enemyPositionY, shot_direction
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:

            shot_direction[0] = circle_posix
            shot_direction[1] = int(circle_posiy)

            enemyPositionX = pygame.mouse.get_pos()[0]
            enemyPositionY = pygame.mouse.get_pos()[1]

            if (enemyPositionX - circle_posix) > 0:
                rateOnFireX = (enemyPositionX - circle_posix)/60
            if (enemyPositionX - circle_posix) < 0:
                rateOnFireX = ((enemyPositionX - circle_posix)/60)
            if (enemyPositionY - circle_posiy) > 0:
                rateOnFireY = (enemyPositionY - circle_posiy)/60
            if (enemyPositionY - circle_posiy) < 0:
                rateOnFireY = ((enemyPositionY - circle_posiy)/60)

def detect_event():
    global event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        detect_movement()
        detect_shot()


def frame_logic():
    global mouse_pos, circle_posix, circle_posiy, enemyPosition
    global shot_direction, rateOnFireX, rateOnFireY
    #  ZONA DE LOGICA DE ANIMACIONES Y JUEGO
    mouse_pos = pygame.mouse.get_pos()

    if speedX <0:
        if 23 < circle_posix:
            circle_posix = circle_posix + speedX
    if speedX>0:
        if circle_posix <= 777:
            circle_posix = circle_posix + speedX
    if speedY < 0:
        if 23 < circle_posiy:
            circle_posiy = circle_posiy + speedY
    if speedY > 0:
        if circle_posiy <= 477:
            circle_posiy = circle_posiy + speedY

    if -5 <= shot_direction[0] <= 810 and -5 <= shot_direction[1] <= 510:
        shot_direction[0] = shot_direction[0] + rateOnFireX * 2
        shot_direction[1] = shot_direction[1] + rateOnFireY * 2
        print(shot_direction)
    else:
        shot_direction[0] = shot_direction[0] + 0
        shot_direction[1] = shot_direction[1] + 0

    # ----------------------------------------


def draw_frames():
    global count_direction
    screen.fill(background)  # añedimos color de fondo
    # Zona de dibujo
    pygame.draw.rect(screen, red, (mouse_pos[0] - (tam / 2), mouse_pos[1] - (tam / 2), tam, tam))
    pygame.draw.circle(screen, green, (circle_posix, circle_posiy), 20)

    pygame.draw.rect(screen,red,(shot_direction[0]-5,shot_direction[1]-5,10,10))
    # ------------------------------------------------
    # actualizamos pantalla



while True:
    detect_event()
    frame_logic()
    draw_frames()
    pygame.display.flip()
    clock.tick(60)