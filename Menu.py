import pygame
from pygame import*
import subprocess
import Arkanoid

class Menu:
    def tick(self):
        """Return time in seconds since previous call
        and limit speed of the game to 60 fps"""
        self.delta = self.clock.tick(60) / 1000.0

    def __init__(self):
        """Constructor of the Game"""
        self._running = True
        self.size = self.width, self.height = 640, 400
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        pygame.display.set_caption('Arkanoid')
        self.clock = pygame.time.Clock()
        self.tool = 'run'
        self.image = pygame.image.load("Menu.jpg").convert()
        
    def event_handler(self, event):
        """Handling one pygame event"""
        if event.type == pygame.QUIT:
            self.exit()

    def move(self):
        """Here game objects update their positions"""
        self.tick()
        self.pressed = pygame.key.get_pressed()
        x = mouse.get_pos()[0]
        y = mouse.get_pos()[1]
        
        if pygame.mouse.get_pressed() == (1, 0, 0):
            if x > 220 and x < 420 and \
               y > 80 and y < 130:
                game = Arkanoid.Game()
                game.execute()
           # if x > 220 and x < 420 and \
               #y > 150 and y < 210:
            if x > 220 and x < 420 and \
               y > 230 and y < 280:
                menu.exit()

    def render(self):
        """Render the scene"""
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.image, (1,1))
        pygame.display.flip()

    def exit(self):
        """Exit the game"""
        self._running = False        

    def execute(self):
        """Execution loop of the game"""
        while(self._running):
            for event in pygame.event.get():
                self.event_handler(event)
            self.move()
            self.render()
        pygame.quit()

if __name__ == "__main__":
    menu = Menu()
    menu.execute()
