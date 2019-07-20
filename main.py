import pygame
import random
import os

pygame.init()

#game specific variables
clock = pygame.time.Clock()
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
white = (255, 255 , 255)
red = (255 , 0 , 0)
black = (0, 0 , 0)
green = (0, 255 ,0)
blue = (135,206,250)

#creating game window
gamewindow = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Snake game")

#loading image to display while playing
bgimg1 = pygame.image.load("snake2.png")
bgimg1 = pygame.transform.scale(bgimg1, (SCREEN_WIDTH//2,SCREEN_HEIGHT//2)).convert_alpha()

#loading image to display on welcome screen
bgimg2 = pygame.image.load("welcome.png")
bgimg2 = pygame.transform.scale(bgimg2, ((SCREEN_WIDTH//2)+500,(SCREEN_HEIGHT//2)+100)).convert_alpha()

#loading image to display apple (snake's food)
bgimg3 = pygame.image.load("apple1.png")
bgimg3 = pygame.transform.scale(bgimg3, ((SCREEN_WIDTH//22),(SCREEN_HEIGHT//18))).convert_alpha()

#loading image to display when game is over
bgimg4 = pygame.image.load("gameover_snake.png")
bgimg4 = pygame.transform.scale(bgimg4, (SCREEN_WIDTH//4,SCREEN_HEIGHT//2)).convert_alpha()

#function to display text on the screen
def text_screen(text, color, x , y,fsize):
    font = pygame.font.SysFont("comicsansms", fsize)
    screen_text = font.render(text , True , color)
    gamewindow.blit(screen_text , [x,y])

#function to draw snake
def plot_snake(gamewindow , color , snk_list , snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gamewindow, color , [x, y, snake_size, snake_size])

#function to display welcome screen
def welcomeScreen():
    game_exit = False
    while not game_exit:
        gamewindow.fill(black)
        gamewindow.blit(bgimg2, (0, 30))
        text_screen("Welcome to snakes",white,230,420,50)
        text_screen("(Press space bar to play)",white, 310,490,30)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameLoop()

#function which initiates game loop
def gameLoop():
    game_exit = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_size = 25
    velocity_x = 0
    velocity_y = 0
    FPS = 60
    init_velocity = 2
    score = 0
    food_x = random.randint(40, SCREEN_WIDTH / 2)
    food_y = random.randint(40, SCREEN_HEIGHT / 2)
    snk_list = []
    snk_len = 1


    gamewindow.blit(bgimg1 ,(0,0))

    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")

    else:
        with open("highscore.txt", "r") as f:
            hiscore = f.read()

    while not game_exit:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(hiscore))
            pygame.mixer.music.load("woodpecker.mp3")
            pygame.mixer.music.play()
            gamewindow.fill(black)
            gamewindow.blit(bgimg4, (320, (SCREEN_HEIGHT//2)-250))
            text_screen("Game Over", blue, 280, 400,60)
            text_screen("(Press Enter To Continue)", blue, 285, 490, 25)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.stop()
                        welcomeScreen()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -(init_velocity)
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -(init_velocity)
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_q:
                        score = score + 10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 15 and abs(snake_y - food_y) < 15:
                score = score + 10
                snk_len = snk_len + 5
                food_x = random.randint(40, SCREEN_WIDTH / 2)
                food_y = random.randint(40, SCREEN_HEIGHT / 2)
                pygame.mixer.music.load("Wood_Plank_Flicks.mp3")
                pygame.mixer.music.play()

            gamewindow.fill(black)
            gamewindow.blit(bgimg1, (SCREEN_WIDTH -SCREEN_WIDTH//2,SCREEN_HEIGHT-SCREEN_HEIGHT//2.5))
            text_screen(f"Score: {score}   HighScore: {hiscore}", blue, 5, 5,30)
            gamewindow.blit(bgimg3 , (food_x , food_y))
            #pygame.draw.rect(gamewindow, red, [food_x, food_y, snake_size, snake_size])
            if(score <200 and score>=0):
                text_screen(f"       ", black, 780, 5, 30)
                text_screen(f"Level 1", blue, 780, 5, 30)

            elif(score >= 400 and score < 800):
                text_screen(f"       ",black,780,5,30)
                text_screen(f"Level 3", blue, 780, 5, 30)
                text_screen(f"                 ", black, 30, 550, 30)
                text_screen(f"Level 2 completed", blue, 30 ,550, 20)

            elif(score >= 200 and score < 400):
                text_screen(f"       ", black, 780, 5, 30)
                text_screen(f"Level 2", blue, 780, 5, 30)
                text_screen(f"                 ", black,30,550,20)
                text_screen(f"Level 1 completed", blue, 30, 550, 20)

            elif(score >= 800):
                text_screen(f"       ", black, 780, 5, 30)
                text_screen(f"                 ", black, 10,550,20)
                text_screen(f"Level 3 completed", blue, 10, 550, 20)


            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if(len(snk_list) > snk_len):
                del snk_list[0]

            if snake_x < 0 or snake_x > SCREEN_WIDTH or snake_y < 0 or snake_y > SCREEN_HEIGHT:
                game_over = True

            if score > int(hiscore):
                hiscore = score

            plot_snake(gamewindow, green, snk_list, snake_size)

        pygame.display.update()
        clock.tick(FPS)

#call to  welcomescreen()
welcomeScreen()

#quitting pygame and program
pygame.quit()
quit()