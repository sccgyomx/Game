from turtle import position
from colores import *
from player import Player
from enemy import Enemy
from shot import Shot
import pygame
import random
import sys


coorListStars = []
speedY = 0
speedX = 0
enemy_list=[]
shot_enemies = []
shot_player=[]
mouse_pos=(0,0)
Terminar = False
pantalla = "menu"
score = 0

imageEnemy=pygame.image.load("nave_espacial.png")
imageEnemy=pygame.transform.scale(imageEnemy,(40,40))

imagePlayer=pygame.image.load("nave_extraterrestre.png")
imagePlayer=pygame.transform.scale(imagePlayer,(40,40))

def detectar_eventos():
    global speedX, speedY, Terminar, mouse_pos
    for event in pygame.event.get():
        exit_detection(event)
        player_motion_detection(event)
        left_click_detection(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mouse_pos = pygame.mouse.get_pos()
                shot_player.append(generate_shot((mouse_pos[0] - player.PositionX) /60, (mouse_pos[1] - player.PositionY) /60, player.PositionX, player.PositionY))

def generate_shot(rateOnFireX, rateOnFireY,PositionX, PositionY):
    if (-10 > rateOnFireX > 10) or (-10 > rateOnFireY > 10):
        rateOnFireX = rateOnFireX*3
        rateOnFireY = rateOnFireY*3
    return Shot(rateOnFireX,rateOnFireY,PositionX,PositionY)


def collider_check(shotPositionX,shotPositionY,targetPositionX,targetPositionY):
    if (shotPositionX-9 < targetPositionX < shotPositionX + 9 ) and (shotPositionY - 9 < targetPositionY < shotPositionY + 9 ):
        print(f"posicion del disparo {shotPositionX},{shotPositionY} y posicion del objetivo {targetPositionX},{targetPositionY}")
        return True


def left_click_detection(event):
    global  pantalla
    if event.type == pygame.MOUSEBUTTONDOWN:
        if pantalla == "menu":
            pantalla = "game"
        if pantalla == "gameOver":
            pantalla = "menu"

def exit_detection(event):
    if event.type == pygame.QUIT:
        sys.exit()

def player_motion_detection(event):
    global speedX, speedY,Terminar
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            speedX = -3
        if event.key == pygame.K_d:
            speedX = 3
        if event.key == pygame.K_w:
            speedY = -3
        if event.key == pygame.K_s:
            speedY = 3

        if event.key == pygame.K_RETURN:
            Terminar = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
            speedX = 0
        if event.key == pygame.K_d:
            speedX = 0
        if event.key == pygame.K_w:
            speedY = 0
        if event.key == pygame.K_s:
            speedY = 0

def terminar():
    return Terminar

#stars---------------------------------------------------------------------------
def generate_stars_list():
    for i in range(100):
        x = random.randint(0, 800)
        y = random.randint(0, 500)
        coorListStars.append([x, y])


def drawing_star_list(display):
    for coordenada in coorListStars:
        numero_random = random.randint(0,2)
        if numero_random == 0:
            pygame.draw.circle(display, white, (coordenada[0], coordenada[1]), 2)
        elif numero_random == 1:
            pygame.draw.circle(display, yellow, (coordenada[0], coordenada[1]), 3)
        else:
            pygame.draw.circle(display, orange, (coordenada[0], coordenada[1]), 2)
        coordenada[1] += 1
        if coordenada[1] == 500:
            coordenada[1] = 0
#stars---------------------------------------------------------------------------------------------------------}


#player >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def generate_player():
    global player
    player = Player(random.randint(10,790),random.randint(10,490))


def player_movement():
    if speedX < 0:
        if 23 < player.PositionX:
            player.PositionX = player.PositionX + speedX
    if speedX > 0:
        if player.PositionX <= 777:
            player.PositionX = player.PositionX + speedX
    if speedY < 0:
        if 23 < player.PositionY:
            player.PositionY = player.PositionY + speedY
    if speedY > 0:
        if player.PositionY <= 477:
            player.PositionY = player.PositionY + speedY


def draw_Player(display):
    global imagePlayer
    display.blit(imagePlayer,(player.PositionX-20, player.PositionY-20,10,10))


def draw_shots_player(display):
    global enemy_list, score
    for shot_p in shot_player:
        shot_p.shot_directionX += shot_p.rateOnFireX
        shot_p.shot_directionY += shot_p.rateOnFireY

        for enemy in enemy_list:
            if collider_check(shot_p.shot_directionX,shot_p.shot_directionY,enemy.positionX, enemy.positionY):
                enemy_list.remove(enemy)
                shot_player.remove(shot_p)
                score+=1


        pygame.draw.circle(display,green,(shot_p.shot_directionX,shot_p.shot_directionY),4)
        if check_if_it_is_on_the_screen(shot_p.shot_directionX,shot_p.shot_directionY):
            shot_player.remove(shot_p)

def check_if_it_is_on_the_screen(directionX,directionY): #Funtion generic
    validation = True
    if -5 <= directionX <= 810 and -5 <= directionY <= 510:
        validation= False
    return  validation
        
#player <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


#enemy
def generate_enemies_list():
    for i in range(random.randint(1,6)):
        x = random.randint(0, 800)
        y = random.randint(0, 500)
        sX = random.randint(-1, 1)
        sY = random.randint(-1, 1)
        enemy_list.append(Enemy(x, y, sX, sY))

def spawn_enemis(display):
    global player, imageEnemy
    if len(enemy_list)>0:
        for enemy in enemy_list:
            display.blit(imageEnemy,(enemy.positionX-20, enemy.positionY-20,10,10))
            if random.randint(0,300)==180:
                shot_enemies.append(generate_shot((player.PositionX - enemy.positionX) /60, (player.PositionY - enemy.positionY) /60, enemy.positionX, enemy.positionY))



def enemy_movement():
    if len(enemy_list):
        for enemy in enemy_list:
            if -5 <= enemy.positionX <= 810 and -5 <= enemy.positionY <= 510:
                enemy.positionX += enemy.speedX
                enemy.positionY += enemy.speedY
            else:
                enemy.speedY = enemy.speedY *-1
                enemy.speedX = enemy.speedX *-1

                enemy.positionX += enemy.speedX
                enemy.positionY += enemy.speedY


def draw_shot_enemy(display):
    global player,enemy_list,pantalla,score
    for shot_enemy in shot_enemies:
        shot_enemy.shot_directionX += shot_enemy.rateOnFireX
        shot_enemy.shot_directionY += shot_enemy.rateOnFireY
        
        print("Disparo enemigo")    
        if collider_check(shot_enemy.shot_directionX,shot_enemy.shot_directionY ,player.PositionX,player.PositionY):
            print("Jugador eliminado")
            shot_enemies.clear()
            enemy_list.clear()
            pantalla="gameOver"
            writeScore(score)
            shot_player.clear()

        pygame.draw.circle(display,red,(shot_enemy.shot_directionX, shot_enemy.shot_directionY), 4)
        if check_if_it_is_on_the_screen(shot_enemy.shot_directionX,shot_enemy.shot_directionY):
            shot_enemies.remove(shot_enemy)
#enemy


#Score.........................................
def readMaxScore():
    maxScore = 0
    archi1=open("datos.txt","r")
    for linea in archi1:
        maxScore=int(linea)
    archi1.close()
    return maxScore


def writeScore(score):
    if score> readMaxScore():
        datos=open("datos.txt","w") 
        datos.write(f"{score}") 
        datos.close() 
#Score.........................................


def menu(display, titulo, font1,font2):
    global score
    score=0
    Titulo = titulo.render(f"El juego de las navecitas sin sprite's",True,orange)
    TituloX = 400 - (Titulo.get_width() // 2)

    objetivo1 = font1.render(f"El objetivo pricipal es divertirte disparandole a las naves enemigas para",True,white)
    objetivoX1 = 400 - (objetivo1.get_width() // 2)
    objetivo2 = font1.render(f"obtener una puntuacion mayor, al igual debes evitar que alguno de sus",True,white)
    objetivoX2 = 400 - (objetivo2.get_width() // 2)
    objetivo3 = font1.render(f"disparos te toque, recuerda siempre batir tu propio record.",True,white)
    objetivoX3 = 400 - (objetivo3.get_width() // 2)
    
    movimientos = font2.render("movimientos: W = , S = , A = , D =  ",True,blue)
    movimientosX = 400 - (movimientos.get_width() // 2)

    shots = font2.render("El barra espaciadora activa los disparos",True,blue)
    shotsX = 400 - (shots.get_width() // 2)
    
    target = font2.render("Los disparos del jugador siguen al ",True,blue)
    targetX = 400 - (target.get_width() // 2)

    playerIcon = font2.render("EL jugador es:  ",True,green)
    playerIconX = 250 - (playerIcon.get_width()//2)
    enemyIcon = font2.render("Los enemigos son:  ",True,red)
    enemyIconX = 550 - (enemyIcon.get_width()//2)

    instCerrar = font1.render("Precione  o de click en  de la barra de titulo para cerrar",True, red)
    instCerrarX = 400 - ( instCerrar.get_width() // 2 )

    instruccionIniciar = font1.render("Precione el click izquierdo para iniciar",True, green)
    instIniciar = 400 - (instruccionIniciar.get_width() // 2)

    display.blit(Titulo, (TituloX, 0))
    display.blit(objetivo1, (objetivoX1, 50))
    display.blit(objetivo2, (objetivoX2, 80))
    display.blit(objetivo3, (objetivoX3, 110))
    display.blit(movimientos, (movimientosX, 150))
    display.blit(shots, (shotsX, 200))
    display.blit(target, (targetX, 250))
    display.blit(playerIcon, (playerIconX, 300))
    display.blit(enemyIcon, (enemyIconX, 300))
    display.blit(instCerrar, (instCerrarX, 350))
    display.blit(instruccionIniciar, (instIniciar, 400))

def game(display, font1):
    global score
    if not coorListStars:
        generate_stars_list()
    drawing_star_list(display)
    
    
    if not enemy_list:
        generate_enemies_list()
    spawn_enemis(display)
    enemy_movement()
    if shot_enemies:
        draw_shot_enemy(display)

    player_movement()
    if shot_player:
        draw_shots_player(display)
    maxScore=readMaxScore()
    text = font1.render(f"Puntuación: {score}   Maxima Puntuación: {maxScore}",True,blue)
    centerX=400-(text.get_width() // 2)
    display.blit(text,(centerX,0))
    draw_Player(display)

def game_over(display, titulo,font1):
    global score
    text = titulo.render(f"Game Over",True,white)
    centerX=400-(text.get_width() // 2)
    display.blit(text,(centerX,0))

    maxScore=readMaxScore()
    text = titulo.render(f"Puntuación: {score}   Maxima Puntuación: {maxScore}",True,orange)
    centerX=400-(text.get_width() // 2)
    display.blit(text,(centerX,200))

    instruccionIniciar = font1.render("Precione el click izquierdo para regresar a las instrucciones",True, green)
    instIniciar = 400 - (instruccionIniciar.get_width() // 2)
    display.blit(instruccionIniciar, (instIniciar, 400))



#zona de dibujo
def drawing_and_logic_zone(display,titulo,font1,font2):
    if pantalla == "menu":
        menu(display,titulo, font1,font2)
    if pantalla == "game":
        game(display, font1)
    if pantalla == "gameOver":
        game_over(display, titulo,font1)

