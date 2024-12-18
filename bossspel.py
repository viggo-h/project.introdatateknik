

import pygame
import random
import sys
pygame.init()


from boss import spawn_boss,boss_movment, boss_collaterate, boss_attack
boss_exist = False


# Skapa fönstret
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame")

#Bilder på spelaren
mario_still = pygame.image.load("mario_still.PNG")
mario_still = pygame.transform.scale(mario_still, (70,83))
mario_running_right = pygame.image.load("mario_running_right.PNG")
mario_running_right = pygame.transform.scale(mario_running_right, (80,83)) #(Facing right)
mario_running_left = pygame.image.load("mario_running_left.PNG")
mario_running_left = pygame.transform.scale(mario_running_left, (80,83))
mario_jumping_right = pygame.image.load("mario_jumping_right.PNG")
mario_jumping_right = pygame.transform.scale(mario_jumping_right, (75,83))
mario_jumping_left = pygame.image.load("mario_jumping_left.PNG")
mario_jumping_left = pygame.transform.scale(mario_jumping_left, (75,83))
mario_groundpound = pygame.image.load("mario_groundpound.PNG")
mario_groundpound = pygame.transform.scale(mario_groundpound, (120,85))

#Blå knapp bild
proceed_button = pygame.image.load("redbutton.png")
proceed_button = pygame.transform.scale(proceed_button,(30,30))
# Bakgrundsbild
background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (800, 600))  
start_background_image = pygame.image.load("Arcade Gamer.PNG")
start_background_image = pygame.transform.scale(start_background_image, (800,600))
victory_background_image = pygame.image.load("victoryscreen.png")
victory_background_image = pygame.transform.scale(victory_background_image, (800,600))

#Bilder för hinder
brick_wall = pygame.image.load("brick_wall.jpg")
brick_wall = pygame.transform.scale(brick_wall, (100, 40))
stone = pygame.image.load("stone.PNG")
stone = pygame.transform.scale(stone, (10,10))


#Ljudeeffekter
sound_effects = {
    "jump": pygame.mixer.Sound("mario_jump_soundsfx.mp3"),
    #"die": , 
    "boss_talk1": pygame.mixer.Sound("boss_monologue1.mp3"),
    "boss_take_dmg":pygame.mixer.Sound("boss_taking_dmg.mp3"),
    "victory": pygame.mixer.Sound("victory_music.mp3"),
    "firework": pygame.mixer.Sound("victory_firework.mp3"),
}   
#Musik
music_tracks = {
    "start_menu": "start_menu_music.mp3",
    1: "level1_music.mp3",
    2: "level2_music.mp3",
    3: "boss_music_phase1.mp3",
    4: "boss_music_phase1.mp3",
    5: "boss_music_phase1.mp3",
    "gameover": "gameover_music.mp3"
}
def play_music(track_key):
    if track_key in music_tracks:
        pygame.mixer.music.load(music_tracks[track_key])
        pygame.mixer.music.play(-1)

play_music("start_menu") 
gameover_music_played, level1_music, level2_music, level3_music, level4_music,level5_music,boss_talk1,boss_encountered = False,False,False,False,False,False,False,False


# Färger 
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0,0,255)
red = (255, 0, 0)
silver =(192, 192, 192)
yellow =(255,223,0)
brown = (90, 78, 68)
blood_red = (166,16,30)
cave_grey = (59,74,79)
red_blood = (190,6,6)

# Huvudkaraktär position 
circle_x, circle_y = 40, 500
circle_radius = 40
circle_speed_x = 10
circle_speed_y = 0
jump_strength = -10
gravity = 0.5
on_ground,doublejump,movment_lock,jumping = False,False,False,False

#Liv och skada
hearts = 3
tagen_skada = False
kollision = False

#fiende
fiende_x, fiende_y = 540, 50
fiende_storlek = 80
fiende_speed_x = 0
fiende_speed_y = 5
fiende_image = pygame.image.load("Thwomp.gif")
fiende_image = pygame.transform.scale(fiende_image, (80, 80)) 

#fiende 2
fiende2_X, fiende2_y = 320, 530
fiende2_storlek = 80
fiende2_speedX = 10
fiende2_image = pygame.image.load("bulletbill.png")
fiende2_image = pygame.transform.scale(fiende2_image, (105, 85))

