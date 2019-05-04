from Config import *
import eztext


class Manager:
    def __init__(self):
        self.surface = screen
        self.ball = Ball(self, ball_speed)
        self.player_paddle = Paddle(self)
        self.enemy_paddle = ComputerPaddle(self)
        self.player_score = 0
        self.computer_score = 0
        self.player_scoreboard = eztext.Input(maxlength=3, color=(255, 255, 255), prompt=str(self.player_score))
        self.computer_scoreboard = eztext.Input(maxlength=3, color=(255, 255, 255), prompt=str(self.computer_score))
        self.player_scoreboard.x = screen_width/2 - 100
        self.computer_scoreboard.x = screen_width/2 + 100

    def score(self):
        if self.ball.x < 0:
            self.computer_score += 1
            self.computer_scoreboard.prompt = str(self.computer_score)
            self.start_ball("Enemy")

        if self.ball.x > screen_width:
            self.player_score += 1
            self.player_scoreboard.prompt = str(self.player_score)
            self.start_ball("Player")

    def start_ball(self, who_scored):
        self.ball.x = screen_width / 2 - 5
        self.ball.y = screen_height / 2 - 5
        self.ball.speed_y = 0
        self.ball.speed_x = 0
        time.sleep(1)
        if who_scored == "Enemy":
            self.ball.speed_x = ball_speed
        if who_scored == "Player":
            self.ball.speed_x = -ball_speed

    def update(self):
        self.ball.update()
        self.player_paddle.update()
        self.enemy_paddle.update()
        self.ball.check_hit(self.player_paddle)
        self.ball.check_hit(self.enemy_paddle)
        self.score()
        self.player_scoreboard.draw(self.surface)
        self.computer_scoreboard.draw(self.surface)


class Ball:
    def __init__(self, manager, speed_x):
        self.manager = manager
        self.x = screen_width/2 - 5
        self.y = screen_height/2 - 5
        self.speed_x = speed_x
        self.speed_y = 0
        self.middle = self.y-5

    def move(self):
        if self.speed_y > ball_max_speed or self.speed_y * -1 > ball_max_speed:
            self.speed_y = ball_max_speed
        self.x += self.speed_x
        self.y += self.speed_y
        if self.y <= 0 or self.y >= screen_height-10:
            self.speed_y *= -1
        self.middle = self.y-5

    def draw(self):
        pygame.draw.rect(self.manager.surface, white, (self.x, self.y, 10, 10), 0)

    def check_hit(self, paddle):
        if paddle.y < self.y+10 < paddle.y + paddle_height:
            if paddle.x < self.x + 10 < paddle.x + paddle_width:
                self.speed_x *= -1
                self.check_distance_from_middle(paddle)
            if paddle.x < self.x < paddle.x + paddle_width:
                self.speed_x *= -1
                self.check_distance_from_middle(paddle)

    def check_distance_from_middle(self, paddle):
        # finding where the middle of the paddle is
        middle_y = paddle.middle
        if self.middle < middle_y:
            # if it's above the middle of the paddle
            self.speed_y -= ball_speed_y_change
        if self.middle > middle_y:
            self.speed_y += ball_speed_y_change

    def update(self):
        self.draw()
        self.move()


class Paddle:
    def __init__(self, manager):
        self.manager = manager
        self.x = 0
        self.y = screen_height/2 - paddle_height/2
        self.middle = self.y + paddle_height / 2
        self.velocity = 0

    def draw(self):
        pygame.draw.rect(self.manager.surface, white, (self.x, self.y, paddle_width, paddle_height), 0)

    def key_events(self, event):
        if event.key == pygame.K_UP:
            self.velocity = -2
        if event.key == pygame.K_DOWN:
            self.velocity = 2

    def stop_moving(self):
        self.velocity = 0

    def move(self):
        self.y += self.velocity
        if self.y <= 0:
            self.y = 0
        if self.y >= screen_height-paddle_height:
            self.y = screen_height-paddle_height
        self.middle = self.y + paddle_height / 2

    def update(self):
        self.draw()
        self.move()


class ComputerPaddle(Paddle):

    def __init__(self, manager):
        Paddle.__init__(self, manager)
        self.manager = manager
        self.x = screen_width - paddle_width
        self.y = screen_height/2 - paddle_height/2
        self.middle = self.y + paddle_height/2

    def check_position(self):
        if self.middle < self.manager.ball.middle:
            self.velocity = 2
        elif self.middle > self.manager.ball.middle:
            self.velocity = -2
        elif self.middle == self.manager.ball.middle:
            self.velocity = 0

    def move(self):
        if self.y <= 0:
            self.y = 0
        if self.y >= screen_height-paddle_height:
            self.y = screen_height-paddle_height
        self.y += self.velocity
        self.middle = self.y + paddle_height / 2

    def update(self):
        self.draw()
        self.check_position()
        self.move()
