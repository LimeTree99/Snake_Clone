import pygame
import os




class main:
    def __init__(self,
                 width,
                 height,
                 window_name,
                 corner_image = os.path.split(__file__)[0] + '/images/flower_corner_image.png',
                 framerate = 60):
        
        self.width = width
        self.height = height
        self.framerate = framerate
        self.end = False
        self.background_on = True
        self.background_colour = (255,255,255)
        self.events = 0
        self.timer = 100
        
        pygame.init()
        self.display = pygame.display.set_mode((self.width,self.height),
                                               pygame.RESIZABLE)
        
        pygame.display.set_caption(window_name)
        icon = pygame.image.load(corner_image)
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()

    def update(self):
        pass
    
    def event_handle(self, event):
        pass

    def resize(self):
        pass
        
    def run(self):
        on_timer = pygame.USEREVENT+1
        pygame.time.set_timer(on_timer, self.timer)
        while not self.end:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    
                    
                if event.type == pygame.VIDEORESIZE:
                    self.width, self.height = event.w, event.h
                    self.display = pygame.display.set_mode((self.width, self.height),
                                                           pygame.RESIZABLE)
                    self.resize()
                    
                self.event_handle(event)

                if event.type == on_timer:
                    if self.background_on:
                        self.display.fill(self.background_colour)

                    self.update()
                    
            
            
            pygame.display.update()
            
            self.clock.tick(self.framerate)




if __name__ == '__main__':
    
    game = main(800, 500, 'Working Title')
    game.run()
