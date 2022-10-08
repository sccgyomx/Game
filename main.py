import random
import pygame
import sys
from PIL import ImageColor

from shot import Shot
from enemy import Enemy

pygame.init()

# definimos colores
background = ImageColor.getcolor("#282a36", "RGB")
white = ImageColor.getcolor("#f8f8f2", "RGB")
red = ImageColor.getcolor("#ff5555", "RGB")
blue = ImageColor.getcolor("#8be9fd", "RGB")
green = ImageColor.getcolor("#50fa7b", "RGB")
orange = ImageColor.getcolor("#ffb86c","RGB")
yellow = ImageColor.getcolor("#f1fa8c","RGB")

game_over = False
start = False


size = (800, 500)  # definimos el tamaño de la ventana

screen = pygame.display.set_mode(size)  # creamos la ventana
# definimos el reloj para controlar los FPS
clock = pygame.time.Clock()

# tamaño
global tam

# mouse invisible => pygame.mouse.set_visible(0)
# mouse visible => pygame.mouse.set_visible(1)

# definimos la posicion y velocidad inicial del circulo
global playerPositionX
global playerPositionY
global speedX
global speedY

# definimos la la direccion del tiro
global rateOnFireX
global rateOnFireY

global shot_direction

global enemyPositionX
global enemyPositionY

global count_direction

global coorListStars

global player_shot_drawing
global enemy_shot_drawing
global user_shot_list
global enemy_list
global shot_enemy_list
global score_player


def generate_stars_list():
    for i in range(100):
        x = random.randint(0, 800)
        y = random.randint(0, 500)
        coorListStars.append([x, y])


def generate_enemies_list():
    for i in range(random.randint(1,6)):
        x = random.randint(0, 800)
        y = random.randint(0, 500)
        sX = random.randint(-1, 1)
        sY = random.randint(-1, 1)
        enemy_list.append(Enemy(x, y, sX, sY))


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
    global rateOnFireX, rateOnFireY, enemyPositionX, enemyPositionY, shot_direction, user_shot_list
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            enemyPositionX = pygame.mouse.get_pos()[0]
            enemyPositionY = pygame.mouse.get_pos()[1]
            rateOnFireX = (enemyPositionX - playerPositionX) / 60
            rateOnFireY = (enemyPositionY - playerPositionY) / 60
            user_shot_list.append(Shot(rateOnFireX, rateOnFireY, playerPositionX, playerPositionY))


def detect_event():
    global event, game_over,start
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not start:
                start = True
            if game_over:
                start = False
                game_over = False
        detect_movement()
        detect_shot()


def frame_logic():
    global mouse_pos
    global shot_direction, rateOnFireX, rateOnFireY
    #  ZONA DE LOGICA DE ANIMACIONES Y JUEGO
    mouse_pos = pygame.mouse.get_pos()
    player_movement()
    player_shot_movement()
    enemy_movement()
    create_enemy_shots()
    add_speed_enemy_shot()
    # ----------------------------------------


def add_speed_enemy_shot():
    if len(enemy_list) > 0:
        for enemy in enemy_list:
            if len(shot_enemy_list) > 0:
                for enemyShot in shot_enemy_list:
                    if -5 <= enemyShot.shot_directionX <= 810 and -5 <= enemyShot.shot_directionY <= 510:
                        enemyShot.shot_directionX += enemyShot.rateOnFireX * 0.05
                        enemyShot.shot_directionY += enemyShot.rateOnFireY * 0.05
                    else:
                        shot_enemy_list.remove(enemyShot)


def create_enemy_shots():
    global rateOnFireX, rateOnFireY, playerPositionX, playerPositionY
    if len(enemy_list):
        for enemy in enemy_list:
            if enemy_shot_validation():
                rateOnFireX = (playerPositionX - enemy.positionX) / 60
                rateOnFireY = (playerPositionY - enemy.positionY) / 60
                shot_enemy_list.append(Shot(rateOnFireX, rateOnFireY, enemy.positionX, enemy.positionY))


def enemy_shot_validation():
    if random.randint(0, 300) == 180:
        return True
    else:
        return False


def enemy_movement():
    if len(enemy_list):
        for enemy in enemy_list:
            if -5 <= enemy.positionX <= 810 and -5 <= enemy.positionY <= 510:
                enemy.positionX += enemy.speedX
                enemy.positionY += enemy.speedY
            else:
                enemy.positionX = random.randint(0, 800)
                enemy.positionY = random.randint(0, 500)


def player_shot_movement():
    if len(user_shot_list) > 0:
        for user_shot in user_shot_list:
            if -5 <= user_shot.shot_directionX <= 810 and -5 <= user_shot.shot_directionY <= 510:
                user_shot.shot_directionX += user_shot.rateOnFireX
                user_shot.shot_directionY += user_shot.rateOnFireY
            else:
                for shot in player_shot_drawing:
                    if user_shot in shot:
                        player_shot_drawing.remove(shot)
                        if user_shot in user_shot_list:
                            user_shot_list.remove(user_shot)


