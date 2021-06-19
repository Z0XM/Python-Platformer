import pygame
import os
from Assets.Colors import*
from Assets.Z import*

##------------------------------------------------------------------------------------------------------------------------------------------##
##-----------------------------------------------------------------PLOT---------------------------------------------------------------------##
## Zanta was an extremly powerful old wizard, one in a million. Who used his magical powersto distribute gits to children all around the    ##
## With the help of his deer friends and magical sledge and and a magical bag that he created. But one day all fell off as his bag became   ##
## useless as its magical power ran out. Zanta having no more magic power left to create another one, retired. And over decades he became a ##
## myth and soon a legend. Zanta in his younger days had many freinds as powerful as him called the Elves. But unlike him they didnt have   ##
## an everlasting life. But after a very long time, Someone disguised as elf appeared. Zanta came back from shadows once again and teamed up##
## with few kids and adults to stop the elf from doing evil things which could harm the whole world. Zanta Finally won the battle with the  ##
## death of the elf. Zanta was loved by everyone again. But the elf left something behind.--------------------------------------------------##
##------------------------------------------------------------------------------------------------------------------------------------------##
##                                                                                                                                          ##
##------------------------------------------------------------------------------------------------------------------------------------------##
##--------------------------------------------------------------STAGES----------------------------------------------------------------------##
##---STAGE 1--------------------------------------------------------------------------------------------------------------------------------##
## Zanta is forced to return to the rest world from his ice cave as his cave has been flooded with magical lava.                            ##
## Zanta finds his lost bag.                                                                                                                ##
##---STAGE 2--------------------------------------------------------------------------------------------------------------------------------##
## Zanta runs in city to find the elf.                                                                                                      ##
## Zanta encounters the kids and adults who try to help him.                                                                                ##
##---STAGE 3--------------------------------------------------------------------------------------------------------------------------------##
## Everybody goes into the jungle to find magical deers and sledge.                                                                         ##
## Zanta restores his much of the power and his bag.                                                                                        ##
##---STAGE 4--------------------------------------------------------------------------------------------------------------------------------##
## Everybody finds out the elf.                                                                                                             ##
## Elf is defeated.                                                                                                                         ##
##---STAGE 5--------------------------------------------------------------------------------------------------------------------------------##
## Backstory of clash of the elves and wizards.                                                                                             ##
## Truth Out.                                                                                                                               ##
##------------------------------------------------------------------------------------------------------------------------------------------##
##------------------------------------------------------------------------------------------------------------------------------------------##


