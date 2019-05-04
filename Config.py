import pygame
import time
pygame.init()
screen_height = 400
screen_width = 600
screen = pygame.display.set_mode((screen_width, screen_height))
black = (0, 0, 0)
white = (255, 255, 255)
ball_speed = -3
ball_max_speed = 4
ball_speed_y_change = 1
paddle_height = 100
paddle_width = 10

