import pygame
from random import randint
from pyhelp import colour
import pygame_window

class Score:
    def __init__(self, display, position, old_scores):
        self.score = 0
        self.incriment = 100
        self.font = pygame.font.SysFont("arial", 45)
        self.display = display 
        self.position = position

        self.highscores = [0,0,0,0,0]
        

    def draw(self):
        text = self.font.render(str(self.score), True, colour.white)
        self.display.blit(text, self.position)

    def update(self):
        self.score += self.incriment

    def restart(self):
        n = 0
        while n < len(self.highscores):
            if self.score > self.highscores[n]:
                self.highscores.insert(self.score, n)
                self.highscores.pop(-1)
                break
            n += 0
        self.score = 0

        
        

class Snake:
    def __init__(self, start, length):
        self.length = length
        self.head = start
        self.direction = 'w'

        self.body = [[x, self.head[1]] for x in range(self.head[0] + 1,
                                                      self.head[0] + self.length - 1)]
        self.tail = [self.head[0] + self.length - 1, self.head[1]]

    def get_grid(self):
        return self.body + [self.head, self.tail]

    def print(self):
        print([self.head]+self.body+[self.tail])


class Grid:
    def __init__(self, display, rows, columns, position):
        self.display = display
        self.rows = rows
        self.columns = columns
        self.position = position

        self.width = 20
        self.height = 20

        self.grid = [[None for _ in range(self.columns)] for _ in range(self.rows)]


    def set_point(self, x, y, thing):
        self.grid[y][x] = thing

    def remove(self, x, y):
        self.grid[y][x] = None

    def get_point(self, x, y):
        return self.grid[y][x]

    def draw_bd(self):
        pygame.draw.rect(self.display, colour.white,
                         [self.position[0], self.position[1],
                          self.columns * self.width, self.rows * self.height], 1)

    def draw(self):
        for y in range(self.rows):
            for x in range(self.columns):
                if self.get_point(x, y) is not None:
                    pygame.draw.rect(self.display,
                                     self.get_point(x, y),
                                     [self.position[0] + x * self.width,
                                      self.position[1] + y * self.height,
                                      self.width-1, self.height-1])
        self.draw_bd()


    def _print(self):
        for i in self.grid:
            print(i)

        

class Window(pygame_window.main):
    def __init__(self):
        pygame_window.main.__init__(self, 800, 600, 'RTS')
        self.background_colour = colour.black
        self.framerate = 60
        

        self.speed_up = 100
        self.timer = 200
        
        self.score = Score(self.display, (1, 1), "a_file.txt")
        self.grid = Grid(self.display, 20, 20, (50,50))

        self.ted = Snake([self.grid.columns//2, self.grid.rows//2], 3)

        self.food = [0,0]
        
        self.start()
        
    def rand_p(self, x,y):
        p = [randint(0, x), randint(0, y)]
        while p in self.ted.get_grid():
            p = [randint(0, x), randint(0, y)]

        return p

    def set_food(self):
        self.food = self.rand_p(self.grid.rows-1, self.grid.columns-1)
        self.grid.set_point(self.food[0], self.food[1], colour.red)

    def start(self):
        self.grid = Grid(self.display, 20, 20, (50,50))
        self.set_food()
        self.ted = Snake([self.grid.columns//2, self.grid.rows//2], 3)
        for i in self.ted.get_grid():
            self.grid.set_point(i[0],i[1], colour.white)

    def step(self):
        d = self.ted.direction
        hold = [self.ted.head[0], self.ted.head[1]]
        
        if d == 'n':
            hold[1] -= 1
        elif d == 'e':
            hold[0] += 1
        elif d == 's':
            hold[1] += 1
        elif d == 'w':
            hold[0] -= 1

        if self.will_die(hold[0], hold[1]):
            self.start()
            print('dead')
        elif hold == self.food:
            self.ted.body.insert(0, self.ted.head)
            self.ted.head = hold

            self.grid.set_point(self.ted.head[0], self.ted.head[1], colour.white)
            self.set_food()

            self.timer += self.speed_up
            self.score.update()
        else:
            self.grid.remove(self.ted.tail[0], self.ted.tail[1])
            
            self.ted.tail = self.ted.body.pop(-1)
            self.ted.body.insert(0, self.ted.head)
            self.ted.head = hold

            self.grid.set_point(self.ted.head[0], self.ted.head[1], colour.white)
            

    def will_die(self, x, y):
        if x < 0 or y < 0:
            dead = True
        elif x >= self.grid.columns or y >= self.grid.rows:
            dead = True
        elif [x, y] in self.ted.body + [self.ted.tail]:
            dead = True
            print([x, y], self.ted.body[1:] + [self.ted.tail])
        else:
            dead = False

        return dead

    def event_handle(self, event):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if self.ted.direction != 's':
                        self.ted.direction = 'n'

                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if self.ted.direction != 'n':
                        self.ted.direction = 's'

                if event.key == pygame.K_d  or event.key == pygame.K_RIGHT:
                    if self.ted.direction != 'w':
                        self.ted.direction = 'e'

                if event.key == pygame.K_a  or event.key == pygame.K_LEFT:
                    if self.ted.direction != 'e':
                        self.ted.direction = 'w'
        
        



    def update(self):
        self.grid.draw()
        self.score.draw()
        self.step()

if __name__ == '__main__':
    Window().run()
    
