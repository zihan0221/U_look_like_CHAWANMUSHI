import pygame
from config import *
import math
import random
from spawn import randomXY, game_map, playerLocation

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha() 

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'

        self.image = self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self, event):
        self.movement(event)

        playerLocation[0] += self.x_change
        playerLocation[1] += self.y_change

        self.rect.x += self.x_change * TILESIZE
        self.rect.y += self.y_change * TILESIZE

        self.x_change = 0
        self.y_change = 0

    def movement(self, event):
        if event.type == pygame.KEYUP:
            flag = 1
            if event.key == pygame.K_a:
                self.x_change -= PLAYER_SPEED
            elif event.key == pygame.K_d:
                self.x_change += PLAYER_SPEED
            elif event.key == pygame.K_w:
                self.y_change -= PLAYER_SPEED
            elif event.key == pygame.K_x:
                self.y_change += PLAYER_SPEED
            elif event.key == pygame.K_q:
                self.y_change -= PLAYER_SPEED
                self.x_change -= PLAYER_SPEED
            elif event.key == pygame.K_e:
                self.y_change -= PLAYER_SPEED
                self.x_change += PLAYER_SPEED
            elif event.key == pygame.K_z:
                self.y_change += PLAYER_SPEED
                self.x_change -= PLAYER_SPEED
            elif event.key == pygame.K_c:
                self.y_change += PLAYER_SPEED
                self.x_change += PLAYER_SPEED
            elif event.key == pygame.K_t:
                if self.game.teleport > 0:
                    (tx, ty) = randomXY(game_map, [])
                    (self.rect.x, self.rect.y) = (tx * TILESIZE, ty * TILESIZE)
                    self.game.teleport -= 1
                else :
                    print('no teleport device')
            else:
                flag = 0

            if game_map[playerLocation[1]+self.y_change][playerLocation[0]+self.x_change] == 'B':
                print('You can\'t go there!!!!')
                flag = 0
                self.x_change = 0
                self.y_change = 0
                # for i in range(MAP_HEIGHT):
                #   for j in range(MAP_WIDTH):
                #       print(game_map[i][j], end='')
                # print()

            cnt = 0
            if flag:
                for i in self.game.robot:
                    i.movement(event)
                    if abs(i.rect.x-i.game.player.rect.x)<32 and abs(i.rect.y-i.game.player.rect.y)<32:
                        self.game.game_result = 1
                    if not i.status:
                        cnt += 1
            if cnt == TOTAL_ROBOT:
                self.game.game_result = 2


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(98, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(131, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Robot(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = ROBOT_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.status = True

        self.x_change = 0
        self.y_change = 0

        self.image = self.game.terrain_spritesheet.get_sprite(33, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self, event):
        if not self.status:
            self.image = self.game.terrain_spritesheet.get_sprite(66, 0, self.width, self.height)

        self.rect.x += self.x_change * TILESIZE
        self.rect.y += self.y_change * TILESIZE

        self.x_change = 0
        self.y_change = 0


    def movement(self, event):
        if self.status:
            if self.rect.x < self.game.player.rect.x:
                self.x_change += 1
            elif self.rect.x > self.game.player.rect.x:
                self.x_change -= 1
            elif self.rect.x == self.game.player.rect.x:
                self.x_change = 0

            if self.rect.y < self.game.player.rect.y:
                self.y_change += 1
            elif self.rect.y > self.game.player.rect.y:
                self.y_change -= 1
            elif self.rect.y == self.game.player.rect.y:
                self.y_change  = 0
        cx = self.rect.x + self.x_change * TILESIZE
        cy = self.rect.y + self.y_change * TILESIZE
        for i in self.game.robot:
            if(abs(cx-i.rect.x)<32 and abs(cy-i.rect.y)<32):
                i.status = 0
                self.status = 0
        self.update(event)


class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('zpix.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False