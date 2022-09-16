import pygame
import os
pygame.font.init()
pygame.mixer.init()

width, height = 900, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Welcome to the Game!")

fps = 60
VEL = 5
boarder = pygame.Rect(width//2 -5,0, 10, height)
space_width, space_height = 55, 40
white = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Yellow = (255, 255, 0)
bullet_vel = 7
max_bullets = 3

bullet_hit_sound = pygame.mixer.Sound(os.path.join('Images_songs', 'Grenade.mp3'))
bullet_fire_sound = pygame.mixer.Sound(os.path.join('Images_songs', 'Gun+silencer.mp3'))

player1_hit = pygame.USEREVENT + 1
player2_hit = pygame.USEREVENT + 2


health_font = pygame.font.SysFont('comicsans', 40)
winner_font = pygame.font.SysFont('comicsans', 100)


spaceship1_image = pygame.image.load(os.path.join('Images_songs', 'spaceship1.png'))
image1 = pygame.transform.rotate(pygame.transform.scale(spaceship1_image, (space_width, space_height)), -90)

spaceship2_image = pygame.image.load(os.path.join('Images_songs', 'spaceship2.png'))
image2 = pygame.transform.rotate(pygame.transform.scale(spaceship2_image, (space_width, space_height)), 90)

space = pygame.transform.scale(pygame.image.load(os.path.join('Images_songs', 'space.png')), (width, height))


def draw_design(player1, player2, player1_bullets, player2_bullets, player1_health, player2_health):
    win.blit(space, (0, 0))
    pygame.draw.rect(win,Black, boarder)


    player1_health_text = health_font.render("Health: " + str(player1_health), 1, white)
    player2_health_text = health_font.render("Health: " + str(player2_health), 1, white)
    win.blit(player1_health_text, (10, 10))
    win.blit(player2_health_text, (width - player2_health_text.get_width() - 10, 10))
    win.blit(image1, (player1.x, player1.y))
    win.blit(image2, (player2.x, player2.y))



    for bullet in player2_bullets:
        pygame.draw.rect(win, Red, bullet)
    
    for bullet in player1_bullets:
        pygame.draw.rect(win, Yellow, bullet)
    pygame.display.update()

def player1_handle_movement(keys_pressed, player1):
    if keys_pressed[pygame.K_a] and player1.x - VEL > 0: # Left
            player1.x -= VEL
    if keys_pressed[pygame.K_d] and player1.x + VEL + player1.width < boarder.x: # right
            player1.x += VEL
    if keys_pressed[pygame.K_w] and player1.y - VEL > 0: # up
            player1.y -= VEL
    if keys_pressed[pygame.K_s] and player1.y + VEL + player1.height < height - 15: # up
            player1.y += VEL



def player2_handle_movement(keys_pressed, player2):
    if keys_pressed[pygame.K_a] and player2.x - VEL > boarder.x + boarder.width: # Left
            player2.x -= VEL
    if keys_pressed[pygame.K_d] and player2.x + VEL + player2.width < boarder.x: # right
            player2.x += VEL
    if keys_pressed[pygame.K_w] and player2.y - VEL > 0: # up
            player2.y -= VEL
    if keys_pressed[pygame.K_s] and player2.y + VEL + player2.height < height - 15: # up
            player2.y += VEL

def handle_bullets(player1_bullets, player2_bullets, player1, player2):
    for bullet in player1_bullets:
        bullet.x += bullet_vel
        if player2.colliderect(bullet):
            pygame.event.post(pygame.event.Event(player2_hit))
            player1_bullets.remove(bullet)
        if bullet.x > width:
            player1.remove(bullet)
        elif bullet.x < 0:
            player2.remove(bullet)
    

    for bullet in player2_bullets:
        bullet.x -= bullet_vel
        if player1.colliderect(bullet):
            pygame.event.post(pygame.event.Event(player2_hit))
            player2_bullets.remove(bullet)

def draw_winner(text):
    draw_text = winner_font.render(text, 1, white)
    win.blit(draw_text, (width/2 - draw_text.get_width()/2, height/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    player1 = pygame.Rect(100, 300, space_width, space_height)
    player2 = pygame.Rect(700, 300, space_width, space_height)

    player1_bullets = []
    player2_bullets = []

    player1_health = 10
    player2_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(player1_bullets ) < max_bullets:
                    bullet = pygame.Rect(player1.x + player1.width, player1.y + player1.height//2 - 2, 10, 5)
                    player1_bullets.append(bullet)
                    bullet_fire_sound.play()
                
                if event.key == pygame.K_RCTRL and len(player2_bullets) < max_bullets:
                     bullet = pygame.Rect( player2.x, player2.y + player2.height//2 - 2, 10, 5)
                     player2_bullets.append(bullet)
                     bullet_fire_sound.play()

            if event.type == player2_hit:
                player2_health -= 1
                bullet_hit_sound.play()


            if event.type == player1_hit:
                player1_health -= 1
                bullet_hit_sound.play()

        winner_text = ""
        if player2_health <= 0:
            winner_text = "Player 1 Wins!"
        
        if player1_health <= 0:
            winner_text = "Player 2 Wins!"
        
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        player1_handle_movement(keys_pressed, player1)
        player2_handle_movement(keys_pressed, player2)
        
        

        handle_bullets(player1_bullets, player2_bullets, player1, player2)
        draw_design(player1, player2, player1_bullets, player2_bullets, player1_health, player2_health)
    main()
    

if __name__ == "__main__":
    main()
