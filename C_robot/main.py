from sprites import *
from config import *
from spawn import game_map
import sys
import pygame

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('zpix.ttf', 32)
        self.running = True

        self.character_spritesheet = Spritesheet('img/sprite.png')
        self.terrain_spritesheet = Spritesheet('img/sprite.png')
        self.game_background = pygame.image.load('img/background.png')
        self.robot = []
        self.teleport = TELEPORT_DEVICES
        self.game_result = 0

    def createTilemap(self):
        for i, row in enumerate(game_map):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == 'B':
                    Block(self, j, i)
                if column == 'P':
                    self.player = Player(self, j, i)
                if column == 'R':
                    self.robot.append(Robot(self, j, i))



    def new(self):
        # a new game starts
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.createTilemap()


    def events(self):
        # game loop events
        for event in pygame.event.get():
            self.update(event)
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False



    def update(self, event):
        # game loop updates
        self.all_sprites.update(event)
        if self.game_result != 0:
            self.playing = False


    def draw(self):
        # game loop draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        self.font2 = pygame.font.Font('zpix.ttf', 18)

        newscreen = self.font2.render('teleports remaining: '+str(self.teleport), True, WHITE)
        newscreen_rect = newscreen.get_rect(x=WIN_WIDTH-390, y=10)
        self.screen.blit(newscreen, newscreen_rect)

        newscreen = self.font2.render('Enter move or Close the window:', True, WHITE)
        newscreen_rect = newscreen.get_rect(x=WIN_WIDTH-390, y=34)
        self.screen.blit(newscreen, newscreen_rect)

        newscreen = self.font2.render('(Q)(W)(E)', True, WHITE)
        newscreen_rect = newscreen.get_rect(x=WIN_WIDTH-390, y=56)
        self.screen.blit(newscreen, newscreen_rect)

        newscreen = self.font2.render('(A)(S)(D)', True, WHITE)
        newscreen_rect = newscreen.get_rect(x=WIN_WIDTH-390, y=78)
        self.screen.blit(newscreen, newscreen_rect)

        newscreen = self.font2.render('(Z)(X)(C)', True, WHITE)
        newscreen_rect = newscreen.get_rect(x=WIN_WIDTH-390, y=100)
        self.screen.blit(newscreen, newscreen_rect)


        self.clock.tick(FPS)
        pygame.display.update()


    def main(self):
        # game loop
        while self.playing:
            self.events()
            self.draw()
            self.screen.blit(self.game_background, (0, 0))
        self.running = False



    def game_over(self):
        g.end_screen()
        g.thank_screen()
        pass


    def intro_screen(self):
        intro = True

        title = self.font.render('Maze game', True, BLACK)
        title_rect = title.get_rect(x=WIN_WIDTH//2-100, y=WIN_HEIGHT//2-100)

        play_button = Button(WIN_WIDTH//2-70, WIN_HEIGHT//2-30, 100, 50, WHITE, BLACK, 'Play', 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.fill((178, 236, 237))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
    def end_screen(self):
        end = True

        if self.game_result == 1:
            title = self.font.render('You have been caught by a robot!', True, BLACK)
            title_rect = title.get_rect(x=WIN_WIDTH//2-250, y=WIN_HEIGHT//2-100)
        elif self.game_result == 2:
            title = self.font.render('All the robots have crashed into each other and you lived to tell the tale! Good job!', True, BLACK)
            title_rect = title.get_rect(x=WIN_WIDTH//2-700, y=WIN_HEIGHT//2-100)

        while end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = False
                    self.running = False

            
            self.screen.fill((178, 236, 237))
            self.screen.blit(title, title_rect)
            self.clock.tick(FPS)
            pygame.display.update()
    def thank_screen(self):
        thank = True

        title = self.font.render('Thanks for playing!', True, BLACK)
        title_rect = title.get_rect(x=WIN_WIDTH//2-200, y=WIN_HEIGHT//2-100)

        while thank:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    thank = False
                    self.running = False

            
            self.screen.fill((178, 236, 237))
            self.screen.blit(title, title_rect)
            self.clock.tick(FPS)
            pygame.display.update()


g = Game()
g.intro_screen()
g.new()

while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()