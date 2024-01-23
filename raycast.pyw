import numpy
import math
import random
import sys
import pygame as pg

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
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
MINIMAP_SCALE = 7

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

for i in range(100):
    walls.append(pg.Rect(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(32, 100), random.randint(32, 100)))

class Player:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.z = 100
        self.angle = 0
        self.speed = 8
        self.turn_speed = 3

    def update(self):
        keys = pg.key.get_pressed()
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
            self.x -= math.cos(math.radians(self.angle + 90)) * self.speed
            self.y -= math.sin(math.radians(self.angle + 90)) * self.speed
            for wall in walls:
                if wall.collidepoint(self.x, self.y):
                    self.x += math.cos(math.radians(self.angle + 90)) * self.speed
                    self.y += math.sin(math.radians(self.angle + 90)) * self.speed
        if keys[pg.K_d]:
            self.x += math.cos(math.radians(self.angle + 90)) * self.speed
            self.y += math.sin(math.radians(self.angle + 90)) * self.speed
            for wall in walls:
                if wall.collidepoint(self.x, self.y):
                    self.x -= math.cos(math.radians(self.angle + 90)) * self.speed
                    self.y -= math.sin(math.radians(self.angle + 90)) * self.speed
        if keys[pg.K_ESCAPE]:
            sys.exit()
player = Player()

def ray_casting():
    for ray_angle in numpy.arange(player.angle - 32, player.angle + 32, 0.25):
        sin_a = math.sin(math.radians(ray_angle))
        cos_a = math.cos(math.radians(ray_angle))
        for depth in range(1, 800, 8):
            test_x = player.x + cos_a * depth
            test_y = player.y + sin_a * depth
            if pg.Rect(test_x, test_y, 5, 5).collidelist(walls) != -1:
                for depth2 in numpy.arange(depth, depth - 5, -0.25):
                    test_x = player.x + cos_a * depth2
                    test_y = player.y + sin_a * depth2
                    if pg.Rect(test_x, test_y, 1, 1).collidelist(walls) == -1:
                        break
                break

        depth *= math.cos(math.radians(ray_angle - player.angle))

        wall_color = (220 / (1 + depth * 0.005)**2, 215 / (1 + depth * 0.005)**2, 172 / (1 + depth * 0.008)**2)
        wall_height = (SCREEN_HEIGHT / (depth*0.01))
        pg.draw.rect(screen, wall_color, ((ray_angle-player.angle+32)*30, SCREEN_HEIGHT/2-wall_height/2
                                          ,8, wall_height))

def draw_floor():
    for y in range(int(SCREEN_HEIGHT/2), SCREEN_HEIGHT, 20):
        pg.draw.rect(screen, (y/SCREEN_HEIGHT*95, y/SCREEN_HEIGHT*91, y/SCREEN_HEIGHT*59), (0, y, SCREEN_WIDTH, 20))

def draw_ceiling():
    for y in range(0, int(SCREEN_HEIGHT/2), 20):
        pg.draw.rect(screen, ((1-(y/SCREEN_HEIGHT)**0.5)*232, (1-(y/SCREEN_HEIGHT)**0.5)*232, (1-(y/SCREEN_HEIGHT)**0.5)*215), (0, y, SCREEN_WIDTH, 20))

def draw_gui():
    pg.draw.circle(screen, RED, SCREEN_CENTER, 5, 1)
    pg.draw.line(screen, RED, (SCREEN_CENTER[0] - 10, SCREEN_CENTER[1]), (SCREEN_CENTER[0] + 10, SCREEN_CENTER[1]), 1)
    pg.draw.line(screen, RED, (SCREEN_CENTER[0], SCREEN_CENTER[1] - 10), (SCREEN_CENTER[0], SCREEN_CENTER[1] + 10), 1)

    fps = int(clock.get_fps())
    fps_text = pg.font.SysFont("Consolas", 24).render(str(fps), True, RED)
    fps_text_rect = fps_text.get_rect()
    fps_text_rect.topleft = (10, 10)
    screen.blit(fps_text, fps_text_rect)

    mini_map = pg.Surface((SCREEN_WIDTH//MINIMAP_SCALE, SCREEN_HEIGHT//MINIMAP_SCALE))
    mini_map.fill(BLACK)
    for wall in walls:
        pg.draw.rect(mini_map, WHITE, (wall.x//MINIMAP_SCALE, wall.y//MINIMAP_SCALE, wall.width//MINIMAP_SCALE, wall.height/8))
    pg.draw.circle(mini_map, RED, (int(player.x//MINIMAP_SCALE), int(player.y//MINIMAP_SCALE)), 2)
    pg.draw.line(mini_map, RED, (int(player.x//MINIMAP_SCALE), int(player.y//MINIMAP_SCALE)), (int(player.x//MINIMAP_SCALE + math.cos(math.radians(player.angle))*10), int(player.y//MINIMAP_SCALE + math.sin(math.radians(player.angle))*10)), 1)
    mini_map.set_alpha(200)
    screen.blit(mini_map, (SCREEN_WIDTH - SCREEN_WIDTH//MINIMAP_SCALE, 0))

    player_pos_text = pg.font.SysFont("Consolas", 24).render(f'{int(player.x)} X {int(player.y)} Y', True, RED)
    player_pos_text_rect = player_pos_text.get_rect()
    player_pos_text_rect.topleft = (SCREEN_WIDTH - player_pos_text_rect.width - SCREEN_WIDTH//MINIMAP_SCALE - 20, 10)
    screen.blit(player_pos_text, player_pos_text_rect)
    
def main():
    pg.mouse.set_visible(False)
    pg.display.toggle_fullscreen()
    player.x = SCREEN_WIDTH//2
    player.y = SCREEN_HEIGHT//2
    while pg.Rect(player.x, player.y, 5, 5).collidelist(walls) != -1:
        player.x += 1
        player.y += 1
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
        mouse_x, mouse_y = pg.mouse.get_pos()
        pg.mouse.set_pos(SCREEN_CENTER)
        player.angle += (mouse_x - SCREEN_CENTER[0]) * 0.1
        draw_ceiling()
        draw_floor()
        player.update()
        ray_casting()
        draw_gui()
        pg.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()