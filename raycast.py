import numpy
import math
import random
import sys
import pygame as pg

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 780
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_CENTER = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
SCREEN_RECT = pg.Rect((0, 0), SCREEN_SIZE)
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
BROWN = (139, 69, 19)

pg.init()
pg.display.set_caption("Half Life 3")
screen = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock()

walls = []
for x in range(0, SCREEN_WIDTH, 64):
    walls.append(pg.Rect(x, 0, 64, 64))
    walls.append(pg.Rect(x, SCREEN_HEIGHT - 64, 64, 64))
for y in range(0, SCREEN_HEIGHT, 64):
    walls.append(pg.Rect(0, y, 64, 64))
    walls.append(pg.Rect(SCREEN_WIDTH - 64, y, 64, 64))

# generate random walls for testing
for i in range(10):
    walls.append(pg.Rect(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(10, 100), random.randint(10, 100)))

class Player:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.angle = 0
        self.speed = 5
        self.turn_speed = 3

    def update(self):
        keys = pg.key.get_pressed()
        # pass if touching wall
        if keys[pg.K_w]:
            self.x += math.cos(math.radians(self.angle)) * self.speed
            self.y += math.sin(math.radians(self.angle)) * self.speed
            for wall in walls:
                if wall.collidepoint(self.x, self.y):
                    self.x -= math.cos(math.radians(self.angle)) * self.speed
                    self.y -= math.sin(math.radians(self.angle)) * self.speed
        if keys[pg.K_s]:
            self.x -= math.cos(math.radians(self.angle)) * self.speed
            self.y -= math.sin(math.radians(self.angle)) * self.speed
            for wall in walls:
                if wall.collidepoint(self.x, self.y):
                    self.x += math.cos(math.radians(self.angle)) * self.speed
                    self.y += math.sin(math.radians(self.angle)) * self.speed
        if keys[pg.K_a]:
            self.angle -= self.turn_speed
        if keys[pg.K_d]:
            self.angle += self.turn_speed

player = Player()

def ray_casting():
    for ray_angle in numpy.arange(player.angle - 30, player.angle + 30, 0.5):
        sin_a = math.sin(math.radians(ray_angle))
        cos_a = math.cos(math.radians(ray_angle))
        for depth in range(2, 800, 3):
            test_x = player.x + cos_a * depth
            test_y = player.y + sin_a * depth
            if pg.Rect(test_x, test_y, 5, 5).collidelist(walls) != -1:
                depth *= math.cos(math.radians(ray_angle - player.angle))
                depth *= 0.8
                break
        wall_color = (200 / (1 + depth * 0.02), 200 / (1 + depth * 0.01), 255 / (1 + depth * 0.02))
        wall_height = (SCREEN_HEIGHT / (depth*0.01))
        pg.draw.rect(screen, wall_color, ((ray_angle-player.angle+30)*15, SCREEN_HEIGHT/2-wall_height/2, 8, wall_height))


def draw_floor():
    pg.draw.rect(screen, BROWN, (0, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT/2))

def draw_ceiling():
    pg.draw.rect(screen, CYAN, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT/2))
    
def main():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
        draw_ceiling()
        draw_floor()
        player.update()
        ray_casting()
        pg.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()