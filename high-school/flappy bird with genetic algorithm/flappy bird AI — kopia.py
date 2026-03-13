#-------------------------------modules---------------------------------------

import pygame
import random
import tensorflow
from tensorflow import keras
from keras import layers

#-----------------------------pygame stuff------------------------------------


pygame.init()


window = pygame.display.set_mode((600, 800))
pygame.display.set_caption("Flappy Bird")
#icon = pygame.image.load("smok1.png")
#pygame.display.set_icon(icon)
pygame.mouse.set_visible = True
clock = pygame.time.Clock()


window.fill((100, 100, 255))
TEXTCOLOR = (255, 255, 255)
font = pygame.font.SysFont("timesnewroman", 50)


#------------------------------variables-----------------------------------

end = False
speed = 5
distances = []
for x in range(73, 100):
    distances.append(x*speed)
next_pole = 0
number = 0
poles = []
birds = []
new_game = False
score = 0
gen = 1
nearest_pole = None
milage = 0
hiscore = 0
good_round = False


#--------------------------------classes-----------------------------------


class bird:
    def __init__(self, color):
        self.height = 400
        self.alive = True
        self.color = color
        self.r = color[0]
        self.g = color[1]
        self.b = color[2]
        if self.r > 25:
            self.r -= 25
        else:
            self.r = 0
        if self.g > 38:
            self.g -= 38
        else:
            self.g = 0
        if self.b > 27:
            self.b -= 27
        else:
            self.b = 0
        self.shadow = (self.r, self.g, self.b)
        self.r = color[0]
        self.g = color[1]
        self.b = color[2]
        if self.r < 160:
            self.r += 95
        else:
            self.r = 255
        if self.g < 247:
            self.g += 8
        else:
            self.g = 255
        self.ilumination = (self.r, self.g, self.b)
        self.speed = 10
        self.dragon = 0
        self.dragons = [pygame.image.load("smok1.png"), pygame.image.load("smok2.png")]
        for x in range(0, 2):
            self.img = self.dragons[x]
            for i in range(0, 20):
                for j in range(0, 20):
                    self.cl = self.img.get_at((i, j))[0]
                    if self.cl == 146:
                        self.img.set_at((i, j), self.ilumination)
                    elif self.cl == 51:
                        self.img.set_at((i, j), self.color)
                    elif self.cl == 26:
                        self.img.set_at((i, j), self.shadow)

    
    def jump(self):
        self.speed = -20
        self.dragon = 1


    def die(self):
        self.alive = False
        #if good_round:
            #print("h: %s d: %s ph: %s ps: %s" %(self.height, nearest_pole.distance, nearest_pole.height, nearest_pole.size))


    def fall(self):
        self.height += self.speed
        if self.speed < 10:
            self.speed += 5
            if self.speed > 0:
                self.dragon = 0






class pole:

    def __init__(self, height, size):
        self.height = height
        self.size = size
        self.distance = 600


    def go(self):
        global speed
        self.distance -= speed

    



#--------------------------------AI stuff------------------------------------


