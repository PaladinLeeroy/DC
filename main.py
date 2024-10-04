#подключение библиотек
import pygame
import math
import sys

#инициализация Pygame
pygame.init()
clock = pygame.time.Clock()
tick = 0
#инициализация цветов для игры
WHITE = (255, 255, 255)
RED = (255, 0, 0)
#переменная для мода редактирования
redMod = 0

stateGame = 'menu'
#класс "Игрок" - переменные и методы для объекта игрока
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.max_health = 150
        self.hp = 150
        #состояние персонажа - режим ожидания, бег в разные стороны, атака, смерть
        #0 - idle, 1 - run right, 2 - run bottom, 3 - left, 4 - up, 23 - bottom left; 15 - attack left; 100 - death animate
        self.state = 0
        self.spriteOffset = 68
        self.tileWidth = 192
        self.tileHeight = 192

        self.isAttack = False

        self.spriteCount = 6
        self.currentSprite = 0
        self.currentSpriteAttack = 0

        self.lastPos = 's'
        self.currentPos = 's'
        self.noneGoSpriteFormS = ['rbpl', 'rbpbl', 'rbpul', ' ']
        self.noneGoSpriteFormG = ['rbpl', 'rbpbl', 'rbpul', ' ', 'sbl', 'sl', 'sul']
        #загрузка листа спрайтов
        self.image = pygame.image.load('assets/player/warrior/yellow/Warrior_Yellow_with_dead.png')
        self.flipImage = pygame.transform.flip(self.image, True, False)

        self.rectColl = pygame.Surface((60, 60))
        self.rectColl.fill(WHITE)
        self.rect = self.rectColl.get_rect()

        self.attackRect = [pygame.Surface((60, 100)), pygame.Surface((100, 60)), pygame.Surface((60, 100)), pygame.Surface((100, 60))]
        self.attackRect[0].fill(WHITE)
        self.attackRect[1].fill(WHITE)
        self.attackRect[2].fill(WHITE)
        self.attackRect[3].fill(WHITE)
        self.attackRect = [self.attackRect[0].get_rect(), self.attackRect[1].get_rect(), self.attackRect[2].get_rect(), self.attackRect[3].get_rect()]
    #метод движения персонажа
    def move(self, dx, dy):
        if may_play():
            self.x += dx * self.speed
            self.y += dy * self.speed
            self.rect[0] = self.x + 60
            self.rect[1] = self.y + 70
    #метод для отрисовки персонажа
    def draw(self, x, y):
        self.draw_hp()
        self.collision_on_enemies()
        if self.state == 100:
            if self.currentSprite < self.spriteCount - 1:
                screen.blit(self.image, (x, y), area=(animate_x(self, 192), self.animate_y(), 192, 192))
                self.currentSprite += 1
            else:
                screen.blit(self.image, (x, y), area=(192 * 5, 960, 192, 192))  # Последний кадр анимации
        elif self.isAttack:
            self.attack(x, y)
        elif self.state == 3 or self.state == 4 or self.state == 23:
            screen.blit(self.flipImage, (x, y), area=(animate_x(self, 192), self.animate_y(), 192, 192))
        elif self.state == 1 or self.state == 2 or self.state == 0:
            screen.blit(self.image, (x, y), area=(animate_x(self, 192), self.animate_y(), 192, 192))
    #метод для redMod, рисует белый прямоугольник в ногах персонажа, для отображения того где он находится
    def drawRectLegs(self, x, y):
        if redMod == 1:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(x + self.spriteOffset, y + self.spriteOffset + 45, 55, 25))
    #метод, нужный для возврата позиции по Y из листа спрайтов в зависимости от состояния
    def animate_y(self):
        if self.state == 0:
            return 0 #позиция в спрайтшитах по Y для разделения анимаций
        elif self.state == 100:
            return 960
        elif self.state == 1 or self.state == 2 or self.state == 3 or self.state == 4 or self.state == 23:
            return 192
        elif self.state == 15:
            return 576
    #метод, создающий логику атаки персонажа
    def attack(self, x, y):
        if may_play():
            self.attackRect[0][0] = self.x + 122
            self.attackRect[0][1] = self.y + 40

            self.attackRect[1][0] = self.x + 55
            self.attackRect[1][1] = self.y + 110

            self.attackRect[2][0] = self.x + 10
            self.attackRect[2][1] = self.y + 30

            self.attackRect[3][0] = self.x + 40
            self.attackRect[3][1] = self.y + 20
            if redMod == 1:
                if self.state == 15 or self.state == 50:
                    pygame.draw.rect(screen, WHITE, self.attackRect[0])
                elif self.state == 25:
                    pygame.draw.rect(screen, WHITE, self.attackRect[1])
                elif self.state == 35:
                    pygame.draw.rect(screen, WHITE, self.attackRect[2])
                elif self.state == 45:
                    pygame.draw.rect(screen, WHITE, self.attackRect[3])
            self.attack_animate(x, y)
    #анимация атаки персонажа
    def attack_animate(self, x, y):
        if may_play():
            if tick % 6 == 0:
                self.currentSpriteAttack += 1
            if self.currentSpriteAttack == self.spriteCount:
                self.currentSpriteAttack = 0
                self.isAttack = False
            if self.state == 50:
                screen.blit(self.image, (x, y), area=(self.currentSpriteAttack * 192, 2 * 192, 192, 192))
            elif self.state == 15:
                screen.blit(self.image, (x, y), area=(self.currentSpriteAttack * 192, 2 * 192, 192, 192))
            elif self.state == 35:
                screen.blit(self.flipImage, (x, y), area=(self.currentSpriteAttack * 192, 2 * 192, 192, 192))
            elif self.state == 45:
                screen.blit(self.image, (x, y), area=(self.currentSpriteAttack * 192, 4 * 192, 192, 192))
            elif self.state == 25:
                screen.blit(self.image, (x, y), area=(self.currentSpriteAttack * 192, 3 * 192, 192, 192))

    #столкновение меча персонажа(на самом деле прямоугольника, который находится в той стороне, куда атакует персонаж) с каждым врагом
    def collision_attack(self, enemies):
        for i in enemies:
            if self.state == 15 or self.state == 50:
                is_collide = self.attackRect[0].colliderect(i.rect)
            elif self.state == 25:
                is_collide = self.attackRect[1].colliderect(i.rect)
            elif self.state == 35:
                is_collide = self.attackRect[2].colliderect(i.rect)
            elif self.state == 45:
                is_collide = self.attackRect[3].colliderect(i.rect)
            if is_collide:
                i.get_hit()

    #столкновение персонажа и каждого противника
    def collision_on_enemies(self):
        if may_play():
            for i in enemies:
                is_collide = self.rect.colliderect(i.rect)
                if is_collide:
                    self.hp -= 0.5
                    if self.hp <= 0:
                        self.death()

    #гибель героя от атак противника
    def death(self):
        self.state = 100
        self.currentSprite = 0
        game.draw_lose_pole()

    #отрисовка полоски здоровья персонажа
    def draw_hp(self):
        pygame.draw.rect(screen, RED, (20, 20, (self.hp * 0.75) * 2, 20))
        pygame.draw.rect(screen, WHITE, (20, 20, (self.max_health * 0.75) * 2, 20), 3)

    #метод для определения на какой поверхности находится герой и предыдущая позиция героя (песок, лесенка, трава)
    def player_pos(self):
        posx = math.floor((self.x + self.spriteOffset + 28) / first_map.tileWidth)
        posy = math.floor((self.y + self.spriteOffset + 65 + 12) / first_map.tileWidth)
        if posy == 12:
            posy = 11
        if first_map.firstMap[posy][posx] != self.currentPos:
            self.lastPos = self.currentPos
        self.currentPos = first_map.firstMap[posy][posx]

    #метод, нужен для огрничения ходьбы персонажа по поверхности воды, когда его предыдущей позицией был песок
    def change_posS(self):
        for i in self.noneGoSpriteFormS:
            if ((self.lastPos == 's'
                or self.lastPos == 'su'
                or self.lastPos == 'sb'
                or self.lastPos == 'sl'
                or self.lastPos == 'sr'
                or self.lastPos == 'sbr'
                or self.lastPos == 'sbl'
                or self.lastPos == 'sur'
                or self.lastPos == 'sul'
            )) and self.currentPos == i:
                if self.state == 1:
                    self.x -= 1
                elif self.state == 2:
                    self.y -= 1
                elif self.state == 3:
                    self.x += 1
                elif self.state == 4:
                    self.y += 1
                self.lastPos = 's'
                return False
        return True

    ##метод, нужен для огрничения ходьбы персонажа по поверхности воды, когда его предыдущей позицией была трава
    def change_posG(self):
        for i in self.noneGoSpriteFormG:
            if ((self.lastPos == 'g'
                  or self.lastPos == 'gu'
                  or self.lastPos == 'gb'
                  or self.lastPos == 'gl'
                  or self.lastPos == 'gr'
                  or self.lastPos == 'gbr'
                  or self.lastPos == 'gbl'
                  or self.lastPos == 'gur'
                  or self.lastPos == 'gul'
            )) and self.currentPos == i:
                if self.state == 1:
                    self.x -= 1
                elif self.state == 2:
                    self.y -= 1
                elif self.state == 3:
                    self.x += 1
                elif self.state == 4:
                    self.y += 1
                self.lastPos = 'g'
                return False
        return True
