import pygame
import math

class Circle:

    def __init__(self, x = 100, y = 100, r = 10,vx = 0, vy = 13, colour = (255,255,255)):
        """Constructor of Player class"""
        """self.a - acceleration"""
        """self.r - radius"""
        self.x, self.y, self.r, self.vx, self.vy, self.colour = \
                x, y, r, vx, vy, colour
        square_1_color = (255,255,255)

    def render(self, game):
        """Draw Player on the Game window"""
        pygame.draw.circle(game.screen,
                self.colour,
                (int(self.x), int(self.y)), self.r)

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

class Platform_main:
    def __init__(self, x = 270, y = 370, a = 100, b = 10, colour = (255,255,0)):
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
        if game.pressed[pygame.K_LEFT]:
            self.x -= 7
        if game.pressed[pygame.K_RIGHT]:
            self.x += 7

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
        self.platform1 = Platform()
        self.platform2 = Platform(x = 145, y = 10)
        self.platform3 = Platform(x = 265, y = 10)
        self.platform4 = Platform(x = 385, y = 10)
        self.platform5 = Platform(x = 505, y = 10)
        self.platform_main = Platform_main()
        self.ar = pygame.PixelArray(self.screen)

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
