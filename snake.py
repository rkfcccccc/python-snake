import pygame, random

snakes = []
control_keys = {}
remains = {}

remains_mode = True
remains_lifetime = 100

apples = []
apples_count = 5
score_per_apple = 15

opposite_directions = {
    'up': 'down', 
    'down': 'up',
    'left': 'right',
    'right': 'left'
}
###

pygame.init()

clock = pygame.time.Clock()
game_display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

display_info = pygame.display.Info()
screen_width = display_info.current_w
screen_height = display_info.current_h

screen_indent = screen_width - (screen_width / 1.1)

SIZE_W, SIZE_H = 8, 8
CELL_SIZE = (screen_height - screen_indent * 2) / SIZE_H

border_size = 10

pygame.display.set_caption('snake')
pygame.mouse.set_visible(False)


class Snake:
    score = 0

    def __init__(self, cell_x, cell_y, direction, length, speed, color):
        tail = []

        x, y = dir2xy(direction)

        for i in range(length):
            tail.append((cell_x + -x * i, cell_y + -y * i))

        self.direction = direction
        self.length = length
        self.color = color
        self.tail = tail
        self.speed = speed

        self.alive = True

        self.last_move = 0

    def next_cell(self):
        return tuple(self.tail[0][i] + dir2xy(self.direction)[i] for i in range(2))

    def move(self):
        old_tail = self.tail[::]
        self.tail[0] = self.next_cell()

        for i in range(1, len(self.tail)):
            self.tail[i] = old_tail[i - 1]

        self.last_move = pygame.time.get_ticks()

    def set_direction(self, direction):
        self.direction = direction

    def die(self):
        self.alive = False

        if remains_mode:
            for i in range(len(self.tail) - 1, 0, -1):
                remains[self.tail[i]] = [100 + i * remains_lifetime, 100 + i * remains_lifetime]

    def set_speed(self, speed):
        self.speed = speed

    def set_length(self, length):
        if length == 0:
            self.alive = False
        elif length < self.length:
            for i in range(length, self.length):
                del self.tail[i]
        elif length > self.length:
            for i in range(length - self.length):
                self.tail.append(self.tail[-1])

        self.length = length


class Apple:
    def __init__(self):
        self.cell = (random.randint(0, SIZE_W), random.randint(0, SIZE_W))
        print(is_wall(self.cell))
        while is_wall(self.cell):
            self.cell = (random.randint(0, SIZE_W), random.randint(0, SIZE_W))

    def check(self):
        for s in snakes:
            if s.tail[0] == self.cell:
                s.set_length(s.length + 1)
                s.score += score_per_apple
                self.__init__()
                break

def dir2xy(direction):
    x, y = 0, 0
    if direction == 'left':
        x = -1
    elif direction == 'up':
        y = -1
    elif direction == 'right':
        x = 1
    else:
        y = 1

    return x, y


def cell2xy(cell):
    return min(screen_indent + cell[0] * CELL_SIZE, screen_indent + (SIZE_W - 1) * CELL_SIZE), min(screen_indent + cell[1] * CELL_SIZE, screen_indent + (SIZE_H - 1) * CELL_SIZE)


def is_wall(cell):
    next_pos = cell2xy(cell)

    if next_pos[0] < screen_indent or next_pos[0] > screen_indent + CELL_SIZE * (SIZE_W - 1):
        return True
    elif next_pos[1] < screen_indent or next_pos[1] > screen_indent + CELL_SIZE * (SIZE_H - 1):
        return True
    elif remains.get(cell) and remains[cell] is not None:
        return True

    for s in snakes:
        if not s.alive:
            continue

        for _cell in s.tail:
            if _cell == cell:
                return True

    return False


# directions: left, up, right, down
def create_snake(cell_x, cell_y, direction, length, speed, color, controls=None):
    s = Snake(cell_x, cell_y, direction, length, speed, color)

    snakes.append(s)

    if controls:
        for k, v in controls.items():
            control_keys[k] = [v, len(snakes) - 1]

    return s