#"нарезка" тайлов для карты - возвращает аргументы для area по определенным координатам для метода pygame.blit
def tile_slice(x, y, tileWidth, tileHeight):
    return tileWidth * x, tileHeight * y, tileWidth, tileHeight

#изменение размера изображения
def scale_image(image, scale):
    return pygame.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

#класс, описывающий карту тайлов
class TileMap:
    def __init__(self, tileWidth, tileHeight, firstMap, secondMap):
        self.imageFlat = pygame.image.load("assets/Terrain/Ground/Tilemap_Flat.png")
        self.imageFlatElevation = pygame.image.load("assets/Terrain/Ground/Tilemap_Elevation.png")
        self.imageFlatElevationFlip90 = pygame.transform.rotate(self.imageFlatElevation, 90)
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        self.firstMap = firstMap
        self.secondMap = secondMap
        self.water = pygame.image.load("assets/Terrain/Water/Water.png")

        self.spriteCountFoam = 8 - 1
        self.currentSpriteFoam = 0
        self.imageFoam = pygame.image.load("assets/Terrain/Water/Foam/Foam1-sheet.png")

        self.spriteCountTree = 4 - 1
        self.currentSpriteTree = 0
        self.imageTree = pygame.image.load("assets/Resources/Trees/Tree.png")

        self.imageLog = pygame.image.load("assets/Resources/Resources/W_Idle.png")
    #отрисовка карты
    def draw(self):
        for i in range(len(self.firstMap)):
            for j in range(len(self.firstMap[i])):
                screen.blit(self.water, (self.tileWidth * j, self.tileHeight * i))
        for i in range(len(self.firstMap)):
            for j in range(len(self.firstMap[i])):
                if self.firstMap[i][j] != ' ' and self.firstMap[i][j] != 'g' and self.firstMap[i][j] != 's' and self.firstMap[i][j] != 'rbpul' and self.firstMap[i][j] != 'rbpu':
                    #screen.blit(self.imageFoam, ((self.tileWidth * j) - 8, (self.tileHeight * i) - 8), area=(self.animate_x(self.currentSpriteFoam, self.spriteCountFoam), 0, 81, 81))
                    self.animate_foam(i, j)
        for i in range(len(self.firstMap)):
            for j in range(len(self.firstMap[i])):
                if self.firstMap[i][j] == 's':
                    #отрисовка части листа спрайтов по координатам 6, 1, ширина высота тайла
                    screen.blit(self.imageFlat, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(6, 1, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'g':
                    screen.blit(self.imageFlat, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(1, 1, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'gl':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(0, 1, self.tileWidth, self.tileHeight))
                    screen.blit(self.imageFlat, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(0, 1, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'gr':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(2, 1, self.tileWidth, self.tileHeight))
                    screen.blit(self.imageFlat, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(2, 1, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'gb':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(1, 2, self.tileWidth, self.tileHeight))
                    screen.blit(self.imageFlat, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(1, 2, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'gu':
                    screen.blit(self.imageFlat, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(1, 0, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'gul':
                    screen.blit(self.imageFlat, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(0, 0, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'gur':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(2, 0, self.tileWidth, self.tileHeight))
                    screen.blit(self.imageFlat, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(2, 0, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'gbr':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(2, 2, self.tileWidth, self.tileHeight))
                    screen.blit(self.imageFlat, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(2, 2, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'gbl':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(0, 1, self.tileWidth, self.tileHeight))
                    screen.blit(self.imageFlat, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(0, 2, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'sb':
                    screen.blit(self.imageFlat, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(6, 2, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'su':
                    screen.blit(self.imageFlat, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(6, 0, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'sl':
                    screen.blit(self.imageFlat, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(5, 1, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'sr':
                    screen.blit(self.imageFlat, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(7, 1, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'sul':
                    screen.blit(self.imageFlat, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(5, 0, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'sur':
                    screen.blit(self.imageFlat, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(7, 0, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'sbl':
                    screen.blit(self.imageFlat, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(5, 2, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'sbr':
                    screen.blit(self.imageFlat, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(7, 2, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'reb1':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(0, 7, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'reb2':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(1, 7, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'reb3':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(2, 7, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'freb1':
                    screen.blit(pygame.transform.rotate(self.imageFlatElevation, 270), (self.tileWidth * j, self.tileHeight * i), area=tile_slice(0, 2, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'freb2':
                    screen.blit(pygame.transform.rotate(self.imageFlatElevation, 270), (self.tileWidth * j, self.tileHeight * i), area=tile_slice(0, 1, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'freb3':
                    screen.blit(pygame.transform.rotate(self.imageFlatElevation, 270), (self.tileWidth * j, self.tileHeight * i), area=tile_slice(0, 0, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'rbpul':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(0, 0, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'rbpl':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(0, 1, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'rbpbl':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(0, 2, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'reb1':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(0, 7, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'reb2':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(1, 7, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'reb3':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(2, 7, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'rbpul':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(0, 0, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'rbpl':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(0, 1, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'rbpr':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(2, 1, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'rbpbl':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(0, 2, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'rbpbr':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(2, 2, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'rbpm':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(1, 1, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'rbpb':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(1, 2, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'rbpu':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(1, 0, self.tileWidth, self.tileHeight))
                elif self.firstMap[i][j] == 'rbpur':
                    screen.blit(self.imageFlatElevation, (self.tileWidth * j, self.tileHeight * i), area=tile_slice(2, 0, self.tileWidth, self.tileHeight))
    #отрисовка второго слоя карты, в данном случае деревья или бревна
    def draw_second(self):
        for i in range(len(self.secondMap)):
            for j in range(len(self.secondMap[i])):
                if self.secondMap[i][j] == 't':
                    self.animate_trees(i, j)
                if self.secondMap[i][j] == 'log':
                    screen.blit(self.imageLog, (self.tileWidth * j, self.tileHeight * i))
    #анимация биения волн о скалы
    def animate_foam(self, i, j):
        if tick % 10 == 0:
            self.currentSpriteFoam += 1
        if self.currentSpriteFoam == self.spriteCountFoam:
            self.currentSpriteFoam = 0
        x = 81 * self.currentSpriteFoam
        screen.blit(self.imageFoam, ((self.tileWidth * j) - 8, (self.tileHeight * i) - 8),
                    area=(x, 0, 81, 81))
    #анимация движения деревьев от ветра
    def animate_trees(self, i, j):
        if tick % 10 == 0:
            self.currentSpriteTree += 1
        if self.currentSpriteTree == self.spriteCountTree:
            self.currentSpriteTree = 0
        x = 192 * self.currentSpriteTree
        screen.blit(self.imageTree, (self.tileWidth * j, self.tileHeight * i), area=(x, 0, 192, 192))

#функция возвращающая отступ по X для анимации объектов
def animate_x(obj, sizeTile):
    if tick % 6 == 0:
        obj.currentSprite += 1
    if obj.currentSprite == obj.spriteCount:
        obj.currentSprite = 0
    return sizeTile * obj.currentSprite
#сделать диалоги
#класс для неигровых персонажей
class Npc:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.tileWidth = 192
        self.tileHeight = 192
        if type == 'torch':
            self.max_health = 120
            self.hp = 90

        self.currentSprite = 0
        self.spriteCount = 7 - 1
        # параметры для колизии npc
        self.npc_coll = [['torch', 2.8, 2.8, 60, 60]]

        self.imageTorch = pygame.image.load("assets/Factions/Goblins/Troops/Torch/Yellow/Torch_Yellow.png")

        self.coll = pygame.Surface((self.tileWidth / self.npc_coll[0][1], self.tileHeight / self.npc_coll[0][2]))
        self.coll.fill(WHITE)
        self.rect = self.coll.get_rect()
    #отрисовка неигровых персонажей
    def draw(self):
        self.draw_hp()
        if redMod == 1:
            pygame.draw.rect(screen, WHITE, (self.rect))
        screen.blit(self.imageTorch, (self.x, self.y), area=(animate_x(self, 192), 0, self.tileWidth, self.tileHeight))

    # отрисовка здоровья неигровых персонажей
    def draw_hp(self):
        pygame.draw.rect(screen, RED, (self.x + (self.tileWidth * 0.5) / 2, self.y + 40, self.hp * 0.75, 14))
        pygame.draw.rect(screen, WHITE, (self.x + (self.tileWidth * 0.5) / 2, self.y + 40, self.max_health * 0.75, 14), 2)
        pass


#сделать атаку факелом
#зачатки класса для описания npc с факелом в руках
class Torch(Npc):
    def exlode(self):
        pass

class Enemy:
    def __init__(self, x, y, type, typeMove):
        self.x = x
        self.y = y
        self.type = type
        self.typeMove = typeMove
        self.speed = typeMove[4]
        self.state = typeMove[5]
        self.tileWidth = 96
        self.tileHeight = 96
        if type == 'mechFly':
            self.max_health = 60
            self.hp = 60

        self.currentSprite = 0
        self.spriteCount = 4 - 1

        self.sprites = [[0, 3]]
        self.enemies_coll = [['mechFly', 2.8, 2.8, 25, 15]]

        self.imageMechFly = [
            pygame.image.load("assets/Factions/Tech/Enemies/mechFlyIdle.png"),
            pygame.image.load("assets/Factions/Tech/Enemies/mechFlyShoot.png"),
            pygame.image.load("assets/Factions/Tech/Enemies/mechFlyDeath.png")
        ]
        self.imageMechTroops = [
            pygame.image.load("assets/Factions/Tech/Enemies/mechTroopsRun.png")
        ]
        self.imageMechTroopsFlip = [
            pygame.transform.flip(self.imageMechTroops[0], True, False)
        ]
        self.imageMechFlyFlip = [
            pygame.transform.flip(self.imageMechFly[0], True, False),
            pygame.transform.flip(self.imageMechFly[1], True, False),
            pygame.transform.flip(self.imageMechFly[2], True, False)
        ]

        self.coll = pygame.Surface((self.tileWidth / 2, self.tileHeight / 2))
        self.coll.fill(WHITE)
        self.rect = self.coll.get_rect()
    #отрисовка противников
    def draw(self):
        self.draw_hp()
        if redMod == 1:
            pygame.draw.rect(screen, WHITE, (self.rect))
        if self.state == 1:
            screen.blit(self.imageMechFly[0], (self.x, self.y), area=(animate_x(self, 96), 0, self.tileWidth, self.tileHeight))
        elif self.state == 3:
            screen.blit(self.imageMechFlyFlip[0], (self.x, self.y), area=(animate_x(self, 96), 0, self.tileWidth, self.tileHeight))
        elif self.state == 5:
            screen.blit(self.imageMechFlyFlip[2], (self.x, self.y), area=(animate_x(self, 96), 0, self.tileWidth, self.tileHeight))
            if self.currentSprite > 5:
                self.state = 6
                self.x = -1000
    #отрисовка здоровья противников
    def draw_hp(self):
        if self.state == 1 or self.state == 3:
            pygame.draw.rect(screen, RED, (self.x + (self.tileWidth * 0.5) / 2, self.y, self.hp * 0.75, 12))
            pygame.draw.rect(screen, WHITE, (self.x + (self.tileWidth * 0.5) / 2, self.y, self.max_health * 0.75, 12), 2)
    #движение противников
    def move(self):
        if self.state == 1 or self.state == 3:
            if self.typeMove[0] == 'left_right':
                if self.typeMove[3] == False:
                    self.x += self.speed
                    self.typeMove[1] += self.speed
                    if self.typeMove[1] > self.typeMove[2]:
                        self.typeMove[3] = True
                        self.state = 3
                else:
                    self.x -= self.speed
                    self.typeMove[1] -= self.speed
                    if self.typeMove[1] < 0:
                        self.typeMove[3] = False
                        self.state = 1
            self.rect[0] = self.x + self.enemies_coll[0][3]
            self.rect[1] = self.y + self.enemies_coll[0][4]
    #метод для полученя урона противником
    def get_hit(self):
        self.hp -= 1.2
        if self.hp <= 0:
            self.destroi()
    #метод для уничтожения противника
    def destroi(self):
        self.state = 5
        self.spriteCount = 7
        self.currentSprite = 0
        del self

# size - 20x12
# s - sand middle
# g - grass middle
# sb - sand bottom
# sl - sand left
# sr - sand right
# su - sand up

# reb1, reb2, reb3 - rock elevation big 1-3
# rbpbl - rock big platform bottom left
# rbpl - rock big platform left
# rbpul - rock big platform up left
# rbpm - rock big platform middle
# rbpb - rock big platform bottom
#первый слой карты
first_level_tiles = [
    [' ', ' ', 'sul', 'su', 'su', 'su', 'su', 'su', 'su', 'su', 'su', 'sur', ' ', ' ', 'gul', 'gu', 'gu', 'gu', 'gu', 'gur'],
    [' ', ' ', 'sl', 's', 's', 's', 's', 's', 's', 's', 's', 's', 'su', 'freb3', 'gl', 'g', 'g', 'g', 'g', 'gr'],
    ['sul', 'su', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 'freb2', 'gl', 'g', 'g', 'g', 'g', 'gr'],
    ['sl', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 'freb2', 'gl', 'g', 'g', 'g', 'g', 'gr'],
    ['sl', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 'freb2', 'gl', 'g', 'g', 'g', 'g', 'gr'],
    ['sl', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 'freb1', 'gbl', 'gb', 'gb', 'gb', 'gb', 'gbr'],
    ['sl', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 'reb1', 'reb2', 'reb2', 'reb2', 'reb2', 'reb3'],
    ['sl', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 'sr'],
    ['sl', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 'sr'],
    ['sl', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 'sb', 'sb', 'sb', 'sbr'],
    ['sl', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 'sbr', ' ', ' ', ' ', ' '],
    ['sbl', 'sb', 'sb', 'sb', 'sb', 'sb', 'sb', 'sb', 'sb', 'sb', 'sb', 'sb', 'sb', 'sb', 'sbr', ' ', ' ', ' ', ' ', ' ']
]
#второй стой карты
second_level_tiles = [
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 't', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 't', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', 'log', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'log', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
]

#определение объектов классов TileMap и Player
first_map = TileMap(64, 64, first_level_tiles, second_level_tiles)
player = Player(100, 100)
#определение объекта класса Torch
npcs = [Torch(400, 600, 'torch')]

#определение противников с параметрами - массива объектов класса Enemy
enemies = [
    #x, y, тип, параметры движения
    Enemy(900, 200, 'mechFly', ['left_right', 0, 200, False, 2, 1]),
    Enemy(850, 400, 'mechFly', ['left_right', 0, 150, True, 2, 1]),
    Enemy(600, 700, 'mechFly', ['left_right', 0, 40, True, 2, 1]),
    Enemy(700, 500, 'mechFly', ['left_right', 100, 200, True, 2, 1]),
]

#Установка размеров окна
screen_width = 1280
screen_height = 768
#инициализируется окно программы
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("ATTACK OF THE IRONS")

#класс содержащий методы отрисовки текста, проверки победы
class Game:
    def __init__(self):
        #инициализация параметров шрифта и кнопок
        pygame.font.init()
        self.font_menu_path = "assets/fonts/Keleti-Regular.ttf"
        self.font = pygame.font.Font(self.font_menu_path, 40)
        self.font_logo = pygame.font.Font(self.font_menu_path, 120)
        self.font_win_path = "assets/fonts/Font Over.otf"
        self.font_win = pygame.font.Font(self.font_win_path, 25)
        self.menu_button_color = '#5A5C3E'
        self.win_font_color = '#e0461f'
        self.button_go_menu_image = pygame.image.load('assets/UI/buttons/Button_Disable_3Slides.png')
        self.image_for_font_win = scale_image(pygame.image.load("assets/UI/Buttons/Button_Hover_9Slides.png"), 1.6)
        self.button_win_rect = pygame.Rect(640 - 134, 355, 270, 76)
        self.enemies_death = [0]

        for i in range(len(enemies) - 1):
            self.enemies_death.append(1)
        self.win = False
        self.click1 = False
        self.click = False
        self.mx, self.my = pygame.mouse.get_pos()
    #отрисовка текста
    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    #проверка победы
    def check_win(self):
        for i in range(len(enemies)):
            if enemies[i].state == 6:
                self.enemies_death[i] = 2
        if len(set(self.enemies_death)) == 1:
            #print("WIN!!!")
            self.win = True
            player.state = 0
            self.draw_win_pole()
    #отрисовка поля победы
    def draw_win_pole(self):
        screen.blit(self.image_for_font_win, (1280/2 - (192*1.6)/2, 200))
        self.draw_text('Вы выйграли', self.font_win, self.menu_button_color, screen, 530, 240)
        screen.blit(self.button_go_menu_image, (1280/2 - 192/2, 400))
        self.draw_text('Выход', self.font_win, self.menu_button_color, screen, 585, 420)
        self.event_click_game()

    # отрисовка поля поражения
    def draw_lose_pole(self):
        screen.blit(self.image_for_font_win, (1280/2 - (192*1.6)/2, 200))
        self.draw_text('Вы проиграли', self.font_win, self.menu_button_color, screen, 530, 240)
        screen.blit(self.button_go_menu_image, (1280/2 - 192/2, 400))
        self.draw_text('Выход', self.font_win, self.menu_button_color, screen, 585, 420)
        self.event_click_game()
    #метод для событий кликов по кнопкам
    def event_click_game(self):
        self.mx, self.my = pygame.mouse.get_pos()
        if self.button_win_rect.collidepoint((self.mx, self.my)):
            if self.click1:
                pygame.quit()
                sys.exit()

        self.click1 = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click1 = True

#класс для описывающий отображение фона, кнопок, логотипа в меню
class Menu(Game):
    def __init__(self):
        self.image = pygame.image.load('assets/UI/bg.png')
        self.button_image = scale_image(pygame.image.load('assets/UI/buttons/Button_Disable_3Slides.png'), 1.5)
        self.button1_xy = [640-144, 250]
        self.button2_xy = [640-144, 350]
        self.button1_rect = pygame.Rect(640-134, 255, 270, 76)
        self.button2_rect = pygame.Rect(640-134, 355, 270, 76)

        self.logo_image = pygame.image.load('assets/logo.png')
        self.logo_image = scale_image(self.logo_image, 0.25)
        self.music_menu_path = "assets/music/music_menu.mp3"
        self.music_win_path = "assets/music/music_win.mp3"
        music = pygame.mixer.music.load(self.music_menu_path)
        pygame.mixer.music.play(-1, 0.0, 0)

        super().__init__()
    #отрисовка картинки игры и вызов метода для отрисовки кнопок
    def draw_and_event(self):
        screen.blit(self.image, (0, 0))
        self.draw_button()
    #отрисовка кнопок
    def draw_button(self):
        screen.blit(self.button_image, (self.button1_xy))
        screen.blit(self.button_image, (self.button2_xy))
        self.draw_text('Играть', self.font, self.menu_button_color, screen, 590, 275)
        self.draw_text('Выход', self.font, self.menu_button_color, screen, 594, 373)
        self.draw_text('ATTACK OF THE IRONS', self.font_logo, self.menu_button_color, screen, 200, 50)
        self.event_click()
    #переделать в метод главного класса
    #метод событий нажатия на кнопки
    def event_click(self):
        self.mx, self.my = pygame.mouse.get_pos()
        if self.button1_rect.collidepoint((self.mx, self.my)):
            if self.click:
                play_game()
        if self.button2_rect.collidepoint((self.mx, self.my)):
            if self.click:
                pygame.quit()
                sys.exit()

        self.click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True

#функция, которая возвращает значение True или False - можно ли нажимать клавиши на клавиатуре (при победе или гибели)
def may_play():
    if player.state != 100 and game.win == False:
        return True
    else:
        return False

#запуск главного меню
def main_menu():
    while in_menu:
        menu.draw_and_event()
        pygame.display.update()

#запуск игры после нажатия кнопки в меню
def play_game():
    global in_menu
    in_menu = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        global tick
        tick += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #отрисовка карты
        first_map.draw()
        first_map.draw_second()
        #считывание клавиш, движение и атака персонажа
        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        if may_play():
            if player.change_posS():
                if keys[pygame.K_SPACE] and keys[pygame.K_a]:
                    player.state = 35
                    player.isAttack = True
                elif keys[pygame.K_SPACE] and keys[pygame.K_d]:
                    player.state = 15
                    player.isAttack = True
                elif keys[pygame.K_SPACE] and keys[pygame.K_w]:
                    player.state = 45
                    player.isAttack = True
                elif keys[pygame.K_SPACE] and keys[pygame.K_s]:
                    player.state = 25
                    player.isAttack = True
                elif keys[pygame.K_SPACE]:
                    player.state = 50
                    player.isAttack = True
                elif keys[pygame.K_w]:
                    if player.isAttack == False:
                        player.state = 4
                    if player.y + player.speed + 64 > 0:
                        dy -= 1
                elif player.isAttack == False:
                    player.state = 0
                if keys[pygame.K_a]:
                    if player.isAttack == False:
                        player.state = 3
                    if player.x + player.speed + 64 > 0:
                        dx -= 1
                if keys[pygame.K_s]:
                    if player.isAttack == False:
                        player.state = 2
                    if (player.y + player.speed) + 128 < screen.get_height():
                        dy += 1
                if keys[pygame.K_d]:
                    if player.isAttack == False:
                        player.state = 1
                    if (player.x + player.speed) + 128 < screen.get_width():
                        dx += 1
                if keys[pygame.K_s] and keys[pygame.K_a]:
                    player.state = 23

        if redMod == 1:
            pygame.draw.rect(screen, WHITE, (player.rect))
        #отрисовка персонажа, движение персонажа
        player.draw(player.x, player.y)
        player.player_pos()
        player.move(dx, dy)
        #отрисовка npc (сделать движение и диалоги)
        for obj in npcs:
            obj.draw()
        #отрисовка и движение противников
        for obj in enemies:
            obj.move()
            obj.draw()

        if player.isAttack:
            player.collision_attack(enemies)
        # Обновление экрана
        game.check_win()
        pygame.display.update()
        clock.tick(60)
#создание объекта класса Game и Menu
game = Game()
menu = Menu()
in_menu = True

#начало программы - вызов главного меню
main_menu()
