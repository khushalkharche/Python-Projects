import pygame
import random
import os
import sys

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

info = pygame.display.Info()
screenWidth, screenHeight = info.current_w, info.current_h

SCREEN = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Dino Game")

clock = pygame.time.Clock()
FPS = 30

def load_image(path):
    return pygame.image.load(path).convert_alpha()

# Images
game_images = {
    "dino": {
        "start": load_image("PythonProjects/pygame/Assets/dino materials/images/Dino/DinoStart.png"),
        "running": [
            load_image("PythonProjects/pygame/Assets/dino materials/images/Dino/DinoRun1.png"),
            load_image("PythonProjects/pygame/Assets/dino materials/images/Dino/DinoRun2.png")
        ],
        "jumping": load_image("PythonProjects/pygame/Assets/dino materials/images/Dino/DinoJump.png"),
        "ducking": [
            load_image("PythonProjects/pygame/Assets/dino materials/images/Dino/DinoDuck1.png"),
            load_image("PythonProjects/pygame/Assets/dino materials/images/Dino/DinoDuck2.png")
        ],
        "dead": load_image("PythonProjects/pygame/Assets/dino materials/images/Dino/DinoDead.png")
    },
    "small_cactus": [
        load_image("PythonProjects/pygame/Assets/dino materials/images/Cactus/SmallCactus1.png"),
        load_image("PythonProjects/pygame/Assets/dino materials/images/Cactus/SmallCactus2.png"),
        load_image("PythonProjects/pygame/Assets/dino materials/images/Cactus/SmallCactus3.png")
    ],
    "large_cactus": [
        load_image("PythonProjects/pygame/Assets/dino materials/images/Cactus/LargeCactus1.png"),
        load_image("PythonProjects/pygame/Assets/dino materials/images/Cactus/LargeCactus2.png"),
        load_image("PythonProjects/pygame/Assets/dino materials/images/Cactus/LargeCactus3.png")
    ],
    "bird": [
        load_image("PythonProjects/pygame/Assets/dino materials/images/Birds/Bird1.png"),
        load_image("PythonProjects/pygame/Assets/dino materials/images/Birds/Bird2.png")
    ],
    "cloud": load_image("PythonProjects/pygame/Assets/dino materials/images/Other/Cloud.png"),
    "base": load_image("PythonProjects/pygame/Assets/dino materials/images/Other/Track.png"),
    "game_over": load_image("PythonProjects/pygame/Assets/dino materials/images/Other/GameOver.png")
}

# Sounds
game_sounds = {
    "jump": pygame.mixer.Sound("PythonProjects/pygame/Assets/dino materials/sounds/jump.mp3"),
    "die": pygame.mixer.Sound("PythonProjects/pygame/Assets/dino materials/sounds/die.mp3")
}

# 🦖 Dino
class Dino:
    def __init__(self):
        self.x = 80
        self.run_y = 310
        self.duck_y = 340

        self.vel_y = 0
        self.gravity = 1

        self.is_jump = False
        self.is_duck = False

        self.step_index = 0

        self.image = game_images["dino"]["running"][0]
        self.rect = self.image.get_rect(topleft=(self.x, self.run_y))

    def update(self, keys):

        # Jump
        if keys[pygame.K_SPACE] and not self.is_jump:
            self.is_jump = True
            self.vel_y = -20
            game_sounds["jump"].play()

        # Duck
        if keys[pygame.K_DOWN] and not self.is_jump:
            self.is_duck = True
        else:
            self.is_duck = False

        # Jump physics
        if self.is_jump:
            self.vel_y += self.gravity
            self.rect.y += self.vel_y

            if self.rect.y >= self.run_y:
                self.rect.y = self.run_y
                self.is_jump = False

        # Animation
        self.step_index += 1
        if self.step_index >= 10:
            self.step_index = 0

        # State handling
        if self.is_jump:
            self.image = game_images["dino"]["jumping"]

        elif self.is_duck:
            self.image = game_images["dino"]["ducking"][self.step_index // 5]
            self.rect.y = self.duck_y

        else:
            self.image = game_images["dino"]["running"][self.step_index // 5]
            self.rect.y = self.run_y

        # Fix hitbox
        self.rect = self.image.get_rect(topleft=(self.x, self.rect.y))

    def draw(self):
        SCREEN.blit(self.image, self.rect)


# 🌵 Obstacles
class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def spawn(self):
        choice = random.randint(0, 2)

        if choice == 0:
            img = random.choice(game_images["small_cactus"])
            y = 325
        elif choice == 1:
            img = random.choice(game_images["large_cactus"])
            y = 300
        else:
            img = random.choice(game_images["bird"])
            y = random.choice([250, 300])  # duck or jump logic

        rect = img.get_rect()
        rect.x = screenWidth
        rect.y = y

        self.obstacles.append((img, rect))

    def update(self, speed):
        for obs in self.obstacles:
            obs[1].x -= speed

        self.obstacles = [obs for obs in self.obstacles if obs[1].x > -50]

    def draw(self):
        for img, rect in self.obstacles:
            SCREEN.blit(img, rect)


# ☁️ Cloud
class Cloud:
    def __init__(self):
        self.x = screenWidth
        self.y = random.randint(50, 100)
        self.image = game_images["cloud"]

    def update(self, speed):
        self.x -= speed // 2
        if self.x < -100:
            self.x = screenWidth
            self.y = random.randint(50, 100)

    def draw(self):
        SCREEN.blit(self.image, (self.x, self.y))


# 🎮 Game
class DinoGame:
    def __init__(self):
        self.running = False
        self.game_over = False
        self.score = 0
        self.speed = 10

        self.font = pygame.font.SysFont("Arial", 25)

    def main_menu(self):
        while True:
            SCREEN.fill((255, 255, 255))

            text = self.font.render("Press SPACE to Start", True, (0, 0, 0))
            SCREEN.blit(text, (400, 250))
            SCREEN.blit(game_images["dino"]["start"], (500, 300))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.running = True
                        return

            pygame.display.update()
            clock.tick(FPS)

    def run_game(self):
        player = Dino()
        obstacles = ObstacleManager()
        cloud = Cloud()

        spawn_timer = 0

        while self.running:
            SCREEN.fill((255, 255, 255))
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            player.update(keys)
            player.draw()

            spawn_timer += 1
            if spawn_timer > 60:
                obstacles.spawn()
                spawn_timer = 0

            obstacles.update(self.speed)
            obstacles.draw()

            for img, rect in obstacles.obstacles:
                if player.rect.colliderect(rect):
                    game_sounds["die"].play()
                    pygame.time.delay(500)
                    self.running = False
                    self.game_over = True

            cloud.update(self.speed)
            cloud.draw()

            self.score += 1
            if self.score % 100 == 0:
                self.speed += 1

            score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
            SCREEN.blit(score_text, (screenWidth - 200, 50))

            SCREEN.blit(game_images["base"], (0, 380))

            pygame.display.update()
            clock.tick(FPS)

    def end_screen(self):
        while self.game_over:
            SCREEN.fill((255, 255, 255))

            text = self.font.render("Game Over! Press SPACE to Restart", True, (0, 0, 0))
            SCREEN.blit(text, (300, 250))

            score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
            SCREEN.blit(score_text, (500, 300))

            SCREEN.blit(game_images["dino"]["dead"], (500, 350))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.__init__()
                        return

            pygame.display.update()
            clock.tick(FPS)


# 🚀 Run
game = DinoGame()

while True:
    game.main_menu()
    game.run_game()
    game.end_screen()