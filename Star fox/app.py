import pygame
import os
pygame.mixer.init()
pygame.font.init()

HEALTH_FONT = pygame.font.SysFont('arial', 40)
winner_font = pygame.font.SysFont('arial', 100)

WIDTH, HEIGHT = 800, 500
wallc = pygame.Rect(WIDTH/2 - 4, 0, 8, 500)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Spaceship 1v1')

FPS = 60

GUN1_HIT = pygame.USEREVENT + 1
GUN2_HIT = pygame.USEREVENT + 2

Gun1picture = pygame.image.load(
    os.path.join('Assets', 'spaceship1.png'))
Gun1 = pygame.transform.scale(Gun1picture, (517/10, 353/10))
Gun2picture = pygame.image.load(
    os.path.join('Assets', 'spaceship.png'))
Gun2 = (pygame.transform.scale(Gun2picture, (517/10, 353/10)))
background = pygame.image.load(os.path.join('Assets', 'starfox background.jpg'))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

fire_noise = pygame.mixer.Sound(os.path.join('Assets', 'Starfox_shoot.mp3'))
hurt_noise = pygame.mixer.Sound(os.path.join('Assets', 'Star fox hit noise.mp3'))

def gun1_movement(key, gun1):
    if key[pygame.K_w] and gun1.y > 0:  # up
        gun1.y -= 4
    if key[pygame.K_a] and gun1.x > 0:  # left
        gun1.x -= 4
    if key[pygame.K_s] and gun1.y + 35.3 < HEIGHT:  # down
        gun1.y += 4
    if key[pygame.K_d] and gun1.x + 51.7 < 396:  # right
        gun1.x += 4
    if key[pygame.K_m]:  # angle?
        pass


def gun2_movement(key, gun2):
    if key[pygame.K_UP] and gun2.y > 0:  # up
        gun2.y -= 4
    if key[pygame.K_LEFT] and gun2.x > WIDTH/2 + 4:  # left
        gun2.x -= 4
    if key[pygame.K_DOWN] and gun2.y + 35.3 < HEIGHT:  # down
        gun2.y += 4
    if key[pygame.K_RIGHT] and gun2.x + 51.7 < 800:  # right
        gun2.x += 4
    if key[pygame.K_n]:  # angle?
        pass


def draw_winner(text):
    drawText = winner_font.render(text, 1, (255, 255, 255))
    WIN.blit(drawText, (400 - drawText.get_width()/2, 250 - drawText.get_width()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def draw_window(gun1, gun2, pler1_bull, pler2_bull, gun2_health, gun1_health, HEALTH_FONT):
    WIN.fill((0, 0, 0))
    WIN.blit(background, (0, 0))
    pygame.draw.rect(WIN, (0, 0, 0), wallc)
    for bull in pler1_bull:
        pygame.draw.rect(WIN, (0, 0, 255), bull)
    for bull in pler2_bull:
        pygame.draw.rect(WIN, (255, 7, 61), bull)
    WIN.blit(Gun1, (gun1.x, gun1.y))
    WIN.blit(Gun2, (gun2.x, gun2.y))
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(gun2_health), 1, (255, 255, 255))
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(gun1_health), 1, (255, 255, 255))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    pygame.display.update()


def bull_flight(pler1_bull, pler2_bull, gun1, gun2):
    for bull in pler1_bull:
        bull.x += 7
        if gun2.colliderect(bull):
            pygame.event.post((pygame.event.Event(GUN2_HIT)))
            pler1_bull.remove(bull)
        elif bull.x > 800:
            pler1_bull.remove(bull)
    for bull in pler2_bull:
        bull.x -= 7
        if gun1.colliderect(bull):
            pygame.event.post((pygame.event.Event(GUN1_HIT)))
            pler2_bull.remove(bull)
        elif bull.x < 0:
            pler2_bull.remove(bull)


def main():
    gun1 = pygame.Rect(200, 250, 40, 30)
    gun2 = pygame.Rect(600, 250, 517/3, 30)
    pler1_bull = []
    pler2_bull = []
    gun1_health = 5
    gun2_health = 5
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and len(pler1_bull) < 4:
                    bull = pygame.Rect(gun1.x + (184.642857143 * 0.1), gun1.y + 15, 10, 5)
                    pler1_bull.append(bull)
                    fire_noise.play()
                if event.key == pygame.K_SLASH and len(pler2_bull) < 4:
                    bull = pygame.Rect(gun2.x, gun2.y + 15, 10, 5)
                    pler2_bull.append(bull)
                    fire_noise.play()
            if event.type == GUN2_HIT:
                gun2_health -= 1
                hurt_noise.play()
            if event.type == GUN1_HIT:
                gun1_health -= 1
                hurt_noise.play()
        winner_txt = ""
        if gun1_health <= 0:
            winner_txt = "Star wolf wins"
        if gun2_health <= 0:
            winner_txt = "Star fox wins"
        if winner_txt != "":
            draw_winner(winner_txt)
            break
        draw_window(gun1, gun2, pler1_bull, pler2_bull, gun2_health, gun1_health, HEALTH_FONT)
        bull_flight(pler1_bull, pler2_bull, gun1, gun2)
        key = pygame.key.get_pressed()
        gun1_movement(key, gun1)
        gun2_movement(key, gun2)
    main()


if __name__ == "__main__":
    main()
