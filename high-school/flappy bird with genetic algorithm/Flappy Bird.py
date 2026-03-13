#-------------------------------modules---------------------------------------

import pygame
import random

#-----------------------------pygame stuff------------------------------------


pygame.init()


window = pygame.display.set_mode((600, 800))
pygame.display.set_caption("Flappy Bird")
pygame.mouse.set_visible = True
clock = pygame.time.Clock()


window.fill((100, 100, 255))
TEXTCOLOR = (255, 255, 255)
font = pygame.font.SysFont("timesnewroman", 50)


#------------------------------variables-----------------------------------

end = False
speed = 5
distances = []
for x in range(72, 100):
    distances.append(x*speed)
next_pole = 0
number = 0
poles = []
new_game = False
score = 0
nearest_pole = None
hiscore = 0


#--------------------------------classes-----------------------------------


class bird:
    def __init__(self, color):
        self.height = 400
        self.alive = True
        self.color = color
        self.speed = 10

    
    def jump(self):
        self.speed = -20


    def die(self):
        self.alive = False


    def fall(self):
        self.height += self.speed
        if self.speed < 10:
            self.speed += 5






class pole:

    def __init__(self, height, size):
        self.height = height
        self.size = size
        self.distance = 600


    def go(self):
        global speed
        self.distance -= speed

    






#-----------------------------game mechanics--------------------------------

Bird = bird((188, 41, 201))


while(not end):

    if new_game:
        poles = []
        next_pole = 0
        nearest_pole = None
        score = 0
        Bird.alive = True
        Bird.height = 400
        new_game = False

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            end = True
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                Bird.jump()



    if next_pole == 0:
        code = '''pole%s = pole(random.randint(40, 610), random.randint(100, 150))
poles.append(pole%s)''' %(number, number)
        exec(code)
        random.shuffle(distances)
        next_pole = distances[0]
        if nearest_pole == None:
            nearest_pole = poles[0]

    next_pole -= speed
    Bird.fall()

    screen = pygame.display.get_surface()

    pygame.draw.rect(window, (0, 252, 255), (0, 0, 600, 800))

    for p in poles:
        p.go()
        pygame.draw.rect(window, (0, 212, 0), (p.distance, 0, 100, p.height))
        pygame.draw.rect(window, (0, 212, 0), (p.distance, p.height + p.size, 100, 800 - (p.height + p.size)))
        if p.distance == -10:
            score += 1
            if score > hiscore:
                hiscore = score
            nearest_pole = poles[1]
            


    p = poles[0]
    if p.distance < -100:
        del poles[0]

    if not Bird.alive:
        new_game = True
    pygame.draw.circle(window, Bird.color, (100, Bird.height), 10)
    for p in poles:
        if p.distance <= 110 and p.distance + 100 >= 90:
            if Bird.height - 10 <= p.height or Bird.height + 10 >= p.height + p.size:
                Bird.die()
    if Bird.height > 800 or Bird.height < 0:
        Bird.die()


    

    text = font.render("Score: %s" %(score), 1, (255, 255, 255))
    screen.blit(text, (20, 20))
    other_text = font.render("Highest score: %s" %(hiscore), 1, (255, 255, 255))
    screen.blit(other_text, (20, 700))

    
    pygame.display.update()
    clock.tick(30) 

    
