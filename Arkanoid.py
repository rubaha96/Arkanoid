import pygame
import math
#from tkinter import

##class Menu_options:
##    def __init__(self):
##        menu_ini = Menu(root)
##        root.config(menu=menu_ini)
##        start_menu = Menu(menu_ini)
##        menu_ini.add_cascade(label="Start", menu = start_menu)
##        menu_ini.add_cascade(label="Help", menu = start_menu)
##        menu_ini.add_cascade(label="Exit", menu = start_menu)

        #younglinux.info/tkinter/menu.php
        #Статья с Хабра habrahabr.ru/post/133337/
        #russianlutheran.org/python/life/life
        
class Circle(pygame.sprite.Sprite):

    def __init__(self, x = 100, y = 100, r = 10,vx = 0, vy = 170, colour = (255,255,255)):
        """Constructor of Player class"""
        """self.a - acceleration"""
        """self.r - radius"""
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y, self.r, self.vx, self.vy, self.colour = \
                x, y, r, vx, vy, colour
        square_1_color = (255,255,255)

    def render(self, game):
        """Draw Player on the Game window"""
        pygame.draw.circle(game.screen,
                self.colour,
                (int(self.x), int(self.y)), self.r)

    def update(self, game):
        """Constant speed of the ball"""
        self.rect = pygame.Rect(self.x - self.r, self.y - self.r, 2 * self.r, 2 * self.r)
        self.x += self.vx * game.delta
        self.y += self.vy * game.delta

        """Do not let Player get out of the Game window"""
        if self.x < self.r:
            if self.vx < 0:
                self.vx = -self.vx
            self.x = self.r
        if self.y < self.r:
            if self.vy < 0:
                self.vy = -self.vy
            self.y = self.r
        if self.x > game.width - self.r:
            if self.vx > 0:
                self.vx = -self.vx
            self.x = game.width - self.r
        if self.y > game.height - self.r:
            if self.vy > 0:
                self.vy = -self.vy
            self.y = game.height - self.r

        if pygame.sprite.collide_rect(self, game.platform_main):
            self.y -= 7
            self.vy = -self.vy
class Platform:
    
    def __init__(self, x = 25, y = 10, a = 100, b = 10, colour = (255,0,255)):
        self.x, self.y, self.a, self.b, self.colour = \
            x, y, a, b, colour
        rect_1_color = (255,0,255)
        rect_1_width = 0

    def render(self, game):
        """Draw Player on the Game window"""
        pygame.draw.rect(game.screen,
                self.colour,
                (int(self.x), int(self.y), self.a, self.b))

class Platform_main(pygame.sprite.Sprite):
    def __init__(self, x = 270, y = 370, a = 100, b = 10, colour = (255,255,0)):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y, self.a, self.b, self.colour = \
            x, y, a, b, colour
        rect_1_color = (255,255,0)
        rect_1_width = 0


    def render(self, game):
        """Draw Player on the Game window"""
        pygame.draw.rect(game.screen,
                self.colour,
                (int(self.x), int(self.y), self.a, self.b))

    def update(self, game):
        """Update Player state"""
        self.rect = pygame.Rect(self.x, self.y, self.a, self.b)
        if game.pressed[pygame.K_LEFT]:
            self.x -= 7
        if game.pressed[pygame.K_RIGHT]:
            self.x += 7

        """Do not let Player get out of the Game window"""
        if self.x < 0:
            self.x = 0
        if self.x > game.width - self.a:
            self.x = game.width - self.a
"""
class Sprite:
    def __init__(self,xpos,ypos,filename):
                self.x=xpos
                self.y=ypos
                self.bitmap=image.load(filename)
        def set_position(self,xpos,ypos):
                self.x=xpos
                self.y=ypos
        def render(self):
                screen.blit(self.bitmap,(self.x,self.y))

       def collSprite(s1_x,s1_y,s2_x,s2_y,size1,size2):
            if (s1_x<(s2_x+size1+size2)) and (s1_x > (s2_x-size1)) and (s1_y > (s2_y - size1)) and (s1_y < (s2_y+size1+size2)):
                return 1
            else:
                return 0
"""
        
        
class Game:
    def tick(self):
        """Return time in seconds since previous call
        and limit speed of the game to 50 fps"""
        self.delta = self.clock.tick(50) / 1000.0

    def __init__(self):
        """Constructor of the Game"""
        self._running = True
        self.size = self.width, self.height = 640, 400
        # create main display - 640x400 window
        # try to use hardware acceleration
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        # set window caption
        pygame.display.set_caption('Arkanoid')
        # get object to help track time
        self.clock = pygame.time.Clock()
        # set default tool
        self.tool = 'run'
        self.player = Circle()
        self.platform1 = Platform()
        self.platform2 = Platform(x = 145, y = 10)
        self.platform3 = Platform(x = 265, y = 10)
        self.platform4 = Platform(x = 385, y = 10)
        self.platform5 = Platform(x = 505, y = 10)
        self.platform_main = Platform_main()
        self.ar = pygame.PixelArray(self.screen)
        #глянуть pubnub (список объектов Units)

    def event_handler(self, event):
        """Handling one pygame event"""
        if event.type == pygame.QUIT:
            # close window event
            self.exit()
        elif event.type == pygame.KEYDOWN:
            # keyboard event on press ESC
            if event.key == pygame.K_ESCAPE:
                self.exit()

    def move(self):
        """Here game objects update their positions"""
        self.tick()
        self.pressed = pygame.key.get_pressed()

        self.platform_main.update(self)
        self.player.update(self)

    def render(self):
        """Render the scene"""
        self.screen.fill((0, 0, 0))
        self.player.render(self)
        self.platform1.render(self)
        self.platform2.render(self)
        self.platform3.render(self)
        self.platform4.render(self)
        self.platform5.render(self)
        self.platform_main.render(self)
        self.ar[int(self.player.x/10.0),int(self.player.y/10.0)] = (200,200,200)
        pygame.display.flip()

    def exit(self):
        """Exit the game"""
        self._running = False

    def cleanup(self):
        """Cleanup the Game"""
        pygame.quit()

    def execute(self):
        """Execution loop of the game"""
        while(self._running):
            # get all pygame events from queue
            for event in pygame.event.get():
                self.event_handler(event)
            self.move()
            self.render()
        self.cleanup()

if __name__ == "__main__":
    game = Game()
    game.execute()
