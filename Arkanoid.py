import pygame
import math
from pygame.locals import *

class Circle(pygame.sprite.Sprite):

    def __init__(self, x = 200, y = 100, r = 10,vx = 0, vy = 170, colour = (255,255,255)):
        """Constructor of ball class"""
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y, self.r, self.vx, self.vy, self.colour = \
                x, y, r, vx, vy, colour
        square_1_color = (255,255,255)

    def render(self, game):
        """Draw ball on the Game window"""
        pygame.draw.circle(game.screen,
                self.colour,
                (int(self.x), int(self.y)), self.r)

    def update(self, game):
        """Moving of ball"""
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

        """Bouncing conditions for ball"""
        if pygame.sprite.collide_rect(self, game.main_platform):
            self.y -= 7
            self.vy = -self.vy
            self.vx += game.main_platform.vx

        """Displacement of ball from striking with platform"""
        for z in game.platforms:
            if pygame.sprite.collide_rect(self, game.platforms[z]):
                self.y += 7
                self.vy = -self.vy
                game.to_remove.add(z)
           
class Platform(pygame.sprite.Sprite):

    def __init__(self, x = 25, y = 10, a = 50, b = 10, vx = 150, colour = (255,0,255)):
        """Constructor of striking objects class"""
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y, self.a, self.b, self.vx, self.colour = \
            x, y, a, b, vx, colour
        self.rect = pygame.Rect(self.x, self.y, self.a, self.b)
        
    def update(self, game):
        """Moving of platform"""
        self.rect = pygame.Rect(self.x, self.y, self.a, self.b)
        self.x += self.vx * game.delta

        """Bouncing from other platforms"""
        if self.x < 0:
            if self.vx < 0:
                self.vx = -self.vx
        if self.x > game.width - self.a:
            if self.vx > 0:
                self.vx = - self.vx
                
        """Displacement of platform from striking"""
        for z in game.platforms:
            if self != game.platforms[z] and pygame.sprite.collide_rect(self, game.platforms[z]):
                self.x -= self.vx / 10
                self.vx = -self.vx

    def render(self, game):
        """Draw platforms on the Game window"""
        pygame.draw.rect(game.screen,
                self.colour,
                (int(self.x), int(self.y), self.a, self.b))         

        """Do not let platforms get out of the Game window"""
        if self.x < 0:
            self.x = 0
        if self.x > game.width - self.a:
            self.x = game.width - self.a

class Platform_main(pygame.sprite.Sprite):

    def __init__(self, x = 270, y = 370, a = 100, b = 10, colour = (255,255,0), vx = 0):
        """Constructor of player class"""
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y, self.a, self.b, self.colour, self.vx = \
            x, y, a, b, colour, vx
        self.rect = pygame.Rect(self.x, self.y, self.a, self.b)

    def render(self, game):
        """Draw Player platform on the Game window"""
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
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        pygame.display.set_caption('Arkanoid')
        self.clock = pygame.time.Clock()
        self.tool = 'run'
        self.player = Circle()

        """Finite-state maschine"""
        self.states = {'Game' : 0, 'Win' : 1, 'Lose' : 2}
        self.state = self.states['Game']

        """Dictionary"""
        self.main_platform = Platform_main()
        self.platforms = {
            0: Platform(),
            2: Platform(x = 145, y = 10),
            3: Platform(x = 285, y = 10),
            4: Platform(x = 410, y = 10),
            5: Platform(x = 520, y = 10),
            6: Platform(x = 100, y = 100),
            7: Platform(x = 230, y = 100),
            8: Platform(x = 350, y = 100),
            9: Platform(x = 490, y = 100),
        }
        self.to_remove = set()
        
        """Losing window"""
    def draw_lose_screen(self):
        red = (255, 0, 0)
        black = (0, 0, 0)
        pygame.font.init()
        self.screen.fill(red)

        font = pygame.font.Font(None, 70)
        text = font.render('You lose!', True, black)
        self.screen.blit(text, (200, 200))

        """Winning window"""
    def draw_win_screen(self):
        blue = (0, 255, 255)
        black = (0, 0, 0)
        pygame.font.init()
        self.screen.fill(blue)

        font = pygame.font.Font(None, 70)
        text = font.render('You win!', True, black)
        self.screen.blit(text, (200, 200))

        """Conditions of game ending"""
    def update_state(self):
        if not self.platforms:
            self.state = self.states['Win']
        elif self.player.y > 389:
            self.state = self.states['Lose']
        else:
            self.state = self.states['Game']
        
    def event_handler(self, event):
        """Handling one pygame event"""
        if event.type == pygame.QUIT:
            self.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.exit()

    def move(self):
        """Here game objects update their positions"""
        self.tick()
        self.pressed = pygame.key.get_pressed()

        """Do deleting platforms"""
        self.player.update(self)
        self.main_platform.update(self)
        for i in self.platforms:
            self.platforms[i].update(self)

        for i in self.to_remove:
            self.platforms.pop(i)
        self.to_remove.clear()

    def render(self):
        """Render the scene"""
        if self.state == self.states['Game']:            
            self.screen.fill((0, 0, 0))
            self.player.render(self)
            self.main_platform.render(self)
            for i in self.platforms:
                self.platforms[i].render(self)
        elif self.state == self.states['Win']:
            self.draw_win_screen()
        elif self.state == self.states['Lose']:
            self.draw_lose_screen()
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
            for event in pygame.event.get():
                self.event_handler(event)

            self.update_state()
            
            if self.state == self.states['Game']:
                self.move()

            self.render()
        self.cleanup()

if __name__ == "__main__":
    game = Game()
    game.execute()