create_snake(1, 1, 'down', 1, 30, (109, 127, 242), {
    273: 'up',
    274: 'down',
    276: 'left',
    275: 'right'
})
"""
create_snake(5, 5, 'down', 4, 30, (62, 242, 109), {
    119: 'up',
    97: 'left',
    115: 'down',
    100: 'right'
})

create_snake(21, 17, 'up', 4, 15, (242, 62, 109))

create_snake(23, 17, 'up', 4, 15, (242, 62, 109))

create_snake(25, 17, 'up', 4, 15, (242, 62, 109))

"""

for i in range(apples_count):
    apples.append(Apple())

###

running = True
try:
    while running:
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == 3 and event.key == 27:
                running = False
    
            if event.type == 3:
                if event.key == 13:
                    snakes[0].alive = False
    
                if control_keys.get(event.key):
                    control = control_keys[event.key]
                    
                    if opposite_directions[snakes[control[1]].direction] != control[0]:
                        snakes[control[1]].set_direction(control[0])
    
            print(event)
    
        game_display.fill((255, 255, 255))
    
        time = pygame.time.get_ticks()
    
        for a in apples:
            x, y = cell2xy(a.cell)
            color = (188, 88, 14)
    
            pygame.draw.rect(game_display, color, (x, y, CELL_SIZE, CELL_SIZE))
    
            a.check()
    
        for s in snakes:
            if not s.alive:
                continue
    
            if time - s.last_move > s.speed * 20:
                if not is_wall(s.next_cell()):
                    s.move()
                else:
                    s.die()
                    continue
    
            for i in range(len(s.tail)):
                part = s.tail[i]
                x, y = cell2xy((part[0], part[1]))
                color = (i == 0 and tuple(i * 0.5 for i in s.color) or s.color)
    
                pygame.draw.rect(game_display, color, (x, y, CELL_SIZE, CELL_SIZE))
    
        for k, v in remains.items():
            if v is None:
                continue
    
            percent = v[0] / (v[1] == -1 and v[0] or v[1])
            size = CELL_SIZE * percent
            x, y = tuple(i + (CELL_SIZE - size) / 2 for i in cell2xy(k))
            remains[k][0] -= 10
    
            if percent <= 0.5:
                remains[k] = None
    
            pygame.draw.rect(game_display, (150, 150, 150), (x, y, size, size))
    
        # Borders #
    
        pygame.draw.rect(game_display, (220, 220, 220),
                         (screen_indent, screen_indent - border_size, CELL_SIZE * SIZE_H, border_size))
        pygame.draw.rect(game_display, (220, 220, 220),
                         (screen_indent, screen_indent + CELL_SIZE * SIZE_H, CELL_SIZE * SIZE_H, border_size))
        pygame.draw.rect(game_display, (220, 220, 220),
                         (screen_indent - border_size, screen_indent - border_size, border_size, CELL_SIZE * SIZE_H + border_size * 2))
        pygame.draw.rect(game_display, (220, 220, 220),
                         (screen_indent + CELL_SIZE * SIZE_W, screen_indent - border_size, border_size, CELL_SIZE * SIZE_H + border_size * 2))
    
        for x in range(1, SIZE_W):
            pygame.draw.rect(game_display, (230, 230, 230), (screen_indent + CELL_SIZE * x, screen_indent, 1, CELL_SIZE * SIZE_H))
    
        for y in range(1, SIZE_H):
            pygame.draw.rect(game_display, (230, 230, 230), (screen_indent, screen_indent + CELL_SIZE * y, CELL_SIZE * SIZE_W, 1))
    
        w, h = screen_width - (screen_width / 1.25), screen_height - (screen_height / 1.1)
        for i in range(len(snakes)):
            x, y = screen_width - screen_indent - w, screen_indent - border_size + (h + 10) * i
            pygame.draw.rect(game_display, (i == 0 and tuple(i * 0.8 for i in snakes[i].color) or s.color), (x, y, w, h))
            pygame.draw.rect(game_display, snakes[i].color, (x + 2, y + 2, w - 4, h - 4))
    
            font = pygame.font.SysFont('bitstreamverasans', 32)
            text = font.render((not snakes[i].alive and 'Died - ' or '') + 'Length: ' + str(snakes[i].length), True, (255, 255, 255))
    
            game_display.blit(text, (x + (w - text.get_width()) / 2, y + (h - text.get_height()) / 2))
    
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
except SystemExit:
    pygame.quit()