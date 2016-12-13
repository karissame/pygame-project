import pygame

class Character(object):
    def __init__(self,x,y,path):
        self.x = x
        self.y = y
        self.path = path
        self.image = pygame.image.load(self.path).convert_alpha()
        print type(self.image)
        self.width = self.image.get_width()

    def render(self,screen):
        screen.blit(self.image, (x, y))


class Hero(Character):
    def __init__(self,x,y,path):
        Character.__init__(self,x,y,path)
        self.speed_x = 0
        self.speed_y = 0

    def update(self, width, height):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x + self.width>= width:
            self.x=0
        if self.y + self.width >= height:
            self.y=0
        if self.x - self.width < 0:
            self.speed_x=5
        if self.y - self.width < 0:
            self.speed_y=5

class Monster(Character):
    def __init__(self,x,y,path):
        Character.__init__(self,x,y,path)
        self.speed_x = -2
        self.speed_y = 0

    def update(self, width, height):
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


def main():
    # declare the size of the canvas
    width = 512
    height = 480
    # blue_color = (97, 159, 182)


    # initialize the pygame framework
    pygame.init()

    # create screen
    screen = pygame.display.set_mode((width, height))

    # set window caption
    pygame.display.set_caption('Catch the Monster')

    # create a clock
    clock = pygame.time.Clock()

    ################################
    # PUT INITIALIZATION CODE HERE #
    ################################
    background = pygame.image.load('images/background.png').convert_alpha()

    hero = Hero(255,255,'images/hero.png')
    monster = Monster(30,100,'images/monster.png')

    chars = [
    hero,
    monster
    ]

    # game loop
    stop_game = False
    while not stop_game:
        # look through user events fired
        for event in pygame.event.get():
            ################################
            # PUT EVENT HANDLING CODE HERE #
            ################################
            if event.type == pygame.QUIT:
                # if they closed the window, set stop_game to True
                # to exit the main loop
                stop_game = True

        #######################################
        # PUT LOGIC TO UPDATE GAME STATE HERE #
        #######################################
        screen.blit(hero.image, (hero.x, hero.y))
        screen.blit(monster.image, (monster.x, monster.y))


        ################################
        # PUT CUSTOM DISPLAY CODE HERE #
        ################################
        screen.blit(background, (0, 0))
        screen.blit(hero.image, (hero.x, hero.y))
        screen.blit(monster.image, (monster.x, monster.y))


        # update the canvas display with the currently drawn frame
        pygame.display.update()

        # tick the clock to enforce a max framerate
        clock.tick(60)

    # quit pygame properly to clean up resources
    pygame.quit()

if __name__ == '__main__':
    main()