def player_movement():
    global playerPositionX, playerPositionY
    if speedX < 0:
        if 23 < playerPositionX:
            playerPositionX = playerPositionX + speedX
    if speedX > 0:
        if playerPositionX <= 777:
            playerPositionX = playerPositionX + speedX
    if speedY < 0:
        if 23 < playerPositionY:
            playerPositionY = playerPositionY + speedY
    if speedY > 0:
        if playerPositionY <= 477:
            playerPositionY = playerPositionY + speedY


def player():
    global enemy_shot_drawing, enemy_list, game_over,start
    Player = pygame.draw.circle(screen, green, (playerPositionX, playerPositionY), 10)
    if len(enemy_shot_drawing) > 0:
        for shot in enemy_shot_drawing:
            if Player.colliderect(shot[0]):
                if shot[1] in shot_enemy_list:
                    print(Player)
                    print(shot,shot_enemy_list)
                    enemy_shot_drawing.clear()
                    enemy_list.clear()
                    user_shot_list.clear()
                    shot_enemy_list.clear()
                    game_over = True
                    start = False


def relative_position_target():
    pygame.draw.rect(screen, red, (mouse_pos[0] - (tam / 2), mouse_pos[1] - (tam / 2), tam, tam))


def draw_frames():
    global count_direction
    # Zona de dibujo
    starts_loop()
    spawn_enemy_shot()
    relative_position_target()
    draw_players_shot()
    player()
    # ------------------------------------------------
    # actualizamos pantalla


def spawn_enemy_shot():
    global score_player
    if len(enemy_list) > 0:
        for enemy in enemy_list:
            ENEMY = pygame.draw.circle(screen, red, (enemy.positionX, enemy.positionY), 10)
            if len(player_shot_drawing)>0:
                for shot in player_shot_drawing:
                    if ENEMY.colliderect(shot[0]):
                        if shot[1] in user_shot_list:
                            user_shot_list.remove(shot[1])
                            enemy_list.remove(enemy)
                            player_shot_drawing.remove(shot)
                            score_player += 1

            if len(shot_enemy_list) > 0:
                for enemyShot in shot_enemy_list:
                    EnemyShot = pygame.draw.circle(screen, red, (enemyShot.shot_directionX, enemyShot.shot_directionY), 4)
                    enemy_shot_drawing.append((EnemyShot, enemyShot))


def draw_players_shot():
    if len(user_shot_list) > 0:
        for user_shot in user_shot_list:
            UserShot = pygame.draw.circle(screen, green, (user_shot.shot_directionX, user_shot.shot_directionY), 4)
            player_shot_drawing.append((UserShot, user_shot))


def starts_loop():
    for coordenada in coorListStars:
        numero_random = random.randint(0,2)
        if numero_random == 0:
            pygame.draw.circle(screen, white, (coordenada[0], coordenada[1]), 2)
        elif numero_random == 1:
            pygame.draw.circle(screen, yellow, (coordenada[0], coordenada[1]), 3)
        else:
            pygame.draw.circle(screen, orange, (coordenada[0], coordenada[1]), 2)
        coordenada[1] += 1
        if coordenada[1] == 500:
            coordenada[1] = 0


def initialize_variables():
    global tam, playerPositionX, playerPositionY, speedX, speedY, rateOnFireX, rateOnFireY, shot_direction, enemyPositionX, enemyPositionY, count_direction, coorListStars, player_shot_drawing, enemy_shot_drawing, user_shot_list, enemy_list, score_player, shot_enemy_list
    # tamaño
    tam = 10
    # mouse invisible => pygame.mouse.set_visible(0)
    # mouse visible => pygame.mouse.set_visible(1)
    # definimos la posicion y velocidad inicial del circulo
    playerPositionX = 30
    playerPositionY = 250
    speedX = 0
    speedY = 0
    # definimos la la direccion del tiro
    rateOnFireX = 0
    rateOnFireY = 0
    shot_direction = [-10, -10]
    enemyPositionX = 0
    enemyPositionY = 0
    count_direction = 0
    coorListStars = []
    player_shot_drawing = []
    enemy_shot_drawing = []
    user_shot_list = []
    enemy_list = []
    shot_enemy_list = []
    score_player = 0


def text_screen_gameOver_Start(texto):
    font = pygame.font.SysFont("JetBrainsMono Nerd Font", 25)
    text = font.render(texto, True, white)
    centerX = (size[0] // 2) - (text.get_width() // 2)
    centerY = (size[1] // 2) - (text.get_height() // 2)
    screen.blit(text, [centerX, centerY])


while True:
    detect_event()
    screen.fill(background)  # añedimos color de fondo
    if not game_over and not start:
        initialize_variables()
        text_screen_gameOver_Start("Click To Start")
    if start:
        if not enemy_list:
            generate_enemies_list()
        if not coorListStars:
            generate_stars_list()
        frame_logic()
        draw_frames()

        font = pygame.font.SysFont("JetBrainsMono Nerd Font", 25)
        text = font.render("score : "+str(score_player), True, white)
        centerX = (size[0] // 2) - (text.get_width() // 2)
        screen.blit(text, [centerX, 0])

    if game_over:
        text_screen_gameOver_Start("Click To Screen Start")
    pygame.display.flip()
    clock.tick(60)
