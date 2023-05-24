# Project: Emil's epic space shooter
# Description: Super epic shooter game, totaly not a ripoff of space invaders.
# Author: Håkan the incredibly handsome
# Date: 1870-3-14
# Version: 0.234243
# ----------------------------------------------------------------------------

# IMPORTS
import os
import random
import pygame
from pygame import mixer
from webscrape import webbscrape as wb

# 
pygame.font.init()

# GAME WINDOW
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Emil's epic space shooter")

# INFOGA BILDER
RED_SPACE_SHIP = pygame.image.load(os.path.join("enemy1.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("enemy2.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("enemy3.png"))

# SPELARE
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("player.png"))

# PROJEKTIL
RED_LASER = pygame.image.load(os.path.join("redlaser.png"))
GREEN_LASER = pygame.image.load(os.path.join("greenlaser.png"))
BLUE_LASER = pygame.image.load(os.path.join("bluelaser.png"))
YELLOW_LASER = pygame.image.load(os.path.join("bullet.png"))

# BACKGROUND
BG = pygame.transform.scale(pygame.image.load(os.path.join("bg.png")), (WIDTH, HEIGHT))

# LAZER CLASS
class Laser:
    """
    Laser class
    
    :param x: x coordinate
    :param y: y coordinate
    :param img: image
    
    :type x: int
    :type y: int
    :type img: pygame.image
    
    :return: None
    :rtype: None
    
    """

    # INIT LASER CLASS
    def __init__(self, x, y, img):
        """ Laser class
        
        :param x: x coordinate
        :param y: y coordinate
        :param img: image
        
        :type x: int
        :type y: int
        :type img: pygame.image
        
        :return: None
        :rtype: None
        """
        # self.x = x
        # self.y = y
        # self.img = img
        # self.mask = pygame.mask.from_surface(self.img)

        self.x = x  # Adjust x position to the middle of the player
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    # DRAW LASER
    def draw(self, window):
        """ Draw laser
        
        :param window: window
        
        :type window: pygame.display
        
        :return: None
        :rtype: None
        """
        window.blit(self.img, (self.x, self.y))

    # MOVE LASER
    def move(self, vel):
        """ Move laser
        
        :param vel: velocity
        
        :type vel: int
        
        :return: None
        :rtype: None"""
        self.y += vel

    # CHECKS IF LASER IS OFF SCREEN
    def off_screen(self, height):
        """ Check if laser is off screen
        
        :param height: height
        
        :type height: int
        
        :return: True or False
        :rtype: bool
        """
        return not(self.y <= height and self.y >= 0)

    # CHECKS IF LASER COLLIDES WITH OBJECT
    def collision(self, obj):
        """ Check if laser collides with object
        
        :param obj: object
        
        :type obj: pygame.image
        
        :return: True or False
        :rtype: bool
        """
        return collide(self, obj)

