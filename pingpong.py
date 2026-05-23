import pygame
import random
import sys


pygame.init()
info = pygame.display.Info()
screenWidth, screenHeight = info.current_w, info.current_h
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("PING PONG GAME")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Ball:
    def __init__(self):
        self.reset()

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y

        if self.y <= 0 or self.y >= screenHeight:
            self.vel_y *= -1

    def reset(self):
        self.x = screenWidth // 2
        self.y = screenHeight // 2
        self.radius = 10
        self.vel_x = random.choice([-5, 5])
        self.vel_y = random.choice([-5, 5])


class Paddles:
    def __init__(self, x):
        self.x = x
        self.y = screenHeight // 2 - 50
        self.width = 10
        self.height = 100
        self.speed = 7

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))

    def update(self, up_key, down_key):
        keys = pygame.key.get_pressed()
        if keys[up_key] and self.y > 0:
            self.y -= self.speed
        if keys[down_key] and self.y < screenHeight - self.height:
            self.y += self.speed


class Game:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 50)
        self.big_font = pygame.font.SysFont("Arial", 80)
        self.state = "menu"
        self.red_score = 0
        self.blue_score = 0
        self.winner = ""

    def menu_screen(self, screen):
        screen.fill("black")
        text = self.font.render("Press SPACE to Start", True, WHITE)
        rect = text.get_rect(center=(screenWidth // 2, screenHeight // 2))
        screen.blit(text, rect)

    def draw_scores(self, screen):
        red_text = self.font.render(str(self.red_score), True, RED)
        blue_text = self.font.render(str(self.blue_score), True, BLUE)

        screen.blit(red_text, (screenWidth // 4, 20))
        screen.blit(blue_text, (3 * screenWidth // 4, 20))

    def game_screen(self, screen):
        screen.fill("black")
        ball.draw(screen)
        left_paddle.draw(screen, RED)
        right_paddle.draw(screen, BLUE)

        self.draw_scores(screen)

        if (ball.x - ball.radius <= left_paddle.x + left_paddle.width and
            left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height):
            ball.vel_x *= -1

        if (ball.x + ball.radius >= right_paddle.x and
            right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height):
            ball.vel_x *= -1

        if ball.x < 0:
            self.blue_score += 1
            ball.reset()

        if ball.x > screenWidth:
            self.red_score += 1
            ball.reset()

        if self.red_score == 10:
            self.winner = "RED WINS!"
            self.state = "game_over"

        if self.blue_score == 10:
            self.winner = "BLUE WINS!"
            self.state = "game_over"

    def game_over_screen(self, screen):
        screen.fill("black")

        text = self.big_font.render(self.winner, True, WHITE)
        rect = text.get_rect(center=(screenWidth // 2, screenHeight // 2 - 50))
        screen.blit(text, rect)

        restart_text = self.font.render("Press R to Restart", True, WHITE)
        rect2 = restart_text.get_rect(center=(screenWidth // 2, screenHeight // 2 + 50))
        screen.blit(restart_text, rect2)

    def reset_game(self):
        self.red_score = 0
        self.blue_score = 0
        self.state = "menu"
        ball.reset()



ball = Ball()
left_paddle = Paddles(50)
right_paddle = Paddles(screenWidth - 60)
game = Game()


if __name__ == "__main__":
    running = True
    while running:
        screen.fill("black")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.state = "game"
                if event.key == pygame.K_r and game.state == "game_over":
                    game.reset_game()

        if game.state == "menu":
            game.menu_screen(screen)

        elif game.state == "game":
            ball.update()
            left_paddle.update(pygame.K_w, pygame.K_s)
            right_paddle.update(pygame.K_UP, pygame.K_DOWN)
            game.game_screen(screen)

        elif game.state == "game_over":
            game.game_over_screen(screen)

        pygame.display.update()
        clock.tick(60)