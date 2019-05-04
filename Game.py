from Config import *
from Classes import Manager

clock = pygame.time.Clock()
manager = Manager()
running = True

while running:
    screen.fill(black)
    manager.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            manager.player_paddle.key_events(event)
        if event.type == pygame.KEYUP:
            manager.player_paddle.stop_moving()

    pygame.display.flip()
    clock.tick(100)
