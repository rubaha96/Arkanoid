import pygame
import math
from pygame.locals import *

class Circle(pygame.sprite.Sprite):

    def __init__(self, x = 200, y = 100, r = 10,vx = 0, vy = 170, colour = (255,255,255)):
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

        """Bouncing ball"""
        if pygame.sprite.collide_rect(self, game.platforms[0]):
            self.y -= 7
            self.vy = -self.vy
            self.vx += game.platforms[0].vx

        for z in game.platforms:
            if z != 0 and pygame.sprite.collide_rect(self, game.platforms[z]):
                self.y += 7
                self.vy = -self.vy
                game.to_remove.add(z)
        flag = 1

        """Losing condition"""
        if self.y > 389:
            game.error_message()
           
class Platform(pygame.sprite.Sprite):
    def __init__(self, x = 25, y = 10, a = 100, b = 10, colour = (255,0,255)):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y,a,b);
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
    def __init__(self, x = 270, y = 370, a = 100, b = 10, colour = (255,255,0), vx = 0):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y, self.a, self.b, self.colour, self.vx = \
            x, y, a, b, colour, vx
        self.rect = pygame.Rect(self.x, self.y, self.a, self.b)
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
        self.vx = 0
        if game.pressed[pygame.K_LEFT]:
            self.vx = -100
        if game.pressed[pygame.K_RIGHT]:
            self.vx = 100

        self.x += self.vx * 3 * game.delta
        
        """Do not let Player get out of the Game window"""
        if self.x < 0:
            self.x = 0
        if self.x > game.width - self.a:
            self.x = game.width - self.a
        
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
        self.platforms = {
            0: Platform_main(),
            1: Platform(),
            2: Platform(x = 145, y = 10),
            3: Platform(x = 265, y = 10),
            4: Platform(x = 385, y = 10),
            5: Platform(x = 505, y = 10)
        }
        self.to_remove = set()
        self.error = False
        
        """Losing window"""
    def error_message(self):
        cyan = (0, 255, 255)
        black = (0, 0, 0)
        pygame.font.init()
        self.screen.fill(cyan)
        flag = 0

        font = pygame.font.Font(None, 50)
        text = font.render('You lose!', True, black)
        self.screen.blit(text, (200, 200))
        pygame.display.flip()
        while(True):
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_SPACE:
                    pygame.quit()

        "Ending of the cycle" 
        self.player.y = 200
        
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

        self.player.update(self)
        for i in self.platforms:
            self.platforms[i].update(self)

        for i in self.to_remove:
            self.platforms.pop(i)
        self.to_remove.clear()

    def render(self):
        """Render the scene"""
        self.screen.fill((0, 0, 0))
        self.player.render(self)
        for i in self.platforms:
            self.platforms[i].render(self)
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
