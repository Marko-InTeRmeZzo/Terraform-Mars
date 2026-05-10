
import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Terraform Mars")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)

# ЗАВАНТАЖЕННЯ

bg = pygame.image.load("assets/mars2.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

rover_img = pygame.image.load("assets/rover4.png")
rover_img = pygame.transform.scale(rover_img, (60, 60))

sat_img = pygame.image.load("assets/satellite.png")
sat_img = pygame.transform.scale(sat_img, (50, 50))

plant_img = pygame.image.load("assets/plants.png")
plant_img = pygame.transform.scale(plant_img, (40, 40))

ice_img = pygame.image.load("assets/ice.png")
ice_img = pygame.transform.scale(ice_img, (50, 50))

# СТАН ГРИ

MENU = 0
PLAY = 1
WIN = 2
state = MENU

# ГРАВЕЦЬ

rover = pygame.Rect(600, 350, 60, 60)
speed = 6

# ДАНІ ПЛАНЕТИ

ore = 0
oxygen = 0
water = 0
satellites = []
plants = []
resources = []

for i in range(12):
    resources.append(pygame.Rect(random.randint(100, 1100), random.randint(100, 600), 50, 50))

# ПИЛОВА БУРЯ

storm_timer = 0
storm = False

# MENU

def draw_menu():
    screen.fill((20, 20, 20))
    title = font.render("TERAFORM MARS", True, (255, 200, 50))
    start = font.render("Press ENTER to start", True, (255, 255, 255))

    screen.blit(title, (WIDTH//2 - 120, HEIGHT//2 - 60))
    screen.blit(start, (WIDTH//2 - 140, HEIGHT//2))

# GAME

def draw_game():
    global oxygen, water

    screen.blit(bg, (0, 0))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]: rover.y -= speed
    if keys[pygame.K_s]: rover.y += speed
    if keys[pygame.K_a]: rover.x -= speed
    if keys[pygame.K_d]: rover.x += speed

    # ресурси
    for r in resources[:]:
        pygame.draw.rect(screen, (200, 180, 120), r)

        if rover.colliderect(r):
            resources.remove(r)
            global ore
            ore += 1

    # посадка рослин
    if keys[pygame.K_1] and ore >= 2:
        plants.append(rover.copy())
        oxygen += 1
        ore -= 2

    # супутник
    if keys[pygame.K_2] and ore >= 5:
        satellites.append([random.randint(0, WIDTH), 100])
        water += 2
        ore -= 5

    # малювання
    screen.blit(rover_img, rover)

    for p in plants:
        screen.blit(plant_img, p)

    for s in satellites:
        screen.blit(sat_img, s)

    # UI
    ui = font.render(f"Ore:{ore} Oxygen:{oxygen} Water:{water}", True, (255,255,255))
    screen.blit(ui, (20, 20))

    # перемога
    if oxygen >= 20 and water >= 20:
        global state
        state = WIN

# WIN SCREEN

def draw_win():
    screen.fill((10, 100, 50))
    text = font.render("MARS IS HABITABLE!", True, (255,255,255))
    screen.blit(text, (WIDTH//2 - 160, HEIGHT//2))

# LOOP

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if state == MENU and event.key == pygame.K_RETURN:
                state = PLAY

    if state == MENU:
        draw_menu()
    elif state == PLAY:
        draw_game()
    elif state == WIN:
        draw_win()

    pygame.display.update()

pygame.quit()
