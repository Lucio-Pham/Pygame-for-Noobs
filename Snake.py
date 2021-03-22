import pygame
import random
import time

pygame.init()

#set up color
blue= (0, 0 , 255) 
red= (255, 0, 0) 
black= (0, 0, 0)
white= (255, 255, 255) 
yellow= (50, 153, 213) 
green= ( 0, 255, 0) 

dis_width = 800
dis_height = 600

display= pygame.display.set_mode((dis_width, dis_height))

pygame.display.update()
pygame.display.set_caption('Snake Game')


snake_block= 10

clock = pygame.time.Clock()
snake_speed= 30

font_style= pygame.font.SysFont('bahnschrift', 25) 
score_font= pygame.font.SysFont('comicsansms', 35) 

def your_score(score): 
    for x in snake_list: 
        pygame.draw.rect(display, black, [x[0, x[1], snake_block, snake_block])


def our_snake (snake_block, snake_list): 
    for x in snake_list: 
        pygame.draw.rect(display, black, [x[0], x[1], snake_block, snake_block]) 

def message(msg, color): 
    mesg= font_style.render(msg, True, color) 
    display.blit(mesg, [dis_width/3, dis_height/3]) 

def game_loop(): 
    game_over= False
    game_close= False

    x1 = dis_width/2
    y1 = dis_height/2

    x1_change = 0 
    y1_change = 0 

    snake_List= []
    Length_of_snake= 1

    food_x = round(random.randrange(0, dis_width-snake_block)/10.0)*10.0 
    food_y = round(random.randrange(0, dis_width - snake_block)/10.0)*10.0 
    
    while not game_over: 
        while game_close ==True: 
            display.fill(blue)
            message("You lost! Press Q-Quit or C-Play again", red) 
            your_score(Length_of_snake -1)
            pygame.display.update() 

            for event in pygame.event.get(): 
                if event.type==pygame.KEYDOWN: 
                    if event.key == pygame.K_q: 
                        game_over==True
                        game_close==False
                    if event.key==pygame.K_c:
                        game_Loop()

        for event in pygame.event.get(): 
            if event.type==pygame.QUIT:
                game_over= True
            if event.type==pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT: 
                    x1_change = -snake_block
                    y1_change = 0 
                elif event.key==pygame.K_RIGHT: 
                    x1_change = snake_block
                    y1_change = 0
                elif event.key==pygame.K_UP: 
                    x1_change = 0 
                    y1_change = -snake_block
                elif event.key==pygame.K_DOWN: 
                    x1_change = 0
                    y1_change = snake_block
        if x1 >= dis_width or x1 <0 or y1 >=dis_height or y1<0: 
            game_over= True
        x1 += x1_change
        y1 += y1_change
        display.fill(blue) 

        pygame.draw.rect(display, green, [food_x, food_y, snake_block, snake_block]) 
        snake_Head= []
        snake_Head.append(x1) 
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len (snake_List) > Length_of_snake: 
            del snake_List[0]
        for x in snake_List[:-1]: 
            if x ==snake_Head: 
                game_close= True
        our_snake(snake_block, snake_List) 
        your_score(Length_of_snake -1)
        #pygame.draw.rect(display, black, [x1, y1, snake_block, snake_block]) 

        pygame.display.update()
        
        if x1==food_x and y1==food_y: 
            food_x= round(random.randrange(0, dis_width-snake_block) /10.0)*10.0
            food_y= round(random.randrange(0, dis_height-snake_block) /10.0)*10.0
            Length_of_snake += 1
         

        clock.tick(snake_speed) 
        time.sleep(2)

pygame.quit()
quit()

