import pygame
from sys import exit
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__(self)
        self.image = pygame.image.load('maincharacter/2 Punk/Punk_idle.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (80,350))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 350:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 350:
            self.rect.bottom = 350

    def animation_state(self):
        if self.rect.bottom < 350:
            self.image = self.idle
        
        else:
            self.player_input += 0.1
            if self.player_index >= len(self.player_idle):self.player_index = 0
            self.image = self.player_idle

    def update(self):
        self.player_input()
        self.apply_gravity()

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 4

            if obstacle_rect.bottom == 350:
                screen.blit(skeleton_surface,obstacle_rect)
            else:
                screen.blit(demon_surf,obstacle_rect)

            #screen.blit(skeleton_surface,obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Game Project')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/VerminVibesV-Zlg3.ttf', 50)

player = pygame.sprite.GroupSingle()
player.add(Player())

skyline_surface = pygame.image.load('graphics/skyline.jpg').convert()
skyline_surface = pygame.transform.scale(skyline_surface, (800, 350))
ground_surface = pygame.image.load('graphics/Ground.png').convert()
ground_surface = pygame.transform.scale(ground_surface, (800,50))
text_surface = test_font.render('My Game', False, 'Yellow')
game_active = True

#Obstacles
skeleton_surface = pygame.image.load('enemies/Skeleton/GIFS/Skeleton Walk.gif').convert_alpha()
skeleton_surface = pygame.transform.scale(skeleton_surface,(50,50))
skeleton_surface = pygame.transform.flip(skeleton_surface,True,False)


demon_surf = pygame.image.load('enemies/NightBorne/NightBorne_idle.gif').convert_alpha()
#demon_surf = pygame.transform.scale(demon_surf,(75,75))

obstacle_rect_list = []

player_surface = pygame.image.load('maincharacter/2 Punk/Punk_idle.png').convert_alpha()
player_surface = pygame.transform.scale(player_surface,(400,100))
player_rect = player_surface.get_rect(midbottom = (80,350))
player_gravity = 0

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 350:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                

        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(skeleton_surface.get_rect(midbottom = (randint(900,1100),350)))
            else:
                obstacle_rect_list.append(demon_surf.get_rect(midbottom = (randint(900,1100),300)))


    if game_active:
        screen.blit(skyline_surface,(0,0))
        screen.blit(ground_surface,(0,350))
        screen.blit(text_surface,(275,50))
        
        #screen.blit(skeleton_surface,skeleton_rect)
        #skeleton_rect.x -= 2
        #if skeleton_rect.right <= 0: skeleton_rect.left = 800
        
        #Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 350: player_rect.bottom = 350
        screen.blit(player_surface,player_rect)
        player.draw(screen)
        player.update()

        #Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #Collision
        game_active = collisions(player_rect,obstacle_rect_list)
        #if skeleton_rect.colliderect(player_rect):
            #game_active = False
    else:
        screen.fill('Yellow')
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,350)
        player_gravity = 0

    pygame.display.update()
    clock.tick(60)