##Game Class--------------------------------------------------------------------------------------------------------------------------------##
##------------------------------------------------------------------------------------------------------------------------------------------##
class NewGame:
    def __call__(self):
        #constants -> ALL CAPS
        #others -> First Letters Caps
        info = pygame.display.Info()
        self.SIZE = (info.current_w-600,info.current_h-400)
        self.miniSIZE = (500,500)
        self.Screen = pygame.display.set_mode(self.miniSIZE)
        self.TITLE = 'Z_Platformer'
        self.ICON = pygame.image.load('data/Z.ico')
        pygame.display.set_icon(self.ICON)
        pygame.display.set_caption(self.TITLE)
        self.FPS = 30
        
        self.BG_COLOR = Black
        self.BG_IMG = pygame.image.load('data/Background/BG.png').convert()
        self.Bg_ImgRect = self.BG_IMG.get_rect()
        self.BG_IMG2 = pygame.image.load('data/Background/BG.png')
        self.PLAYER = None
        self.CAMERA = None
        
        self.LEVEL = [] #stores current level map
        self.Level = 1  #indicates which level the player is on
        with open('data/Levels/level.txt', 'r+') as f:
            data = f.read().split(',')
        self.LEVELS = int(data[0]) #total levels
        self.CompletedLevels = int(data[1]) #levels player has completed

        self.MAP_SIZE = None
        self.TILE_SIZE = (36,36)
        self.HORIZONTAL_SCROLL = True
        self.VERTICAL_SCROLL = True

        self.isPaused = False
        self.isOver = False
        self.onLevelMode = False
        self.Gifts = 0

        self.Platform_Sprites = {'platform':pygame.sprite.Group(), 'lava':pygame.sprite.Group(), 'goal':pygame.sprite.Group()   }
        self.Player_Sprites = pygame.sprite.Group()
        self.Collectable_Sprites = {'present':pygame.sprite.Group() }
        self.JustThere_Sprites = [pygame.sprite.Group(), pygame.sprite.Group()]

        self.ButtonColor = Red
        self.ButtonText = Black
        self.ButtonChange = Orange

        self.Tilesets = {'X':pygame.image.load('data/Tilesets/pic (21).png').convert(),
                         'Z':pygame.image.load('data/Tilesets/pic (20).png').convert(),
                         'C':pygame.image.load('data/Tilesets/pic (22).png').convert(),
                         'Y':pygame.image.load('data/Tilesets/pic (24).png').convert(),
                         'T':pygame.image.load('data/Tilesets/pic (23).png').convert(),
                         'U':pygame.image.load('data/Tilesets/pic (25).png').convert(),
                         'F':pygame.image.load('data/Tilesets/pic (34).png').convert(),
                         'B':pygame.image.load('data/Tilesets/pic (34).png').convert(),
                         }

        self.Decorators = {'a':pygame.image.load('data/Decorators/pic (1).png').convert(),
                           'b':pygame.image.load('data/Decorators/pic (2).png').convert(),
                           'c':pygame.image.load('data/Decorators/pic (3).png').convert(),
                           'd':pygame.image.load('data/Decorators/pic (4).png').convert(),
                           'e':pygame.image.load('data/Decorators/pic (5).png').convert(),
                           'f':pygame.image.load('data/Decorators/pic (6).png').convert(),
                           'g':pygame.image.load('data/Decorators/pic (7).png').convert(),
                           'h':pygame.image.load('data/Decorators/pic (8).png').convert(),
                           'i':pygame.image.load('data/Decorators/pic (9).png').convert(),
                           'j':pygame.image.load('data/Decorators/pic (10).png').convert(),
                           'k':pygame.image.load('data/Decorators/pic (11).png').convert()
                           }
        self.DecoratorSize = {'a':(72,72),
                              'b':(64,64),
                              'c':(36,36),
                              'd':(144,72),
                              'e':(72,72),
                              'f':(72,72),
                              'g':(144,72),
                              'h':(120,144),
                              'i':(124,78),
                              'j':(364,280),
                              'k':(228,280)
                           }

        self.sheet = {'Lava':[],'PlayerWalk':[], 'PlayerRun':[], 'PlayerIdle':[], 'PlayerAnimRight':[], 'PlayerAnimIdle':[], 'Present':[]  }
        self.frames = {'Lava':47, 'PlayerWalk':13, 'PlayerRun':11, 'PlayerIdle':16, 'PlayerAnimRight':7, 'PlayerAnimIdle':1, 'Present':13   }
        self.speed = {'Lava':1, 'PlayerWalk':2, 'PlayerRun':1, 'PlayerIdle':2, 'PlayerAnimRight':1, 'PlayerAnimIdle':1, 'Present':1   }
        self.size = {'Lava':self.TILE_SIZE,
                     'PlayerWalk':(3*(25//20)*self.TILE_SIZE[0],2*(25//20)*self.TILE_SIZE[0]),
                     'PlayerRun':(3*(25//20)*self.TILE_SIZE[0],2*(25//20)*self.TILE_SIZE[0]),
                     'PlayerIdle':(3*(25//20)*self.TILE_SIZE[0],2*(25//20)*self.TILE_SIZE[0]),
                     'PlayerAnimRight':(20,20),
                     'PlayerAnimIdle':(20,20),
                     'Present':(40,36)  }
        self.path = {'Lava':'data/Lava/Lava ',
                     'PlayerWalk':'data/Player/Walk ',
                     'PlayerRun':'data/Player/Run ',
                     'PlayerIdle':'data/Player/Idle ',
                     'PlayerAnimRight':'data/Player_anim/Player_anim_right ',
                     'PlayerAnimIdle':'data/Player_anim/Player_anim_idle ',
                     'Present':'data/Decorators/Anims/Present '   }
        for key in ('Lava', 'PlayerWalk', 'PlayerRun', 'PlayerIdle', 'PlayerAnimRight', 'PlayerAnimIdle','Present'):
            for pos in range(1,self.frames[key]+1):
                self.sheet[key].append(pygame.transform.scale(pygame.image.load(self.path[key] + f'({pos}).png'), self.size[key]))
        
        self.Start()

    def Display(self):
        self.Screen.blit(self.BG_IMG, self.Bg_ImgRect.topleft)
        for group in self.Platform_Sprites.values():
            for sprite in group:
                self.Screen.blit(sprite.image, self.CAMERA.apply(sprite))
        for group in self.JustThere_Sprites:
            for sprite in group:
                self.Screen.blit(sprite.image, self.CAMERA.apply(sprite))
        for sprite in self.Player_Sprites:
            self.Screen.blit(sprite.image, self.CAMERA.apply(sprite))
        for group in self.Collectable_Sprites.values():
            for sprite in group:
                self.Screen.blit(sprite.image, self.CAMERA.apply(sprite))

        #pygame.draw.rect(self.Screen, Red, self.PLAYER.rect.move(self.CAMERA.rect.topleft), 1) #to showcase hitbox and rect of player
        #pygame.draw.rect(self.Screen, Yellow, self.PLAYER.hitbox.move(self.CAMERA.rect.topleft), 1)
        pygame.display.update()

    def Update(self):
        self.Player_Sprites.update()
        self.CAMERA.update(self.PLAYER)
        self.PLAYER.UpdateRect()
        if self.PLAYER.isOn(self.Platform_Sprites['lava']): self.isOver = True
        for sprite in self.Collectable_Sprites['present']:
            if self.PLAYER.rect_collision(self.PLAYER, sprite, True):
                self.Gifts += 1

    def ClearSprites(self):
        for key in self.Platform_Sprites:
            self.Platform_Sprites[key].empty()
        self.Player_Sprites.empty()
        for group in self.JustThere_Sprites:
            group.empty()
        for key in self.Collectable_Sprites:
            self.Collectable_Sprites[key].empty()

    def LoadMap(self):
        with open(f'data/Levels/level{self.Level}.txt') as f:
            self.LEVEL = f.read().split('\n')

        level = []
        for line in self.LEVEL:
            pos, line2 = 0, []
            while pos<len(line):
                if line[pos] == '[':
                    char = ''
                    while line[pos+1]!=']':
                        pos+=1
                        char = char + (line[pos])
                    line2.append(char)
                pos+=1
            level.append(line2)
        self.LEVEL = level.copy()
        
        self.MAP_SIZE = (len(self.LEVEL[0])*self.TILE_SIZE[0], len(self.LEVEL)*self.TILE_SIZE[1])

        for i in range(len(self.LEVEL)):
            for j in range(len(self.LEVEL[i])): 
                if 'L' in self.LEVEL[i][j]:
                    self.Platform_Sprites['lava'].add(Objects(j*self.TILE_SIZE[0], i*self.TILE_SIZE[1], isAnim = True, key = 'Lava'))
                    
                elif 'Q' in self.LEVEL[i][j]:
                    self.PLAYER = Player(j*self.TILE_SIZE[0], i*self.TILE_SIZE[1])
                    self.Player_Sprites.add(self.PLAYER)

                elif 'F' in self.LEVEL[i][j]:
                    self.Platform_Sprites['goal'].add(Objects(j*self.TILE_SIZE[0], i*self.TILE_SIZE[1], self.TILE_SIZE[0], self.TILE_SIZE[1], image = self.Tilesets['F']))
                    
                elif 'B' in self.LEVEL[i][j]:
                    self.Platform_Sprites['platform'].add(Objects(j*self.TILE_SIZE[0], i*self.TILE_SIZE[1], self.TILE_SIZE[0], self.TILE_SIZE[1], image = self.Tilesets['B']))

                elif 'P' in self.LEVEL[i][j]:
                    self.Collectable_Sprites['present'].add(Objects(j*self.TILE_SIZE[0], i*self.TILE_SIZE[1], self.TILE_SIZE[0], self.TILE_SIZE[1], isAnim = True, key = 'Present'))

                for var in ('Z','X','C'):
                    colorKey = {'Z':None, 'X':None, 'C':None}
                    if var in self.LEVEL[i][j]:
                        self.Platform_Sprites['platform'].add(Objects(j*self.TILE_SIZE[0], i*self.TILE_SIZE[1], self.TILE_SIZE[0], self.TILE_SIZE[1], image = self.Tilesets[var], colorkey = colorKey[var]))
                    
                for var in ('U','Y','T'):
                    if var in self.LEVEL[i][j]:
                        self.JustThere_Sprites[0].add(Objects(j*self.TILE_SIZE[0], i*self.TILE_SIZE[1], self.TILE_SIZE[0], self.TILE_SIZE[1], image = self.Tilesets[var]))

                for var in ('a','b','c','d','e','f','g','h','i','j','k'):
                    if var in self.LEVEL[i][j]:
                        width = self.DecoratorSize[var][0]
                        height = self.DecoratorSize[var][1]
                        self.JustThere_Sprites[1].add(Objects(j*self.TILE_SIZE[0] - width//2 + self.TILE_SIZE[0], i*self.TILE_SIZE[1] - height + self.TILE_SIZE[1], width, height, image = self.Decorators[var], colorkey = self.Decorators[var].get_at((0,0))))  


##        with open(f'data/Levels/Decorators/1/level{self.Level}.txt') as f:
##            self.LEVEL = f.read().split('\n')
##
##        for i in range(len(self.LEVEL)):
##            for j in range(len(self.LEVEL[i])):
##                if self.LEVEL[i][j]=='P':
##                    self.Collectable_Sprites['present'].add(Objects(j*self.TILE_SIZE[0], i*self.TILE_SIZE[1], self.TILE_SIZE[0], self.TILE_SIZE[1], isAnim = True, key = 'Present'))
##    
##        with open(f'data/Levels/Decorators/2/level{self.Level}.txt') as f:
##            self.LEVEL = f.read().split('\n')
##
##        for i in range(len(self.LEVEL)):
##            for j in range(len(self.LEVEL[i])):
                var = self.LEVEL[i][j]
                if var in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k'):
                    width = self.DecoratorSize[var][0]
                    height = self.DecoratorSize[var][1]
                    self.JustThere_Sprites[1].add(Objects(j*self.TILE_SIZE[0] - width//2 + self.TILE_SIZE[0], i*self.TILE_SIZE[1] - height + self.TILE_SIZE[1], width, height, image = self.Decorators[var], colorkey = self.Decorators[var].get_at((0,0))))  
                    
                    
        self.PLAYER(ACC=1.2, FRICTION=-0.15, GRAVITY=2, JUMP_vel=-27)
        self.CAMERA = Camera(self.SIZE[0], self.SIZE[1])

    def UpdateCaption(self, text):
        pygame.display.set_caption(text)

    def Start(self):
        running = True
        DisplayScreen = 'menu'
        isdisplay = False
        #menu, level, game, pause, end
        clock = pygame.time.Clock()
        while running:
            clock.tick(self.FPS)
            if DisplayScreen == 'menu':
                if not isdisplay:
                    self.Screen = pygame.display.set_mode(self.miniSIZE, flags = pygame.RESIZABLE)
                    Tab = -1
                    Buttons = [RectButtons(self.ButtonColor, 200, 200, 110, 50, 3, 'S T A R T', 210, 205, self.ButtonText, pygame.font.SysFont('AGENCY FB', 30, 1))
                               , RectButtons(self.ButtonColor, 200, 300, 110, 50, 3, 'L E V E L', 210, 305, self.ButtonText, pygame.font.SysFont('AGENCY FB', 30, 1))
                               , RectButtons(self.ButtonColor, 200, 400, 110, 50, 3, '  E X I T', 208, 405, self.ButtonText, pygame.font.SysFont('AGENCY FB', 30, 1))    ]
                    ButtonNames  = ['start', 'level', 'exit']
                    isdisplay = True
                self.Screen.blit(self.BG_IMG2, (0,-220))
                self.UpdateCaption(f'Status : Menu  |  ')
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                        Tab = Tab+1 if Tab < len(Buttons)-1 else 0        
                for button in Buttons:
                    if button.hit() or (Buttons[Tab] == button and Tab>-1) :button.change(bg_color = self.ButtonChange, border = 4)
                    else:button.restore()
                    button.create(self.Screen) 
                    if (button.hit() and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or (button == Buttons[Tab] and Tab>-1 and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                        if ButtonNames[Buttons.index(button)] in ['start', 'level']:isdisplay = False
                        if ButtonNames[Buttons.index(button)] == 'start':
                            DisplayScreen = 'game'
                            self.onLevelMode = False
                        elif ButtonNames[Buttons.index(button)] == 'level':DisplayScreen = 'level'
                        elif ButtonNames[Buttons.index(button)] == 'exit':
                            running = False

            elif DisplayScreen == 'level':
                if not isdisplay:
                    Tab = -1
                    level_Buttons = []
                    x, y = 50, 50
                    for level in range(1,self.LEVELS+1):
                        level_Buttons.append(SqButtons(self.ButtonColor if level<=self.CompletedLevels else Grey, x, y, 50, 2, f'{level}', x+15, y+10, self.ButtonText, pygame.font.SysFont('AGENCY FB', 30, 1)))
                        x += 60
                        if x+100 >500:
                            x = 50
                            y += 60
                    isdisplay = True          
                self.Screen.blit(self.BG_IMG2, (-500,-220))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        DisplayScreen = 'menu'
                        isdisplay = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                        Tab = Tab+1 if Tab < len(level_Buttons)-1 and Tab<self.CompletedLevels-1 else 0         
                for button in level_Buttons:
                    if (button.hit() and level_Buttons.index(button)<self.CompletedLevels) or (level_Buttons[Tab] == button and Tab>-1) :button.change(bg_color = self.ButtonChange)
                    else:button.restore()
                    button.create(self.Screen)
                for button in level_Buttons:
                    if (button.hit()and level_Buttons.index(button)<self.CompletedLevels and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or (button == level_Buttons[Tab] and Tab>-1 and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                        self.Level = int(button.text)
                        self.onLevelMode = True
                        DisplayScreen = 'game'
                        isdisplay = False

            elif DisplayScreen == 'game':
                if not isdisplay:
                    if not self.onLevelMode: self.Level = 1
                    self.isOver = False
                    self.ClearSprites()
                    self.Screen = pygame.display.set_mode(self.SIZE)
                    self.LoadMap()
                    isdisplay = True
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN and event.key in [pygame.K_w, pygame.K_SPACE] and not self.isPaused:
                        self.PLAYER.jump()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        shot  = pygame.Surface(self.miniSIZE)
                        shot.blit(self.Screen, (self.PLAYER.rect.x%(self.SIZE[0]//2) - self.SIZE[0]//2, self.PLAYER.rect.y%(self.SIZE[1]//2) - self.SIZE[1]//2))
                        DisplayScreen = 'pause'
                        isdisplay = False
                        
                if not self.isPaused:self.PLAYER.move()
                for sprite in self.Platform_Sprites['lava']:
                    sprite.animate()
                for sprite in self.Collectable_Sprites['present']:
                    sprite.animate()
                    
                self.Update()
                self.Display()
                self.UpdateCaption(f'Status : Playing  |  Level : {self.Level}  |  Gifts : {self.Gifts}')
                
                if self.PLAYER.isOn(self.Platform_Sprites['goal']) and not self.isOver:
                    self.ClearSprites()
                    self.Level += 1
                    if self.Level>self.CompletedLevels:self.CompletedLevels = self.Level
                    with open('data/Levels/level.txt','r') as f:
                        data = f.read().split(',')
                    with open('data/Levels/level.txt','w') as f:
                        f.write(data[0] + ',' + str(self.CompletedLevels))
                        
                    if self.Level == self.LEVELS:self.Level = 1 #just for fun
                    self.LoadMap()

                if self.isOver:
                    shot  = pygame.Surface(self.miniSIZE)
                    shot.blit(self.Screen, (self.PLAYER.rect.x%(self.SIZE[0]//2) - self.SIZE[0]//2, self.PLAYER.rect.y%(self.SIZE[1]//2) - self.SIZE[1]//2))
                    DisplayScreen = 'end'
                    isdisplay = False

            elif DisplayScreen == 'pause':
                if not isdisplay:
                    self.Screen = pygame.display.set_mode(self.miniSIZE)
                    Buttons = []
                    Buttons = [RectButtons(self.ButtonColor, 200, 100, 120, 50, 3, 'Resume', 208, 105, self.ButtonText, pygame.font.SysFont('AGENCY FB', 30, 1)),
                               RectButtons(self.ButtonColor, 200, 200, 110, 50, 3, 'Restart', 210, 205, self.ButtonText, pygame.font.SysFont('AGENCY FB', 30, 1)),
                               RectButtons(self.ButtonColor, 200, 300, 120, 50, 3, 'Main Menu', 208, 305, self.ButtonText, pygame.font.SysFont('AGENCY FB', 30, 1)) ]
                    ButtonNames = ['resume', 'restart','menu']
                    Tab = -1
                    isdisplay = True
                self.Screen.blit(shot ,(0,0))
                self.UpdateCaption(f'Status : Paused  |  Level : {self.Level}  |  ')
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        DisplayScreen = 'game'
                        self.Screen  = pygame.display.set_mode(self.SIZE)
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                        Tab = Tab+1 if Tab < len(Buttons)-1 else 0         
                for button in Buttons:
                    if button.hit() or (Buttons[Tab] == button and Tab>-1):button.change(bg_color = self.ButtonChange, border = 4)
                    else:button.restore()
                    button.create(self.Screen)
                    if (button.hit() and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or (button == Buttons[Tab] and Tab>-1 and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                        if ButtonNames[Buttons.index(button)] == 'restart':
                            DisplayScreen = 'game'
                            self.isOver = False
                            isdisplay = False
                        elif ButtonNames[Buttons.index(button)] == 'menu':
                            DisplayScreen = 'menu'
                            isdisplay = False
                        elif ButtonNames[Buttons.index(button)] == 'resume':
                            DisplayScreen = 'game'
                            self.Screen  = pygame.display.set_mode(self.SIZE)
                            
            elif  DisplayScreen == 'end':
                if not isdisplay:
                    self.Screen = pygame.display.set_mode(self.miniSIZE)
                    Buttons = []
                    Buttons = [RectButtons(self.ButtonColor, 200, 200, 110, 50, 3, 'Restart', 210, 205, self.ButtonText, pygame.font.SysFont('AGENCY FB', 30, 1)),
                               RectButtons(self.ButtonColor, 200, 300, 120, 50, 3, 'Main Menu', 208, 305, self.ButtonText, pygame.font.SysFont('AGENCY FB', 30, 1)) ]
                    ButtonNames = ['restart', 'menu']
                    Tab = -1
                    isdisplay = True
                self.Screen.blit(shot, (0,0))
                self.UpdateCaption('Status : GameOver  |  Restart Level :' + ('1' if not self.onLevelMode else f'{self.Level}') + '  |  ')
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                        Tab = Tab+1 if Tab < len(Buttons)-1 else 0         
                for button in Buttons:
                    if button.hit() or (Buttons[Tab] == button and Tab>-1):button.change(bg_color = self.ButtonChange, border = 4)
                    else:button.restore()
                    button.create(self.Screen)
                    if (button.hit() and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or (button == Buttons[Tab] and Tab>-1 and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                        if ButtonNames[Buttons.index(button)] == 'restart':
                            DisplayScreen = 'game'
                            self.isOver = False
                            isdisplay = False
                        elif ButtonNames[Buttons.index(button)] == 'menu':
                            DisplayScreen = 'menu'
                            isdisplay = False
            pygame.display.update()

    def SuddenExit(message = None):
        pygame.quit()
        if message:
            raise SystemExit(message)

##-------------------------------------------------------------------------------------------------------------------------------------------------------##
##Player Class-------------------------------------------------------------------------------------------------------------------------------------------##
##-------------------------------------------------------------------------------------------------------------------------------------------------------##

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.sheet = {'Walk':[Game.sheet['PlayerWalk'].copy()], 'Run':[Game.sheet['PlayerRun'].copy()], 'Idle':[Game.sheet['PlayerIdle'].copy()]}
        self.frames = {'Walk':Game.frames['PlayerWalk'], 'Run':Game.frames['PlayerRun'], 'Idle':Game.frames['PlayerIdle']}

        for key in ('Walk', 'Idle', 'Run'):
            images = []
            for image in self.sheet[key][0]:
                image.convert_alpha()
                images.append(pygame.transform.flip(image, True, False))
            self.sheet[key].append(images)
            
        self.speed = {'Walk':Game.speed['PlayerWalk'], 'Run':Game.speed['PlayerRun'], 'Idle':Game.speed['PlayerIdle']}
        
        self.index = 0
        self.dir = 0
        self.diff = 0
        self.image = self.sheet['Idle'][0][0] 
        self.image.set_colorkey(self.image.get_at((0,0)))    
        self.rect = self.image.get_rect()
        self.hitbox = pygame.Rect(x, y, 45, 58)
        self.UpdateRect()
        self.pos = pygame.math.Vector2(x+self.hitbox.width//2, y+self.hitbox.height//2)

        colorkey = Game.sheet['PlayerAnimRight'][0].get_at((0,0))
        self.AnimR = Objects(self.hitbox.left - self.hitbox.width, self.hitbox.top, colorkey = colorkey, isAnim = True, key = 'PlayerAnimRight')
        self.AnimI = Objects(self.hitbox.left - self.hitbox.width, self.hitbox.top, colorkey = colorkey, isAnim = True, key = 'PlayerAnimIdle')
        self.AnimL = Objects(self.hitbox.left - self.hitbox.width, self.hitbox.top, colorkey = colorkey, isAnim = True, key = 'PlayerAnimRight')
        self.AnimL.sheet = []
        for image in self.AnimR.sheet:
            self.AnimL.sheet.append(pygame.transform.flip(image, True, False))
        
        self.Anim = Objects(self.hitbox.left - self.hitbox.width, self.hitbox.top, isAnim = True, key = 'PlayerAnimIdle')
        
        Game.Player_Sprites.add(self.Anim)
        
    def updateAnim(self):
        if self.vel.x<0:
            self.Anim.rect.left = self.hitbox.right
        elif self.vel.x>0:
            self.Anim.rect.right = self.hitbox.left
        self.Anim.rect.y = self.hitbox.top
    def UpdateRect(self):
        self.rect.x = self.hitbox.x - self.hitbox.width//2 + self.diff
        self.rect.y = self.hitbox.y - self.hitbox.height//10
        
    def move(self):
        self.acc.y = self.GRAVITY
        self.acc.x = 0
        
        boost = self.ACC if pygame.key.get_mods() & pygame.KMOD_SHIFT else 0
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.acc.x = -self.ACC - boost
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.acc.x = self.ACC + boost
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.acc.y += self.ACC + boost
        if not(keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_d]):self.acc.x = 0
        
        self.acc.x += self.vel.x*self.FRICTION
        self.vel += self.acc
        self.pos += self.vel+self.acc/2
        
        if int(self.pos.x)>self.hitbox.centerx: value = 1
        elif int(self.pos.x)<self.hitbox.centerx: value = -1
        
        while self.hitbox.centerx!=int(self.pos.x):
            self.hitbox.centerx += value
            if self.check_collision(self.vel.x, 0):
                self.pos.x = self.hitbox.centerx
                break
        if int(self.pos.y)>self.hitbox.centery: value = 1
        elif int(self.pos.y)<self.hitbox.centery: value = -1

        while self.hitbox.centery!=int(self.pos.y):
            self.hitbox.centery += value
            if self.check_collision(0, self.vel.y):
                self.pos.y = self.hitbox.centery
                break
            
        self.animate(self.vel.x, self.vel.y)
        
    def check_collision(self, dx, dy):
        for key in ('platform', 'goal'):
            for platform in Game.Platform_Sprites[key]:
                if self.rect_collision(self, platform):
                    if dx>0:
                        self.hitbox.right = platform.rect.left
                        self.vel.x = 0
                    if dx<0:
                        self.hitbox.left = platform.rect.right
                        self.vel.x = 0
                    if dy>0:
                        self.hitbox.bottom = platform.rect.top
                        self.vel.y = 0
                    if dy<0:
                        self.hitbox.top = platform.rect.bottom
                        self.vel.y = 0
                    return True
        return False

    def isOn(self, sprites, dokill = False):
        hits = False
        self.hitbox.y += 1
        for platform in sprites:
            if self.rect_collision(self, platform):
                hits = True
                break
        self.hitbox.y -= 1
        if hits: return True

    def rect_collision(self, target1, target2, dokill = False):
        if target1.hitbox.right>target2.rect.left and target1.hitbox.bottom>target2.rect.top and target1.hitbox.top<target2.rect.bottom and target1.hitbox.left<target2.rect.right:
            if dokill:target2.kill()
            return True

    def jump(self):
        boost = 4*self.ACC if pygame.key.get_mods() & pygame.KMOD_SHIFT else 0
        if self.isOn(Game.Platform_Sprites['platform']): self.vel.y = self.JUMP_vel - boost

    def animate(self, dx, dy):
        high_speed = 15
        if high_speed>dx>1 or -high_speed<dx<-1:
            key = 'Walk'
        elif dx>=high_speed or dx<=-high_speed:
            key = 'Run'
        else:
            key = 'Idle'
        if self.index<(self.frames[key]-1)*self.speed[key]:self.index += 1
        else:self.index = 0
        if dx<-1:self.dir = 1
        elif dx>1:self.dir = 0
        self.image = self.sheet[key][self.dir][self.index//self.speed[key]]
        
        if self.dir==1:
            self.diff = -20
        if self.dir==0:
            self.diff = 0

        if self.vel.x>=15:
            self.Anim.copy(self.AnimR, index = self.Anim.index)
        elif self.vel.x<=-15:
            self.Anim.copy(self.AnimL, index = self.Anim.index)
        else:
            self.Anim.copy(self.AnimI, index = 0)
        self.updateAnim()
        self.Anim.animate()

    def __call__(self, ACC, FRICTION, GRAVITY, JUMP_vel):
        self.ACC = ACC
        self.GRAVITY = GRAVITY
        self.FRICTION = FRICTION
        self.JUMP_vel = JUMP_vel
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)

##-------------------------------------------------------------------------------------------------------------------------------------------------------##
##Other Classes-------------------------------------------------------------------------------------------------------------------------------------------##
##-------------------------------------------------------------------------------------------------------------------------------------------------------##

class Objects(pygame.sprite.Sprite):
    def __init__(self, x, y, width = None, height = None, color = None, image = None, colorkey = None, isAnim = False, key = None):
        pygame.sprite.Sprite.__init__(self)
        if color:
            self.image = pygame.Surface((width, height))
            self.image.fill(color)
        elif image:
            self.image = pygame.transform.scale(image, (width, height))
            self.image.convert_alpha()
        elif isAnim:
            self.frames = Game.frames[key]
            self.sheet = Game.sheet[key].copy()
            for image in self.sheet:
                image.convert_alpha()
            self.index = 0
            self.speed = Game.speed[key]
            self.image = self.sheet[self.index]

        if colorkey:self.image.set_colorkey(colorkey)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.isColor = True if color else False
        self.isAnim = isAnim
        self.isImg = True if image else False

    def animate(self):
        if self.isAnim:
            if self.index<(self.frames-1)*self.speed:self.index += 1
            else:self.index = 0
            self.image = self.sheet[self.index//self.speed]

    def copy(self, target, index = None, isAnim = None):
        if self.isAnim:
            self.frames = target.frames
            self.sheet = target.sheet.copy()
            for image in self.sheet:
                image.convert_alpha()
            if index!= None:self.index = index
            self.speed = target.speed
            self.image = self.sheet[self.index]
            
class Camera:
    def __init__(self, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.height = height
        self.width = width

    def apply(self, sprite):
        return sprite.rect.move(self.rect.topleft)

    def update(self, player):
        if player.hitbox.centerx>Game.SIZE[0]//2 and player.hitbox.centerx<Game.MAP_SIZE[0]-Game.SIZE[0]//2 and Game.HORIZONTAL_SCROLL:
            self.rect.x = - player.hitbox.centerx + Game.SIZE[0]//2

        if player.hitbox.centery>Game.SIZE[1]//2 and player.hitbox.centery<Game.MAP_SIZE[1]-Game.SIZE[1]//2 and Game.VERTICAL_SCROLL:
            self.rect.y = - player.hitbox.centery + Game.SIZE[1]//2

pygame.init()
os.environ["SDL_VIDEO_CENTERED"] = "1"
Game = NewGame()
Game()
pygame.quit()       
        
