import pygame ,sys ,random, cv2, math
import HandsTrackingModule as htm
import numpy as np
pygame.init()
#################################################
cam_width, cam_height = 640,480
pTime = 0
#################################################


cap = cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)

detector = htm.HandDetector(detection_con=0.7)



def ball_animation():
    #updating objectd varibale values-like speed/position etc.
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x 
    ball.y += ball_speed_y 
    
    #checking for ball collisions with 4-sides
    if ball.top <= 0  or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= WIDTH:
        game_restart()
    #collsion between ball and paddle
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1    
        smash.play() 
        

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= HEIGHT:
        player.bottom = HEIGHT
    
def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= HEIGHT:
        opponent.bottom = HEIGHT

def game_restart():
    global ball_speed_x, ball_speed_y
    ball_speed_x *= random.choice((1,-1))
    ball_speed_y *= random.choice((1,-1))
    ball.center = (WIDTH/2, HEIGHT/2)




WIDTH = 800
HEIGHT = 610
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PONG')
clock = pygame.time.Clock()

#game objects 
ball = pygame.Rect(WIDTH/2-15, HEIGHT/2-15, 30, 30)
player = pygame.Rect(WIDTH - 20 ,HEIGHT/2-70 ,10, 140)
opponent = pygame.Rect(10 ,HEIGHT/2-70 ,10, 140)

#color variables
bg_color = pygame.Color('grey12')
light_grey = (200,200,200)

# Adjusting objects speed 
ball_speed_x = 7 * random.choice((1,-1))
ball_speed_y = 7 * random.choice((1,-1))
player_speed = 0 
opponent_speed = 10

# boll colliding sound
smash = pygame.mixer.Sound('smash.mp3')

player_paddle_height = 10

while True:
    _, img = cap.read()
    img = detector.find_hands(img)
    landmark_list = detector.find_positions(img, draw=False)
    # print(landmark_list)

    if landmark_list:
        x1,y1 = landmark_list[4][1], landmark_list[4][2]
        # x2,y2 = landmark_list[8][1], landmark_list[8][2]
        # cx,cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1,y1),10,(255,0,0),cv2.FILLED)
        # cv2.circle(img, (x2,y2),10,(255,0,0),cv2.FILLED)
        # cv2.circle(img, (cx,cy),10,(255,0,0),cv2.FILLED)
        # cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)

        # line_length = math.hypot(x2-x1, y2-y1)
        # print(line_length)

        # player_paddle_height = np.interp(line_length, [30,200],[10, 470])
        player_paddle_height = y1

    #checking all events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_DOWN:
        #         player_speed += 7
        #     if event.key == pygame.K_UP:
        #         player_speed -= 7
        # if event.type == pygame.KEYUP:
        #     # player_speed = 0
        #     if event.key == pygame.K_DOWN:
        #         player_speed -= 7
        #     if event.key == pygame.K_UP:
        #         player_speed += 7
    # if player_paddle_height > 100:
    #     player_speed -=7
    # else:
    #     player_speed +=7

    
    player.top = player_paddle_height
    
    print('player_speed: ', player_speed)
    ball_animation()
    player_animation()
    opponent_ai()

    
    
    #displaying all objects on screen
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (WIDTH/2,0),(WIDTH/2, HEIGHT))
    
    #updating the window
    pygame.display.flip()
    clock.tick(60)

    cv2.imshow('check gestures',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break