class brain(bird):

    def __init__(self, color, values):
        self.values = values
        bird.__init__(self, color)
        self.fitness = 1


    def calculate(self, Vdistance, Hdistance): #vertical, horizontal
        self.result = Vdistance * self.values[0]
        self.result += Hdistance * self.values[1]
        if self.result > self.values[1]:
            return True
        else:
            return False


    def calculate_fitness(self):
        self.fitness = milage
        if good_round:
            self.fitness += 10000


    def mutate(self):
        for x in range(0, 2):
            self.probability = random.randint(0, 3)
            if self.probability == 1:
                self.values[x] += random.uniform(-0.1, 0.1)
                self.values[x] = round(self.values[x], 3)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class generation:

    def make_new(self):
        for x in range(0, 30):
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.text = '''self.valuesg%sn%s = [round(random.uniform(-1, 1), 3), round(random.uniform(-1, 1), 3)]
birdg%sn%s = brain(self.color, self.valuesg%sn%s)
birds.append(birdg%sn%s)''' %(gen, x, gen, x, gen, x, gen, x)
            exec(self.text)


    def make_next(self):
        global birds
        self.fitnesses = []
        self.sum = 0
        self.babies = []
        b = birds[0]
        self.leader = brain(b.color, b.values)
        self.leader.fitness = b.fitness
        for b in birds:
            self.fitnesses.append(b.fitness)
            self.sum += b.fitness
            if b.fitness > self.leader.fitness:
                self.leader.color = b.color
                self.leader.values = b.values
                self.leader.fitness = b.fitness
        for q in range(0, 29):
            self.chosen = random.randint(1, self.sum)
            self.current_sum = 0
            for x in range(0, len(self.fitnesses)):
                self.current_sum += self.fitnesses[x]
                if self.current_sum >= self.chosen:
                    b = birds[x]
                    self.text = '''self.valuesg%sn%s = [b.values[0], b.values[1]]
birdg%sn%s = brain(b.color, self.valuesg%sn%s)
birdg%sn%s.mutate()
self.babies.append(birdg%sn%s)''' %(gen, q, gen, q, gen, q, gen, q, gen, q)
                    exec(self.text)
                    break
        birds = []
        for b in self.babies:
            birds.append(b)
        print(self.leader.values)
        self.text = '''self.valuesg%sn29 = [self.leader.values[0], self.leader.values[1]]
birdg%sn29 = brain(self.leader.color, self.valuesg%sn29)
birds.append(birdg%sn29)''' %(gen, gen, gen, gen)
        exec(self.text)




#-----------------------------game mechanics--------------------------------

Bird = brain((188, 41, 201), [0, 0])
birds.append(Bird)
Bird.fitness = 0
#better = brain((255, 255, 255), [0.105, 0.812])
#birds.append(better)
Gen = generation()
Gen.make_new()


while(not end):

    if new_game:
        poles = []
        next_pole = 0
        nearest_pole = None
        score = 0
        gen += 1
        Gen.make_next()
        Bird.alive = True
        Bird.height = 400
        birds.append(Bird)
        #birds.append(better)
        good_rund = False

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            end = True
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                Bird.jump()
                
            if event.key == pygame.K_DOWN:
                for b in birds:
                    if b.alive:
                        print(b.values)



    if next_pole == 0:
        code = '''pole%s = pole(random.randint(40, 610), random.randint(100, 105))
poles.append(pole%s)''' %(number, number)
        exec(code)
        random.shuffle(distances)
        next_pole = distances[0]
        if nearest_pole == None:
            nearest_pole = poles[0]

    next_pole -= speed
    milage += speed

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
                good_round = True
        if p.distance == - 15:
            nearest_pole = poles[1]
            


    p = poles[0]
    if p.distance < -100:
        del poles[0]

    new_game = True
    for b in birds:
        if b.alive:
            if b.fitness > 0 and b.calculate(b.height - (nearest_pole.height + (nearest_pole.size / 2)), 0): #nearest_pole.distance - 110
                b.jump()
            b.fall()
            pygame.draw.circle(window, b.color, (100, b.height), 10)
            #screen.blit(b.dragons[b.dragon], (90, b.height - 10))
            for p in poles:
                if p.distance <= 110 and p.distance + 100 >= 90:
                    if b.height - 10 <= p.height or b.height + 10 >= p.height + p.size:
                        b.die()
                        if b.fitness > 0:
                            b.calculate_fitness()
            if b.height > 800 or b.height < 0:
                b.die()
                if b.fitness > 0:
                    b.calculate_fitness()
            if b.alive:
                new_game = False


    

    text = font.render("Score: %s" %(score), 1, (255, 255, 255))
    screen.blit(text, (20, 20))
    another_text = font.render("Generation: %s" %(gen), 1, (255, 255, 255))
    screen.blit(another_text, (220, 20))
    other_text = font.render("Highest score: %s" %(hiscore), 1, (255, 255, 255))
    screen.blit(other_text, (20, 700))

    
    pygame.display.update()
    clock.tick(200) #30
    








    
