import pygame
import random

pygame.init()

# window
screen = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Pong v1.7.1")

running = True
# points
Lscore = 0
Rscore = 0

score_font = pygame.font.SysFont(None, 60)

# paddle positions
paddleLEFT_y = 250
paddleRIGHT_y = 250

# Ball
ball_x = 500
ball_y = 350
ball_coords = ball_x, ball_y

ball_moving = False

ball_was_hit = False

ball_size = 5

ball_speed_y = 180
ball_speed_x = 180
ball_speed = 180
ball_speed_increase = 10

# ---
clock = pygame.time.Clock()

playerlost = "left"

# paddle pre-flight
paddle_flying = False
paddleLEFT_x = 10
paddle_flight_speed = 350
paddle_flight_speed2 = 400

# paddle speed
paddle_speed = 235

# loop
while running:

    keys = pygame.key.get_pressed()
    # fps limit
    dt = clock.tick(30) / 1000
        
    if not keys[pygame.K_h]:

### BALL ###
        if ball_moving == True:
            ball_y = ball_y + ball_speed_y * dt
            ball_x = ball_x + ball_speed_x * dt

            if ball_y >= 685:
                ball_speed_y = -abs(ball_speed_y)
            if ball_y <= 5:
                ball_speed_y = abs(ball_speed_y)

        # ball reset left
        if ball_x < -10:
            ball_x = 500
            ball_y = 350
            ball_speed_y = 0
            ball_speed_x = 0
            ball_moving = False
            playerlost = "left"
            Rscore += 1
            ball_speed += ball_speed_increase
        
        # ball reset right
        if ball_x > 1010:
            ball_x = 500
            ball_y = 350
            ball_speed_y = 0
            ball_speed_x = 0
            ball_moving = False
            playerlost = "right"
            Lscore += 1
            ball_speed += ball_speed_increase

        # ball coords definition
        ball_coords = ball_x, ball_y
### PADDLE FLYING ###

        # paddle flying key
        if keys[pygame.K_LGUI]:
            paddle_flying = True

        # paddle flying motion
        if paddle_flying:
            paddleLEFT_x = paddleLEFT_x + paddle_flight_speed * dt
            paddleLEFT_y = paddleLEFT_y + paddle_flight_speed2 * dt

        if paddleLEFT_x > 1500:
            paddle_flying = False

        # paddle flying y bounce
        if paddle_flying:
        
            if paddleLEFT_y <= 0:
                paddle_flight_speed2 = -paddle_flight_speed2

            if paddleLEFT_y >= 600:
                paddle_flight_speed2 = -paddle_flight_speed2

### PADDLE STEERING L+R ###

        # left paddle border
        if not paddle_flying:
        
            if paddleLEFT_y >= 590:
                paddleLEFT_y = 590

            if paddleLEFT_y <= 10:
                paddleLEFT_y = 10
        
        # right paddle border
        if paddleRIGHT_y >= 590:
            paddleRIGHT_y = 590
    
        if paddleRIGHT_y <= 10:
            paddleRIGHT_y = 10
        # left paddle
        if keys[pygame.K_s]:
            paddleLEFT_y = paddleLEFT_y + paddle_speed * dt

        if keys[pygame.K_w]:
            paddleLEFT_y = paddleLEFT_y - paddle_speed * dt

        # right paddle
        if keys[pygame.K_DOWN]:
            paddleRIGHT_y = paddleRIGHT_y + paddle_speed * dt

        if keys[pygame.K_UP]:
            paddleRIGHT_y = paddleRIGHT_y - paddle_speed * dt

### HITBOXES ###
        paddleLEFT_hitbox = pygame.Rect(
            paddleLEFT_x,
            paddleLEFT_y,
            7.5,
            75
        )

        paddleRIGHT_hitbox = pygame.Rect(
            980,
            paddleRIGHT_y,
            7.5,
            75
        )

        ball_hitbox = pygame.Rect(
            ball_x - 7,
            ball_y - 7,
            14,
            14
        )

        # hitboxes collision
        if paddleLEFT_hitbox.colliderect(ball_hitbox):
            ball_speed_x = abs(ball_speed_x)

        if paddleRIGHT_hitbox.colliderect(ball_hitbox):
            ball_speed_x = -abs(ball_speed_x)

        if (
            paddleLEFT_hitbox.colliderect(ball_hitbox)
            or paddleRIGHT_hitbox.colliderect(ball_hitbox)
        ) and not ball_was_hit:
            ball_speed_y = random.choice([-ball_speed, ball_speed])
            ball_was_hit = True
        
### DRAWING ###

    screen.fill((0, 0, 0))

    # score
    Lscore_text = score_font.render(str(Lscore), True, (255, 255, 255))
    Rscore_text = score_font.render(str(Rscore), True, (255, 255, 255))

    screen.blit(Lscore_text, (450, 20))
    screen.blit(Rscore_text, (520, 20))

    # line
    for y in range(0, 700, 13):
        pygame.draw.line(
        screen,
        (255, 255, 255),
        (500, y),
        (500, y + 10),
        1
    )

    # paddles
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (paddleLEFT_x, paddleLEFT_y, 7.5, 75)
    )

    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (980, paddleRIGHT_y, 7.5, 75)
    )

# ball
    pygame.draw.circle(
        screen,
        (255, 255, 255),
        (ball_coords),
        ball_size
    )
    
# hitbox.draw.debug (key: h)
    if keys[pygame.K_h]:

        pygame.draw.rect(
            screen,
            (255, 0, 0),
            paddleLEFT_hitbox, 2
            )

        pygame.draw.rect(
            screen,
            (25, 200, 25),
            paddleRIGHT_hitbox, 2
            )
        
        pygame.draw.rect(
            screen,
            (255, 165, 0),
            ball_hitbox, 2
            )
    
    # quit-function
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ### BALL RESET ###

    # ball start L
        if playerlost == "left":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not ball_moving:
                    ball_moving = True
                    ball_speed_x = -ball_speed
                    ball_speed_y = 0
                    playerlost = None
                    ball_was_hit = False
                    ball_speed += 10
                    
    # ball start R
        if playerlost == "right":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not ball_moving:
                    ball_moving = True
                    ball_speed_x = ball_speed
                    ball_speed_y = 0
                    playerlost = None
                    ball_was_hit = False
                    ball_speed += 10

    pygame.display.flip()

pygame.quit()
