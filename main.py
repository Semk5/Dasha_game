import pygame
import random
import sys
import os


FPS = 60
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 960
TILE_SIZE = 64

def load_image(name, colorkey=None):
    image = pygame.image.load(name)
    if colorkey:
        if colorkey == -1:
            image.set_colorkey(image.get_at((0, 0)))
        else:
            image.set_colorkey(colorkey)
        image.convert()
    else:
        image.convert_alpha()
    return image


def draw_text(text, font, color, surface, pos, antialias=True, centerX=False, centerY=False):
    text_object = font.render(text, antialias, color)
    x,y = pos
    if centerX:
        x -= font.size(text)[0] // 2
    if centerY:
        y -= font.size(text)[0] // 2
    surface.blit(text_object, (x,y))

def generate_level(file, images):
    f = open(file)
    level = f.readlines()
    f.close()
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == "#":
                Tile(tiles,x,y,"wall",images)
            if level[y][x] == ".":
                Tile(tiles,x,y,"empty",images)
            if level[y][x] == "|":
                Tile(tiles, x, y, "river_vertical", images)
            if level[y][x] == "@":
                Tile(tiles,x,y,"empty",images)
                pl = Player(x,y)
    return pl

def loading_screen(scr, font):
    scr.blit(load_image(rf"data/sprites/main menu/background/frame_00_delay-0.1s.png"), (0, 0))
    draw_text("Loading...", font, pygame.Color("gainsboro"), scr, (480, 480), centerX=True)

class Tile(pygame.sprite.Sprite):
    def __init__(self,group,pos_x,pos_y, tile_type, tile_images):
        super().__init__(group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x*TILE_SIZE,pos_y*TILE_SIZE)

class Player(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.image = player_image
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(self.x*TILE_SIZE,self.y*TILE_SIZE)
    def directional_move(self, dest):  # 1 - up, 2 - down, 3 - left, 4 - right
        if dest == 1 and self.y > 0:
            self.y -= 1
        if dest == 2 and self.y < 15:
            self.y += 1
        if dest == 3 and self.x > 0:
            self.x -= 1
        if dest == 4 and self.x < 15:
            self.x += 1
        self.rect = self.image.get_rect().move(self.x * TILE_SIZE, self.y * TILE_SIZE)

class Background(pygame.sprite.Sprite):
    def __init__(self, image_input, pos):
        super().__init__()
        self.images = image_input
        self.frame = 0
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect().move(pos)
    def change_frame(self):
        if len(self.images) - 1 > self.frame:
            self.frame += 1
        else:
            self.frame = 0
        self.image = self.images[self.frame]

if __name__ == '__main__':
    pygame.init()
    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(size)
    usual_font = pygame.font.Font(r"data/fonts/antiquity-print.ttf", 40)
    loading_screen(screen, usual_font)
    clock = pygame.time.Clock()
    game_state = 0  # 0 - main menu, 1 - game, 2 - end screen
    running = True
    frame_number = 0
    selected_item = 0
    max_items = 1
    music_volume = 1
    player_image = load_image(r"data/sprites/level/player.png")
    level_images ={
        "wall":load_image(r"data/sprites/level/tree.png"),
        "river_vertical":load_image(r"data/sprites/level/water.png"),
        "empty":load_image(r"data/sprites/level/empty.png")
        }
    tiles = pygame.sprite.Group()
    game_background = load_image(r"data/sprites/level/background.png")
    player = generate_level(r"data/levels/1.lvl", level_images)
    pygame.display.set_caption("The elder scrolls 0: мужик в лесу")
    caption_font = pygame.font.Font(r"data/fonts/AncientModernTalesPixel.ttf", 60)
    default_font = pygame.font.Font(None, 40)
    background_frames = [load_image(rf"data/sprites/main menu/background/{file}") for file in os.listdir(
        r"data/sprites/main menu/background")]
    background = Background(background_frames, (0, 0))
    pygame.mixer.music.load(fr"data/music/main menu/Guts.mp3")
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play(-1)
    while running:
        if game_state == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN and selected_item < max_items:
                        selected_item += 1
                    if event.key == pygame.K_UP and selected_item > 0:
                        selected_item -= 1
                    if event.key == pygame.K_RETURN and selected_item == 0:
                        game_state = 1
                    if event.key == pygame.K_RETURN and selected_item == 1:
                        running = False
            if frame_number % 4 == 0: background.change_frame()
            screen.blit(background.image, background.rect)
            draw_text("The elder scrolls 0:", caption_font, pygame.Color("gainsboro"), screen, (480, 200),
                      antialias=False, centerX=True)
            draw_text("FOREST", caption_font, pygame.Color("firebrick2"), screen, (480, 300), antialias=False,
                      centerX=True)
            draw_text("-> Start game" if selected_item == 0 else "Start game", caption_font,
                      pygame.Color("firebrick2") if selected_item == 0 else pygame.Color("gainsboro"), screen,
                      (480, 500), centerX=True)
            draw_text("-> Exit" if selected_item == 1 else "Exit", caption_font,
                      pygame.Color("firebrick2") if selected_item == 1 else pygame.Color("gainsboro"), screen,
                      (480, 600), centerX=True)
            pygame.display.flip()
            frame_number = frame_number + 1 if frame_number < 60 else 0
            clock.tick(FPS)
        if game_state == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        player.directional_move(1)
                    if event.key == pygame.K_s:
                        player.directional_move(2)
                    if event.key == pygame.K_a:
                        player.directional_move(3)
                    if event.key == pygame.K_d:
                        player.directional_move(4)
            screen.blit(game_background,[0,0])
            screen.blit(player.image,player.rect)
            tiles.draw(screen)
            pygame.display.flip()
        if game_state == 2:
            pass