#Kannonens attribut
cannon_x, cannon_y, cannon_size = -95, 436, 200
cannon_image = pygame.image.load("billblaster.png")
cannon_image = pygame.transform.scale(cannon_image, (cannon_size, cannon_size))

#vinna grejer
cube_x, cube_y = 713, 520
cube_size_x,cube_size_y = 80,100  
pipe_image = pygame.image.load("pipe.PNG")
pipe_image = pygame.transform.scale(pipe_image, (cube_size_x, cube_size_y))  
pipe_image_rotated = pygame.transform.rotate(pipe_image, 90)

#Text
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

#level osv
level = 1  
level_start = False
startmenu = True
gameover = False
onplatform = False

#lava
lavared = (255, 48, 48)
lava_x = 375
lava_y = 580
lava_width = 250
lava_height = 20
lava = pygame.Rect(lava_x, lava_y, lava_width, lava_height)



def show_start_menu(): #startskärm
    screen.blit(start_background_image,(0,0))
    pygame.display.flip()

def victory_screen():  #Vinstskärm
    screen.blit(victory_background_image,(0,0))
    pygame.display.flip()
    
def show_gameover(): #game over skärm
    screen.fill(black)
    gameover_text = font.render("Game Over!", True, red)
    restart_text = small_font.render("Press enter to try again", True, white)
    screen.blit(gameover_text, (800 // 2 - gameover_text.get_width() // 2, 250))
    screen.blit(restart_text, (800 // 2 - restart_text.get_width() // 2, 350))
    pygame.display.flip()

def environment(level):#level system
    if level < 3:
        title_text = font.render(f"Level {level}", True, white)
        screen.blit(title_text, (10, 30))
    elif level < 6:
        boss_text = font.render(f"MOVE TO SURVIVE!", True, blood_red)
        screen.blit(boss_text, (10,10))
    else: 
        title_text = font.render(f"Level {level}", True, white)
        screen.blit(title_text,(-100,-100))


def lives(hearts):   #Life counter
    if level < 3:
        life_text = small_font.render(f"Lives {hearts}", True, white)
        screen.blit(life_text, (700,30))
    elif level == 3: 
        boss1_text = small_font.render(f"3 Rooms left", True, red_blood)
        screen.blit(boss1_text, (650,20))
    elif level == 4:
        boss2_text = small_font.render(f"2 Rooms left", True, red_blood)
        screen.blit(boss2_text, (650,20))
    elif level == 5: 
        boss3_text = small_font.render(f"FINAL ROOM!", True, red_blood)
        screen.blit(boss3_text, (635,20))
    else: 
        life_text = small_font.render(f"Lives {hearts}", True, white)
        screen.blit(life_text, (-100,-100))

class ObstaclePainter:          #To make obstacles
    def __init__(self, screen, stone):
        self.screen = screen
        self.stone = stone

    def render(self, obstacles):
        for obstacle in obstacles:
            for x in range(obstacle.x, obstacle.x + obstacle.width, self.stone.get_width()):
                for y in range(obstacle.y, obstacle.y + obstacle.height, self.stone.get_height()):
                    self.screen.blit(self.stone, (x, y))

obstacle_painter = ObstaclePainter(screen,stone)

# Huvudloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif startmenu and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: #startmeny spelet startar vid enter
            startmenu = False
            play_music(level)
        elif gameover and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: #gameover spelet startar om vid enter
            if event.key == pygame.K_RETURN: #reset spelet
                circle_x, circle_y = 40, 450
                fiende_x, fiende_y = 540, 50
                fiende_speed_y = 5
                level = 1
                hearts = 3
                gameover = False
                gameover_music_played = False
                

            elif event.key == pygame.K_RETURN:
                pygame.quit()
                sys.exit()
    
    if hearts <= 0 and not gameover:  
        gameover = True
        gameover_music_played = False
    
    if startmenu:
        show_start_menu()
        continue
    elif gameover:
        if not gameover_music_played:
            pygame.mixer.music.stop()   
            if level < 6 :
                play_music("gameover")      
            else:
                sound_effects["victory"].play()
                sound_effects["firework"].play()
            gameover_music_played = True
            level1_music = False
        if level < 6:
            level_start = False
            fiende_speed_x = 0
            circle_speed_x = 10
            fiende2_X, fiende2_y = 320, 530
            fiende_image = pygame.image.load("Thwomp.gif")
            fiende_image = pygame.transform.scale(fiende_image, (80, 80))
            background_image = pygame.image.load("background.png")
            background_image = pygame.transform.scale(background_image, (800, 600))
            show_gameover()
            continue  
        if level == 6:
            victory_screen()
            continue

    # Tangenttryckningar
    keys = pygame.key.get_pressed()
    
    movment = False
    movment_right = False
    movment_left = False
    movment_up = False
    movment_groundpound = False

    #x-led rörelse
    if not movment_lock:
        if keys[pygame.K_LEFT]:
            circle_x -= circle_speed_x
            movment = True
            movment_left = True
        if keys[pygame.K_RIGHT]:
            circle_x += circle_speed_x
            movment = True
            movment_right = True

         # Hopp och dubbelhopp
        if keys[pygame.K_UP] and on_ground:
            circle_y -= 5
            circle_speed_y = jump_strength
            on_ground = False
            doublejump = True
            movment = True
            movment_up = True
            if not jumping:
                sound_effects["jump"].stop()
                sound_effects["jump"].play()
                jumping = True
    
        elif keys[pygame.K_UP] and doublejump and circle_y < 500:
            circle_speed_y = jump_strength
            doublejump = False
            movment = True
            movment_up = True

    # snabbt ner
    if keys[pygame.K_DOWN] and on_ground == False and onplatform== False:
        gravity *= 1.25
        damage = 2
        movment = True
        movment_groundpound = True
    else:
        gravity = 0.5    
    
    # Gravitation och vertikal rörelse
    if onplatform == False:
        circle_speed_y += gravity
        circle_y += circle_speed_y

    # Begränsar cirklerns rörelse
    circle_x = max(circle_radius, min(800 - circle_radius, circle_x))
    if circle_y >= 600 - circle_radius: #om cirklen är innanför
        circle_y = 600 - circle_radius
        circle_speed_y = 0
        on_ground = True
        gravity = 0.5
        doublejump = False
        
    # Uppdatera level 
    if (level == 1  or level == 2 )and circle_x >= 730 and circle_y >= 540: ##level 1
        circle_x = 0
        circle_y = 560
        fiende_x = 40
        fiende_y = 520
        fiende_speed_x = 10
        level += 1
    if level == 3 and circle_x <= 140 and circle_y <100:
        circle_x = 0
        circle_y = 560
        level += 1
    if level == 4 and (circle_x >= 740 and (240<=circle_y<=300)):
        circle_x = 0
        circle_y = 560
        level +=1
    if level == 5 and ((380<=circle_x<=440) and (290<=circle_y<=350)):
        level +=1
    if level == 6:
        gameover = True

    # Fiende rörelse i x led
    if fiende_speed_y > 0:
        fiende_y += 2*fiende_speed_y
    if fiende_speed_y < 0:
        fiende_y += fiende_speed_y
        
    if level == 1 and fiende_y >= 500 or fiende_y <= 0:
        if fiende_speed_y == 8:
            fiende_speed_y = 0
        else:
            fiende_speed_y *= -1 
    fiende_x += fiende_speed_x
    fiende2_X += fiende2_speedX 
    if level == 2 and fiende_x >= 650:
        fiende_x = -50
        fiende_speed_x = 15
    if level == 2 and fiende2_X >= 650:
        fiende2_X = -50
        fiende2_speedX = 10
    

    #Uppdatera skärmen
    screen.blit(background_image, (0, 0))
    screen.blit(fiende_image,(fiende_x,fiende_y))
    
    
    #level
    environment(level)
    #Life counter
    lives(hearts)   
    
   

##Hinder
    
        
    #Skapar ett hinder och ger den en hitbox
    obstacles = []
    #Level 1
    if level == 1:
        
        if not level1_music:
            play_music(level)
            level1_music,level2_music,level3_music = True, False, False
            
        
        screen.blit(pipe_image,(cube_x,cube_y))   #Röret för nästa level
       
        obstacle1 = pygame.Rect(200, 425, 100., 50)
        obstacle2 = pygame.Rect(0, 300, 200, 50)
        obstacle3 = pygame.Rect(365, 200, 75, 50)
        obstacle4 = pygame.Rect(625, 150, 80, 450)
        obstacle5 = pygame.Rect(175, 300, 40, 175)
        obstacles =  [obstacle1, obstacle2, obstacle3, obstacle4, obstacle5]
        for obstacle in obstacles: 
            pygame.draw.rect(screen, brown, obstacle)
        
        player_rect = pygame.Rect(circle_x, circle_y, circle_radius*1.25, circle_radius*1.25)
        fiende_rect = pygame.Rect(fiende_x, fiende_y, fiende_storlek, fiende_storlek)
        
        fiende_kollision = player_rect.colliderect(fiende_rect)
        pygame.draw.rect(screen, lavared , lava)
        
        player_rect = pygame.Rect(circle_x, circle_y, circle_radius, circle_radius)
        if player_rect.colliderect(lava):
            hearts -= 1
            if hearts <= 0:
                gameover = True
            else:
            # Återställ spelarens position
                circle_x, circle_y = 40, 400
                player_speed_y = 0  # Nollställ spelarens vertikala hastighet

    # Kontrollera om spelet ska avslutas
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        
        
    if fiende_kollision:
    # Kontrollera om spelaren landar ovanpå fienden
        if circle_y + circle_radius <= fiende_y + 15 and circle_speed_y > 0:  # Om spelaren är nära ovanifrån
        # Fienden "försvinner" om spelaren landar på den
            circle_speed_y = jump_strength
            fiende_speed_y = 8
            on_ground = True  # Markera spelaren som på marken efter landning
            tagen_skada = False  # Spelaren tar ingen skada när den landar korrekt
        elif not tagen_skada and circle_speed_y < 0:
        # Spelaren tar skada om den krockar från sidan eller underifrån
            fiende_speed_y *=-1  # Fienden byter riktning
            hearts -= 1
            circle_x, circle_y = 40, 400
            tagen_skada = True
            if hearts == 0:
                gameover = True  # Spelet tar slut om inga hjärtan återstår
    else:
        tagen_skada = False 


    #Level 2 starter
    if level ==2 and not level_start: #Ge karatären en specifik startpunkt för map-building
        fiende_speed_y = 0
        circle_x, circle_y = 100, 410
        fiende_x, fiende_y = -420, 530
        background_image = pygame.image.load("cave.jpg")
        background_image = pygame.transform.scale(background_image, (800, 700))
        level_start = True
        play_music(level)
    
    #Level 2
    if level == 2:
        screen.blit(fiende2_image, (fiende2_X, fiende2_y))
        
        fiende_speed_x = 10
       
        
        fiende_image = pygame.image.load("bulletbill.png")
        fiende_image = pygame.transform.scale(fiende_image, (105, 85)) 
        spik_x, spik_y, spik_x_storlek = 400, 160, 20
        spik_NHX,spik_NHY,spik_NHsize = 745,420,30
        spik_gropX, spik_gropY,spik_gropSize = 440, 250, 150
        spik_HangX,spik_HangY,spik_HangSize = 230, 270, 70
        ob1 = pygame.Rect(0, 450, 200, 20)     #Botten man landar på
        ob2 = pygame.Rect(200, 90, 40, 380)    #Högra väggen där man startar
        ob3 = pygame.Rect(85, 345, 115, 20)    #Den lägre av de högra platformarna av hoppusslet i starten
        ob4 = pygame.Rect(0, 245, 100, 20)     #Den vänstra av platforma av hoppusslet i starten
        ob5 = pygame.Rect(85, 145, 115, 20)    #Den högre av de högra platformarna av hoppusslet i starten
        ob6 = pygame.Rect(0, 0, 800, 1)        #Takblockerare så att man inte kan hoppa ur skärmen
        ob7 = pygame.Rect(210, 240, 230, 20)   #Platformen under takspiken
        ob8 = pygame.Rect(620, 240, 90, 20)    #Platformen man hoppar till från under spiken
        ob9 = pygame.Rect(700, 90, 20, 170)    #Väggen till droppet uppe till höger
        ob10 = pygame.Rect(600, 120, 20, 20)   #Platformen bredvid takspiken
        ob11 = pygame.Rect(350, 500, 450, 20)  #Platformen man väntar på inför slutspurten
        ob12 = pygame.Rect(580, 0, 20, 140)    #Väggen mot takspikens högra sida
        ob13 = pygame.Rect(420, 260, 20, 80)   #Väggen till vänster om undre spiken
        ob14 = pygame.Rect(420, 340, 205, 20)  #Platformen under den grop spikarna
        ob15 = pygame.Rect(620, 260, 20, 100)  #Väggen till höger om den undre spiken
        obstacles = [ob1,ob2,ob3,ob4,ob5,ob6,ob7,ob8,ob9,ob10,ob11,ob12,ob13,ob14,ob15]
        #Kontakt och skada med spikar och fienden för level 2
        fiende_kollisionlv2 = (circle_x + 30 >= fiende_x and circle_x - 30 <= fiende_x + fiende_storlek and circle_y+circle_radius >= 560 )   
        spik_kollision_NH = (circle_x + 30 >= spik_NHX and circle_x -30 <= spik_NHX + spik_NHsize and circle_y >= spik_NHY - 20 and circle_y <= spik_NHY + 90)
        spik_kollision = (circle_x + 30 >= spik_x and circle_x -30 <= spik_x + spik_x_storlek and circle_y <= spik_y + 20)
        spik_kollision_grop = (circle_x + 30 >= spik_gropX and circle_x -30 <= spik_gropX + spik_gropSize and circle_y <= spik_gropY + 5 and circle_y >= spik_gropY -5)
        fiende2_kollision = (circle_x + 30 >= fiende2_X and circle_x - 30 <= fiende2_X + fiende2_storlek and circle_y+circle_radius >= 560 )
        if kollision == False:   
            if fiende_kollisionlv2 and not tagen_skada:       
                hearts -= 1
                circle_speed_x, circle_speed_y = 0,0
                circle_x, circle_y = 100, 395
                tagen_skada = True
                kollision = True
                if hearts == 0:
                    gameover = True  
            if spik_kollision_NH and not tagen_skada:    
                hearts-=1   
                circle_speed_x, circle_speed_y = 0,0
                circle_x, circle_y = 100, 395
                tagen_skada = True 
                kollision = True
                if hearts == 0:
                    gameover = True
            if spik_kollision and not tagen_skada:    
                hearts-=1   
                circle_speed_x, circle_speed_y = 0,0
                circle_x, circle_y = 100, 395
                tagen_skada = True 
                kollision = True
                if hearts == 0:
                    gameover = True     
            if spik_kollision_grop and not tagen_skada: 
                hearts-=1
                circle_speed_x, circle_speed_y = 0,0
                circle_x, circle_y = 100, 395
                tagen_skada = True
                kollision = True
                if hearts == 0:
                    gameover = True
            if fiende2_kollision and not tagen_skada:
                hearts -= 1
                circle_speed_x, circle_speed_y = 0,0
                circle_x, circle_y = 100, 395
                tagen_skada = True
                kollision = True
                if hearts == 0:
                    gameover = True   
        if not (fiende_kollisionlv2 or (spik_kollision_NH or (spik_kollision or (spik_kollision_grop or fiende2_kollision)))):
            tagen_skada = False 
            kollision = False
            circle_speed_x = 10
        pygame.draw.polygon(screen, (blood_red), ((740,500), (800,500), (770,415)))  #Spiken nere i höger
        pygame.draw.polygon(screen, (blood_red), ((440,340), (500,340), (470,270)))  #Vänstra gropspiken
        pygame.draw.polygon(screen, (blood_red), ((500,340), (560,340), (530,270)))  #mittersta gropspiken
        pygame.draw.polygon(screen, (blood_red), ((560,340), (620,340), (590,270)))  #Högra gropspiken
        pygame.draw.polygon(screen, (blood_red), ((235,260), (280,260), (255,310)))  #Hängade spiken i slutet
        pygame.draw.polygon(screen, (blood_red), ((430,0), (370,0), (400,160)))      #Takspiken

        obstacle_painter.render(obstacles)
        
        #Kannonen som skjuter raketerna 
        screen.blit(cannon_image,(cannon_x,cannon_y))
        screen.blit(pipe_image_rotated,(cube_x,cube_y))

    #Level 3 starter
    if level == 3 and level_start:

        background_image = pygame.image.load("boss_background.JPG")
        background_image = pygame.transform.scale(background_image, (800, 600))
        level_start = False
        fiende_x, fiende_y = 900,900
        fiende2_x,fiende2_y = 900,900
        if not boss_talk1:
            sound_effects["boss_talk1"].play()
            pygame.mixer.music.stop()
            boss_talk1 = True

    #Level 3
    if level == 3:
        #Platformar
        obj1 = pygame.Rect(120,440,130,20) #Platform nere vänster
        obj2 = pygame.Rect(680,400,100,20) #Platform nere höger
        obj3 = pygame.Rect(300,320,80,20 ) #Över vänster
        obj4 = pygame.Rect(610,100,90,20)  #Uppe höger
        obj5 = pygame.Rect(100,100,90,20)  #Uppe vänster
        obj6 = pygame.Rect(500,220,80,20)  #Näst högst upp höger
        obj7 = pygame.Rect(560,240,40,20)  #Mittersta trappsteget
        obj8 = pygame.Rect(580,260,40,20)  #Mittersta 2 trappsteget
        obj9 = pygame.Rect(600,280,40,20)  #Understa trappsteget
        obstacles = [obj1,obj2,obj3,obj4,obj5,obj6,obj7,obj8,obj9]
        obstacle_painter.render(obstacles)

        if boss_encountered:
            boss_x,boss_y = 550,100

        #Kollar om bossen ska spawna
        if not boss_exist:
            spawn_boss(screen)
            boss_exist = True
            start_ticks = pygame.time.get_ticks()  #Börjar en räkning

        #Räknar ut tiden sen bossen spawnade
        boss_delay = (pygame.time.get_ticks() - start_ticks) / 1000  

        
        if boss_exist and (boss_delay < 7) and (not boss_encountered): 
            spawn_boss(screen)  #Visar bossen men låter den inte röra/attackera
            movment_lock = True
            if boss_encountered and not level3_music:
                play_music(level)
                level3_music = True
        
        elif (boss_exist and boss_delay >= 7) or boss_encountered: 
            #Låter bossen attackera och röra sig efter det bestämda tidsomloppet
            movment_lock, boss_encountered = False, True
            boss_movment(screen, level,boss_exist)
            boss_attack(screen, circle_x, circle_y, circle_radius)
            boss_collision = boss_collaterate(circle_x, circle_y)
            boss_attack_collision = boss_attack(screen, circle_x, circle_y, circle_radius)
            if boss_encountered and not level3_music:
                play_music(level)
                level3_music = True
        
            
            #if (boss_collision or boss_attack_collision) and not tagen_skada:
                
                #tagen_skada = True
                #gameover = True
        
                #boss_x, boss_y = 550, 150  
                #boss_exist = False 
                
        
        screen.blit(proceed_button,(98,70))

    #Level 4
    if level == 4:
        boss_reset = False
        
        #Platformar
        obje1 = pygame.Rect(125,470,100,20)   #Första platform vänster
        obje2 = pygame.Rect(350,100,20,400)   #Mitten vägg  
        obje3 = pygame.Rect(600,300,180,20)   #Målplatform höger
        obje4 = pygame.Rect(125,350,100,20)   #Andra platform vänster
        obje5 = pygame.Rect(125,230,100,20)   #Tredje platform vänster
        obje6 = pygame.Rect(125,115,100,20)   #Fjärde platformen vänster
        obstacles =[obje1,obje2,obje3,obje4,obje5,obje6]
        obstacle_painter.render(obstacles)

        if not boss_talk2:
            sound_effects["boss_take_dmg"].play()
        
        
        spawn_boss(screen), boss_movment(screen, level,boss_exist), boss_attack(screen,circle_x,circle_y,circle_radius)
        boss_collision = boss_collaterate(circle_x, circle_y)
        boss_attack_collision = boss_attack(screen,circle_x,circle_y,circle_radius)
        #if boss_collision or boss_attack_collision and not tagen_skada:
            #tagen_skada = True
           # gameover = True
        
        screen.blit(proceed_button,(750,270))

    #Level 5
    if level == 5:
        #Platformar
        objek1 = pygame.Rect(100,480,30,20) #Vänster sida, nerifrån och upp
        objek2 = pygame.Rect(300,350,30,20)
        objek3 = pygame.Rect(90,240,30,20)
        objek4 = pygame.Rect(270,115,30,20)
        
        objek5 = pygame.Rect(705,475,30,20) #Höger sida nerifrån och upp
        objek6 = pygame.Rect(570,340,30,20)
        objek7 = pygame.Rect(600,220,30,20)
        objek8 = pygame.Rect(705,110,30,20)
        objek9 = pygame.Rect(770,380,30,20)

        objek10 = pygame.Rect(370,350,100,20) #Mitten
        objek11 = pygame.Rect(350,100,20,250)
        objek12 = pygame.Rect(470,100,20,250)
        objek13 = pygame.Rect(470,350,5,5)
        objek14 = pygame.Rect(360,350,5,5)
        obstacles=[objek1,objek2,objek3,objek4,objek5,objek6,objek7,objek8,objek9,objek10,objek11,objek12,objek13,objek14]
        obstacle_painter.render(obstacles)

        spawn_boss(screen), boss_movment(screen, level,boss_exist), boss_attack(screen,circle_x,circle_y,circle_radius)
        boss_collision = boss_collaterate(circle_x, circle_y)
        boss_attack_collision = boss_attack(screen,circle_x,circle_y,circle_radius)
        #if boss_collision or boss_attack_collision and not tagen_skada:
            #tagen_skada = True
            #gameover = True

        screen.blit(proceed_button,(400,320))
        
        
    #"Animation" för mario
    if not movment and on_ground:#Om spelaren står stilla
        screen.blit(mario_still,(circle_x-(circle_radius -2),circle_y-(circle_radius +3)))
    
    if movment_groundpound:
        screen.blit(mario_groundpound,(circle_x-(circle_radius +28),circle_y-(circle_radius +5))) 
    elif movment_right and not on_ground: #Om spelaren hoppar till höger
        screen.blit(mario_jumping_right,(circle_x-(circle_radius -2),circle_y-(circle_radius +3)))
        
    elif movment_left and not on_ground: #Om spelaren hopper til vänster
        screen.blit(mario_jumping_left,(circle_x-(circle_radius -2),circle_y-(circle_radius +3)))
        
    elif not on_ground: #Om spelare bara är i luften
       screen.blit(mario_jumping_right,(circle_x-(circle_radius -2),circle_y-(circle_radius +3)))
    elif movment_right and on_ground:  #Om spelaren springer till höger 
        screen.blit(mario_running_right,(circle_x-(circle_radius -2),circle_y-(circle_radius +3)))
    elif movment_left and on_ground:   #Om spelaren springer till vänster
        screen.blit(mario_running_left,(circle_x-(circle_radius -2),circle_y-(circle_radius +3))) 
    if on_ground or onplatform:
        jumping = False
    
    
    #Kollision
    circle_rect = pygame.Rect(circle_x - circle_radius, circle_y - circle_radius, circle_radius * 2, circle_radius * 2)
    
    onplatform = False
    
    for obstacle in obstacles: #ger möjdlighet med olika hinder varje nivå
        if circle_rect.colliderect(obstacle):
            
            # över platformen
            if circle_y + circle_radius >= obstacle.top and circle_y <= obstacle.top:
                circle_speed_y = 0
                onplatform = True
                on_ground = True
                doublejump = True
                if circle_y + circle_radius > obstacle.top + 5 and circle_y < obstacle.top +5: #temporärt fixar bugg med att man hamnar i platformen
                    circle_y -= 10
                
            # vänster om platform
            elif circle_x + circle_radius > obstacle.left and circle_x < obstacle.left:
                circle_x = obstacle.left - circle_radius   
            #höger om platform
            elif circle_x - circle_radius < obstacle.right and circle_x > obstacle.right:
                circle_x = obstacle.right + circle_radius
            #under
            elif circle_y - circle_radius < obstacle.bottom and circle_y > obstacle.bottom:
                circle_y = obstacle.bottom + circle_radius
                circle_speed_y = max(circle_speed_y, 5)  
        if not onplatform:
            onplatform = False

    

    pygame.display.flip()
    pygame.time.delay(25)