# SHIP CLASS (BASE CLASS). ALL SHIPS INHERIT FROM THIS CLASS.
class Ship:
    """ Ship class 
    
    :param x: x coordinate
    :param y: y coordinate
    :param health: health
    
    :type x: int
    :type y: int
    :type health: int
    
    :return: None
    :rtype: None
    """
    # FIRE COOLDOWN
    COOLDOWN = 20

    # INIT SHIP CLASS. 
    def __init__(self, x, y, health=100):
        """ Ship class 
        
        :param x: x coordinate
        :param y: y coordinate
        :param health: health
        
        :type x: int
        :type y: int
        :type health: int
        
        :return: None
        :rtype: None
        """
        # SET SHIP POSITION AND HEALTH.
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0 

    # DRAW SHIP
    def draw(self, window):
        """ Draw ship
        
        :param window: window
        
        :type window: pygame.display
        
        :return: None
        :rtype: None
        """
        # DRAW SHIP IMAGE ON SCREEN
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    # MOVES LAZER. REMOVES LAZER IF IT IS OFF SCREEN. 
    def move_lasers(self, vel, obj):
        """ Move lasers
        
        :param vel: velocity
        :param obj: object
        
        :type vel: int
        :type obj: object
        
        :return: None
        :rtype: None
        """
        # MOVE LASER AND REMOVE LASER IF IT IS OFF SCREEN
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 5
                self.lasers.remove(laser)

    # COOLDOWN BETWEEN SHOTS 
    def cooldown(self):
        """ Cooldown
        
        :return: None
        :rtype: None
        """
        # COOLDOWN BETWEEN SHOTS
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    # SHOOT LAZER
    def shoot(self):
        """ Shoot
        
        :return: None
        :rtype: None
        """
        # SHOOT LASER
        if self.cool_down_counter == 0:
            laser = Laser(self.x+self.get_width()/2, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    # GET WIDTH OF SHIP    
    def get_width(self):
        """ Get width
        
        :return: width
        :rtype: int
        """
        # GET WIDTH OF SHIP
        return self.ship_img.get_width()

    # GET HEIGHT OF SHIP
    def get_height(self):
        """ Get height
        
        :return: height
        :rtype: int
        """
        # GET HEIGHT OF SHIP
        return self.ship_img.get_height()

# SPELARE SHIP
class Player(Ship):
    """ Player class
    
    :param x: x coordinate
    :param y: y coordinate
    :param health: health
    
    :type x: int
    :type y: int
    :type health: int
    
    :return: None
    :rtype: None
    """
    # INIT PLAYER CLASS
    def __init__(self, x, y, health=100):
        """ Player class
        
        :param x: x coordinate
        :param y: y coordinate
        :param health: health
        
        :type x: int
        :type y: int
        :type health: int
        
        :return: None
        :rtype: None
        """
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP # PLAYER SHIP IMAGE
        self.laser_img = YELLOW_LASER # PLAYER LASER IMAGE
        self.mask = pygame.mask.from_surface(self.ship_img) # PLAYER MASK
        self.max_health = health # PLAYER MAX HEALTH

    # HOW LAZER MOVES
    def move_lasers(self, vel, objs):
        """ Move lasers
        
        :param vel: velocity
        :param objs: objects
        
        :type vel: int
        :type objs: object
        
        :return: None
        :rtype: None
        """
        # MOVE LASER AND REMOVE LASER IF IT IS OFF SCREEN. 
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            
            # CHECK IF LASER COLLIDES WITH ENEMY. IF IT DOES, REMOVE LASER AND ENEMY.
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    # DRAW PLAYER
    def draw(self, window):
        """ Draw player

        :param window: window

        :type window: pygame.display

        :return: None
        :rtype: None
        """
        # DRAW PLAYER
        super().draw(window)
        self.healthbar(window)

    # PLAYER HEALTHBAR
    def healthbar(self, window):
        """ Healthbar
        
        :param window: window
        
        :type window: pygame.display
        
        :return: None
        :rtype: None
        """
        # PLAYER HEALTHBAR
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

# ENEMY SHIP CLASS. 
class Enemy(Ship):
    """ Enemy class
    
    :param x: x coordinate
    :param y: y coordinate
    :param color: color
    :param health: health
    
    :type x: int
    :type y: int
    :type color: str
    :type health: int
    
    :return: None
    :rtype: None
    """
    # COLOR MAP FOR ENEMY SHIP AND LASER.
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
                }

    # INIT ENEMY CLASS
    def __init__(self, x, y, color, health=100):
        """ Enemy class
        
        :param x: x coordinate
        :param y: y coordinate
        :param color: color
        :param health: health
        
        :type x: int
        :type y: int
        :type color: str
        :type health: int
        
        :return: None
        :rtype: None
        """
        # MASK FOR ENEMY SHIP AND LASER COLOR MAP.
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    # MOVE ENEMY SHIP
    def move(self, vel):
        """ Move enemy ship
        
        :param vel: velocity
        
        :type vel: int
        
        :return: None
        :rtype: None
        """
        self.y += vel

    # SHOOT LASER
    def shoot(self):
        """ Shoot
        
        :return: None
        :rtype: None
        
        """
        # SHOOT LAZER. LAZER COOLDOWN. LAZER 
        if self.cool_down_counter == 0:
            laser = Laser(self.x+self.get_width()/2, self.y+self.get_height()-2, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

# SKAPAR EN MASK PÅ OBJEKT OCH KOLLAR FÖR KOLLISION
def collide(obj1, obj2):
    """ Collide 
    
    :param obj1: object 1
    :param obj2: object 2
    
    :type obj1: object
    :type obj2: object
    
    :return: None
    :rtype: None
    """

    # OFFSET X AND Y FOR COLLISION DETECTION
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

# MAIN
def main():
    """ Main
    
    :return: None
    :rtype: None
    """

    # RUN = TRUE
    run = True

    # FPS
    FPS = 60

    # CURRENT LEVEL
    level = 0

    # STARTING AMOUNT OF LIVES
    lives = 5
    
    # MAIN FONT
    main_font = pygame.font.SysFont("comicsans", 50)

    # LOST FONT
    lost_font = pygame.font.SysFont("comicsans", 60)

    # ENEMIES LIST 
    enemies = []

    # LENGTH OF WAVE
    wave_length = 5

    # ENEMY VELOCITY
    enemy_vel = 1

    # PLAYER VELOCITY
    player_vel = 5

    # LAZER VELOCITY
    laser_vel = 5

    # PLAYER SPAWN POSITION
    player = Player(300, 630)
   
    # CLOCK
    clock = pygame.time.Clock()

    # LOST = FALSE
    lost = False

    # LOST COUNT
    lost_count = 0

    # REDRAW WINDOW
    def redraw_window():
        """ Redraw window
        
        :return: None
        :rtype: None
        """
        # DRAW BACKGROUND
        WIN.blit(BG, (0,0))

        # DRAW TEXT, LIVES AND LEVEL
        lives_label = main_font.render(f"LIVES: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"LEVEL: {level}", 1, (255,255,255))

        # DRAW LIVES AND LEVEL ON SCREEN
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        # DRAW ENEMIES
        for enemy in enemies:
            enemy.draw(WIN)

        # DRAW PLAYER
        player.draw(WIN)

        # DRAW LOST LABEL
        if lost:
            lost_label = lost_font.render("Du dog!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        # UPDATE DISPLAY
        pygame.display.update()

    # MAIN LOOP
    while run:
        # GAME RUNS AT 60 FPS
        clock.tick(FPS)
        redraw_window()
        
        # LOST IF OUT OF LIVES
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        # QUIT GAME
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        # LEVEL SYSTEM. ADDS MORE ENEMIES THE HIGHER THE LEVEL.
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        # QUIT GAME IF PLAYER CLICKS X
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # PLAYER MOVEMENT AND SHOOTING
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:  # LEFT
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # RIGHT
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # UP
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # DOWN
            player.y += player_vel

        if keys[pygame.K_SPACE]:
            player.shoot()
        
        # webbscrape
        if keys[pygame.K_l]:
            wb()

        # LAZER MOVEMENT
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            # RANDOM SHOOTING
            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            # PLAYER TAKES DAMAGE IF HIT BY ENEMY LASER, -1 LIFE IF ENEMY GOES BELOW THE SCREEN
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        # PLAYER LASER MOVEMENT
        player.move_lasers(-laser_vel, enemies)

# MAIN MENU 
def main_menu():
    """ Main menu
    
    :return: None
    :rtype: None
    """
    # FONT AND SIZE
    title_font = pygame.font.SysFont("comicsans", 50)

    # MAIN LOOP 
    run = True 
    while run:
        # DRAW BACKGROUND
        WIN.blit(BG, (0,0)) 

        # DRAW TITLE
        title_label = title_font.render("KLICK TO START!", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))

        # UPDATE DISPLAY
        pygame.display.update()

        # QUIT GAME IF PLAYER CLICKS X
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    # QUIT GAME
    pygame.quit()
    
# MAIN MENU
main_menu()
