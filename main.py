import pygame
import random
import sys
import os

from pygame import Color

FPS = 60
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 960


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

def loading_screen(screen,font):
    screen.blit(load_image(rf"data/sprites/main menu/background/frame_00_delay-0.1s.png"),(0,0))
    draw_text("Loading...", font, Color("gainsboro"), screen, (480, 480), centerX=True)

class Background(pygame.sprite.Sprite):
    def __init__(self, image_input, pos):
        super().__init__()
        self.images = image_input
        self.frame = 0
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def change_frame(self):
        if len(self.images) - 1 > self.frame:
            self.frame += 1
        else:
            self.frame = 0
        self.image = self.images[self.frame]


def main():
    pygame.init()
    size = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    game_state = 0 # 0 - main menu, 1 - game, 2 - end screen
    running = True
    frame_number = 0
    selected_item = 0
    max_items = 1
    music_volume = 1
    pygame.display.set_caption("The elder scrolls 0: мужик в лесу")
    caption_font = pygame.font.Font(r"data/fonts/AncientModernTalesPixel.ttf", 60)
    usual_font = pygame.font.Font(r"data/fonts/antiquity-print.ttf", 40)
    default_font = pygame.font.Font(None,40)
    loading_screen(screen,usual_font)
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
            draw_text("The elder scrolls 0:", caption_font, Color("gainsboro"),screen,(480,200),antialias=False,centerX=True)
            draw_text("FOREST", caption_font, Color("firebrick2"),screen,(480,300),antialias=False,centerX=True)
            draw_text("-> Start game" if selected_item == 0 else "Start game", caption_font, Color("firebrick2") if selected_item == 0 else Color("gainsboro"), screen, (480, 500), centerX=True)
            draw_text("-> Exit" if selected_item == 1 else "Exit", caption_font, Color("firebrick2") if selected_item == 1 else Color("gainsboro"), screen, (480, 600), centerX=True)
            pygame.display.flip()
            frame_number = frame_number + 1 if frame_number < 60 else 0
            clock.tick(FPS)
        if game_state == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill("white")
            draw_text("Game will be here", default_font, Color("black"), screen, (480, 480), centerX=True)
            pygame.display.flip()
        if game_state == 2:
            pass

if __name__ == '__main__':
    main()
