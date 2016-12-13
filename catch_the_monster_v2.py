import pygame
from random import randint
import time

goblins = []
level_counter = 1


KEY_UP = 273
KEY_DOWN = 274
KEY_LEFT = 276
KEY_RIGHT = 275

class Character(object):
    def __init__(self,x,y,path):
        self.x = x
        self.y = y
        self.path = path
        self.image = pygame.image.load(self.path).convert_alpha()
        self.width = self.image.get_width()


class Hero(Character):
    def __init__(self,x,y,path):
        Character.__init__(self,x,y,path)
        self.speed_x = 0
        self.speed_y = 0

    def update(self, width, height):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x + self.width >= width-self.width:
            self.x = width - self.width*2
        if self.y + self.width >= height-self.width:
            self.y= height - self.width*2
        if self.x < self.width:
            self.x = self.width
        if self.y < self.width:
            self.y = self.width


class Monster(Character):
    def __init__(self,x,y,path,speedlimit):
        Character.__init__(self,x,y,path)
        self.speed_x = 2
        self.speed_y = 0
        self.speedlimit = speedlimit
        self.needMonsterUpdate = False
        self.timestamp = time.time()

    def update(self, width, height):

        if time.time() - self.timestamp >3:
            self.needMonsterUpdate = True
            self.timestamp = time.time()
        if self.needMonsterUpdate:
            self.speed_x = randint(-1 * self.speedlimit,self.speedlimit)
            self.speed_y = randint(-1 * self.speedlimit,self.speedlimit)
            self.needMonsterUpdate = False
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x + self.width >= width:
            self.x=0
        if self.y + self.width >= height:
            self.y=0
        if self.x < 0:
            self.x = width - self.width
        if self.y < 0:
            self.y = height - self.width

class Goblin(Monster):
    def __init__(self,x,y,path,speedlimit):
        Monster.__init__(self,x,y,path,speedlimit)
        Character.__init__(self,x,y,path)
        self.speed_x = 1
        self.speed_y = 0

def main():
    global level_counter
    global goblins
    # declare the size of the canvas
    width = 512
    height = 480
    # blue_color = (97, 159, 182)


    # initialize the pygame framework
    pygame.init()

    # create screen
    screen = pygame.display.set_mode((width, height))



    # create a clock
    clock = pygame.time.Clock()

    caughtMonster = False
    heroDied = False
    death_sound = False
    win_sound = False

    ################################
    # PUT INITIALIZATION CODE HERE #
    ################################

    background = pygame.image.load('images/background.png').convert_alpha()

    hero = Hero(255,255,'images/hero.png')
    monster = Monster(30,100,'images/monster.png',3)
    goblins.append(Goblin(0,0,'images/goblin.png',level_counter))


    named_chars = [
    hero,
    monster
    ]

    chars = goblins + named_chars

    level_up = False

    # game loop
    stop_game = False
    while not stop_game:
        # look through user events fired
        for event in pygame.event.get():
            ################################
            # PUT EVENT HANDLING CODE HERE #
            ################################
            if event.type == pygame.KEYDOWN:
                # activate the cooresponding speeds
                # when an arrow key is pressed down
                if event.key == KEY_DOWN:
                    hero.speed_y = 2
                elif event.key == KEY_UP:
                    hero.speed_y = -2
                elif event.key == KEY_LEFT:
                    hero.speed_x = -2
                elif event.key == KEY_RIGHT:
                    hero.speed_x = 2
            if event.type == pygame.KEYUP:
                # deactivate the cooresponding speeds
                # when an arrow key is released
                if event.key == KEY_DOWN:
                    hero.speed_y = 0
                elif event.key == KEY_UP:
                    hero.speed_y = 0
                elif event.key == KEY_LEFT:
                    hero.speed_x = 0
                elif event.key == KEY_RIGHT:
                    hero.speed_x = 0

            if hero.x + 32 < monster.x or monster.x + 30 < hero.x or hero.y + 32 < monster.y or monster.y + 32 < hero.y:
                pass
            else:
                caughtMonster = True
                if level_up == False:
                    level_counter += 1
                pygame.display.set_caption('Catch the Monster: Level %r' % (level_counter))
                level_up = True
                sound = pygame.mixer.Sound('sounds/win.wav')
                if win_sound == False:
                    sound.play(loops = 0)
                    win_sound = True

            for goblin in goblins:
                if hero.x + 32 < goblin.x or goblin.x + 30 < hero.x or hero.y + 32 < goblin.y or goblin.y + 32 < hero.y:
                    pass
                else:
                    heroDied = True
                    level_counter = 1
                    pygame.display.set_caption('Catch the Monster: Level %r' % (level_counter))
                    goblins = []
                    sound = pygame.mixer.Sound('sounds/lose.wav')
                    if death_sound == False:
                        sound.play(loops = 0)
                        death_sound = True

            if event.type == pygame.KEYDOWN:
                # activate the cooresponding speeds
                # when an arrow key is pressed down
                if event.key == pygame.K_RETURN:
                    main()

            if event.type == pygame.QUIT:
                # if they closed the window, set stop_game to True
                # to exit the main loop
                stop_game = True

        #######################################
        # PUT LOGIC TO UPDATE GAME STATE HERE #
        #######################################
        for char in chars:
            if caughtMonster == False and heroDied == False:
                char.update(width, height)
            else:
                break



        ################################
        # PUT CUSTOM DISPLAY CODE HERE #
        ################################
        if caughtMonster:
            font = pygame.font.Font(None, 25)
            text = font.render('You Win!  Press Enter to play again', True, (0, 0, 0))
            screen.blit(text, (100, height/2))

        elif heroDied:
            font = pygame.font.Font(None, 25)
            text = font.render('You Lose!  Press Enter to play again', True, (0, 0, 0))
            screen.blit(text, (100, height/2))

        else:
            screen.blit(background, (0, 0))
            for char in chars:
                screen.blit(char.image, (char.x, char.y))


        # update the canvas display with the currently drawn frame
        pygame.display.update()

        # tick the clock to enforce a max framerate
        clock.tick(60)

    # quit pygame properly to clean up resources
    pygame.quit()

if __name__ == '__main__':
    main()
