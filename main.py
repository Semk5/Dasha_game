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
                Tile(x,y,"wall",random.choice(images["wall"]))
            if level[y][x] == ".":
                Tile(x,y,"empty",images["empty"])
            if level[y][x] == "|":
                Tile(x, y, "river", images["river"])
            if level[y][x] == "@":
                Tile(x,y,"empty",images["empty"])
                pl = Player(x,y)
            if level[y][x] == "$":
                Mushroom(x,y)
    return pl

def loading_screen(scr, font):
    scr.blit(load_image(rf"data/sprites/main menu/background/frame_00_delay-0.1s.png"), (0, 0))
    draw_text("Loading...", font, pygame.Color("gainsboro"), scr, (480, 480), centerX=True)
    pygame.display.flip()

def next_level():
    global current_level
    global level_loaded
    global last_score
    current_level += 1
    level_loaded = False
    mushrooms.empty()
    tiles.empty()

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, tile_type, image):
        super().__init__(tiles)
        self.type = tile_type
        self.image = image
        self.rect = self.image.get_rect().move(pos_x*TILE_SIZE,pos_y*TILE_SIZE)
    def get_type(self):
            return self.type

class Mushroom(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(mushrooms)
        self.image = mushroom_image
        self.rect = self.image.get_rect().move(pos_x * TILE_SIZE + random.randint(0,40), pos_y * TILE_SIZE + random.randint(0,40))
    def take_mushroom(self):
        global score
        score+=1
        mushrooms.remove(self)

class Player(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.image = player_image[0]
        self.x = pos_x
        self.y = pos_y
        self.rect = self.image.get_rect().move(self.x*TILE_SIZE,self.y*TILE_SIZE)
    def directional_move(self):
        global moved_recently
        if not moved_recently:
            if up_pressed == True and self.y > 0:
                self.y -= 1
                self.rect = self.image.get_rect().move(self.x * TILE_SIZE, self.y * TILE_SIZE)
                collider = pygame.sprite.spritecollideany(self,tiles)
                self.image = player_image[1]
                if collider:
                    if collider.get_type() == "wall" or collider.get_type() == "river":
                        self.y += 1
                        self.rect = self.image.get_rect().move(self.x * TILE_SIZE, self.y * TILE_SIZE)
            if down_pressed == True and self.y < 14:
                self.y += 1
                self.rect = self.image.get_rect().move(self.x * TILE_SIZE, self.y * TILE_SIZE)
                collider = pygame.sprite.spritecollideany(self, tiles)
                self.image = player_image[0]
                if collider:
                    if collider.get_type() == "wall" or collider.get_type() == "river":
                        self.y -= 1
                        self.rect = self.image.get_rect().move(self.x * TILE_SIZE, self.y * TILE_SIZE)
            if left_pressed == True and self.x > 0:
                self.x -= 1
                self.rect = self.image.get_rect().move(self.x * TILE_SIZE, self.y * TILE_SIZE)
                collider = pygame.sprite.spritecollideany(self, tiles)
                self.image = player_image[2]
                if collider:
                    if collider.get_type() == "wall" or collider.get_type() == "river":
                        self.x += 1
                        self.rect = self.image.get_rect().move(self.x * TILE_SIZE, self.y * TILE_SIZE)
            if right_pressed == True and self.x < 14:
                self.x += 1
                self.rect = self.image.get_rect().move(self.x * TILE_SIZE, self.y * TILE_SIZE)
                collider = pygame.sprite.spritecollideany(self, tiles)
                self.image = player_image[3]
                if collider:
                    if collider.get_type() == "wall" or collider.get_type() == "river":
                        self.x -= 1
                        self.rect = self.image.get_rect().move(self.x * TILE_SIZE, self.y * TILE_SIZE)
            collider = pygame.sprite.spritecollideany(self,mushrooms)
            if collider: collider.take_mushroom()
            moved_recently = True

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
    game_font = pygame.font.Font(r"data/fonts/PixeloidSans-Bold.ttf", 30)
    caption_font = pygame.font.Font(r"data/fonts/AncientModernTalesPixel.ttf", 60)
    loading_screen(screen, caption_font)
    clock = pygame.time.Clock()
    game_state = 0  # 0 - main menu, 1 - game, 2 - end screen
    level_loaded = False
    running = True
    frame_number = 0
    selected_item = 0
    max_items = 1
    score = 0
    current_level = 0
    time = 0
    last_score = 0
    last_mushrooms = 0
    left_pressed = right_pressed = up_pressed = down_pressed = moved_recently = False
    player_image = [load_image(r"data/sprites/level/Player_Down.png"),load_image(r"data/sprites/level/Player_Up.png"),load_image(r"data/sprites/level/Player_Left.png"),load_image(r"data/sprites/level/Player_Right.png")]
    mushroom_image = load_image(r"data/sprites/level/Brown_Mushroom.png")
    level_images ={
        "wall":[load_image(rf"data/sprites/level/plants/{file}") for file in os.listdir(r"data/sprites/level/plants")],
        "river":load_image(r"data/sprites/level/water.png"),
        "empty":load_image(r"data/sprites/level/empty.png"),
        }
    tiles = pygame.sprite.Group()
    mushrooms = pygame.sprite.Group()
    house = load_image(r"data/sprites/level/House.png")
    game_background = load_image(r"data/sprites/level/background.png")
    levels = [r"data/levels/1.txt", r"data/levels/2.txt"]
    number_of_levels = len(levels)
    pygame.display.set_caption("ГРИБНИК")
    background_frames = [load_image(rf"data/sprites/main menu/background/{file}") for file in os.listdir(r"data/sprites/main menu/background")]
    background = Background(background_frames, (0, 0))
    path = load_image(r"data/sprites/level/Path.png")
    menu_chanel = pygame.mixer.Channel(1)
    game_chanel = pygame.mixer.Channel(2)
    game_chanel.set_volume(0)
    menu_music = pygame.mixer.Sound(r"data/music/main menu/Guts.mp3")
    game_music = pygame.mixer.Sound(r"data/music/main menu/Guts 8bit.mp3")
    game_chanel.play(game_music,-1)
    menu_chanel.play(menu_music,-1)
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
                        menu_chanel.set_volume(0)
                        game_chanel.set_volume(1)
                    if event.key == pygame.K_RETURN and selected_item == 1:
                        running = False
            if frame_number % 4 == 0: background.change_frame()
            screen.blit(background.image, background.rect)
            draw_text("GRIBNIK", caption_font, pygame.Color("firebrick2"), screen, (480, 200), antialias=False,
                      centerX=True)
            draw_text("-> Start game" if selected_item == 0 else "Start game", caption_font,
                      pygame.Color("firebrick2") if selected_item == 0 else pygame.Color("gainsboro"), screen,
                      (480, 500), centerX=True)
            draw_text("-> Exit" if selected_item == 1 else "Exit", caption_font,
                      pygame.Color("firebrick2") if selected_item == 1 else pygame.Color("gainsboro"), screen,
                      (480, 600), centerX=True)
            draw_text("Game by %ME%",game_font, pygame.Color("white"), screen, (600, 900), antialias=False)
            pygame.display.flip()
            frame_number = frame_number + 1 if frame_number <= 60 else 0
            clock.tick(FPS)
        if game_state == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        up_pressed = True
                    if event.key == pygame.K_s:
                        down_pressed = True
                    if event.key == pygame.K_a:
                        left_pressed = True
                    if event.key == pygame.K_d:
                        right_pressed = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        up_pressed = False
                    if event.key == pygame.K_s:
                        down_pressed = False
                    if event.key == pygame.K_a:
                        left_pressed = False
                    if event.key == pygame.K_d:
                        right_pressed = False
                    moved_recently = False
            if not level_loaded:
                player = generate_level(levels[current_level], level_images)
                level_loaded = True
                last_score = score
                last_mushrooms = len(mushrooms)
            player.directional_move()
            screen.blit(game_background,[0,0])
            tiles.draw(screen)
            mushrooms.draw(screen)
            screen.blit(player.image,player.rect)
            draw_text(f"Score: {score}", game_font, pygame.Color("antiquewhite1"), screen, (20, 20), antialias=False)
            draw_text(f"Time: {0 if time//60 < 10 else ""}{time//60}:{0 if time%60 < 10 else ""}{time%60}", game_font, pygame.Color("antiquewhite1"), screen, (20, 60), antialias=False)
            frame_number = frame_number + 1 if frame_number <= 60 else 0
            if frame_number % 8 == 0: moved_recently = False
            if frame_number == 60: time += 1
            pygame.display.flip()
            clock.tick(FPS)
            if score == last_score + last_mushrooms:
                menu_chanel.set_volume(1)
                game_chanel.set_volume(0)
                if current_level != number_of_levels  and player.x == 0 and player.y == 0:
                    next_level()
            else:
                menu_chanel.set_volume(0)
                game_chanel.set_volume(3)
            if current_level == number_of_levels and score == last_score + last_mushrooms and player.x == 0 and player.y == 0:
                game_state = 2
                menu_chanel.set_volume(1)
                game_chanel.set_volume(0)
                mushrooms.empty()
                tiles.empty()
                level_loaded = False
        if game_state == 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        up_pressed = True
                    if event.key == pygame.K_s:
                        down_pressed = True
                    if event.key == pygame.K_a:
                        left_pressed = True
                    if event.key == pygame.K_d:
                        right_pressed = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        up_pressed = False
                    if event.key == pygame.K_s:
                        down_pressed = False
                    if event.key == pygame.K_a:
                        left_pressed = False
                    if event.key == pygame.K_d:
                        right_pressed = False
                    moved_recently = False
            if not level_loaded:
                mushrooms.empty()
                tiles.empty()
                player = generate_level(r"data/levels/end.txt", level_images)
                level_loaded = True
            player.directional_move()
            screen.blit(game_background, [0, 0])
            screen.blit(path,[448,440])
            screen.blit(player.image, player.rect)
            tiles.draw(screen)
            if 5 <= player.x <= 9 and 2 <= player.y <= 6:
                if player.y == 6:
                    house.set_alpha(150)
                if player.y == 5:
                    house.set_alpha(100)
                if player.y == 4:
                    house.set_alpha(50)
                if player.y == 3:
                    house.set_alpha(100)
                if player.y == 2:
                    house.set_alpha(150)
            else: house.set_alpha(256)
            screen.blit(house, [322,170])
            draw_text(f"You win!!", game_font,pygame.Color("antiquewhite1"),screen,[480,60],antialias=False,centerX=True)
            if frame_number > 30:
                draw_text(f"Time: {0 if time // 60 < 10 else ""}{time // 60}:{0 if time % 60 < 10 else ""}{time % 60}", game_font, pygame.Color("crimson"), screen, [480, 90], antialias=False,centerX=True)
                draw_text(f"Score: {score}", game_font, pygame.Color("crimson"), screen, [480, 120], antialias=False,centerX=True)
            frame_number = frame_number + 1 if frame_number <= 60 else 0
            if frame_number % 6 == 0: moved_recently = False
            pygame.display.flip()
            clock.tick(FPS)
