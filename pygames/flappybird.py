import random
import sys
import pygame
from pygame.locals import K_ESCAPE, K_RETURN, K_SPACE, K_UP, QUIT, KEYDOWN

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

info = pygame.display.Info()
screenWidth, screenHeight = info.current_w, info.current_h
screen = pygame.display.set_mode((screenWidth, screenHeight)) 
pygame.display.set_caption("FLAPPY BIRD")


FPS = 32
clock = pygame.time.Clock() 

game_images = {}
game_sounds = {}

mode = "menu"

icon = pygame.image.load("PythonProjects/pygame/Assets/flappybird materials/images/player.png")
pygame.display.set_icon(icon)

bg = pygame.image.load("PythonProjects/pygame/Assets/flappybird materials/images/background_image.png").convert()
game_images["background"] = pygame.transform.scale(bg, (screenWidth, screenHeight))

player = pygame.image.load("PythonProjects/pygame/Assets/flappybird materials/images/player.png").convert_alpha()
player_w = int(screenWidth * 0.08)
player_h = int(screenHeight * 0.12)
game_images["player"] = pygame.transform.scale(player, (player_w, player_h))

startbtn = pygame.image.load("PythonProjects/pygame/Assets/flappybird materials/images/startbtn.png").convert_alpha()
startbtn_w = int(screenWidth * 0.25)
startbtn_h = int(screenHeight * 0.12)
game_images["startbtn"] = pygame.transform.scale(startbtn, (startbtn_w, startbtn_h))

flpbird = pygame.image.load("PythonProjects/pygame/Assets/flappybird materials/images/flpbird.png").convert_alpha()
flpbird_w = int(screenWidth * 0.4)
flpbird_h = int(screenHeight * 0.15)
game_images["flpbird"] = pygame.transform.scale(flpbird, (flpbird_w, flpbird_h))

base = pygame.image.load("PythonProjects/pygame/Assets/flappybird materials/images/base.png").convert_alpha()
base_h = int(screenHeight * 0.2)
game_images["base"] = pygame.transform.scale(base, (screenWidth+100, base_h))

pipe_image = pygame.image.load("PythonProjects/pygame/Assets/flappybird materials/images/pipe.png").convert_alpha()
pipe_w = int(screenWidth * 0.1)
pipe_h = int(screenHeight * 0.6)
pipe_image = pygame.transform.scale(pipe_image, (pipe_w, pipe_h))
game_images["pipe"] =(
    pygame.transform.rotate(pipe_image, 180),
    pipe_image
)

numbers = []
for i in range(10):
    img = pygame.image.load(f"PythonProjects/pygame/Assets/flappybird materials/images/{i}.png").convert_alpha()
    img = pygame.transform.scale(img, (int(screenWidth * 0.04), int(screenHeight * 0.06)))
    numbers.append(img)
game_images["numbers"] = tuple(numbers)

game_sounds["die"] = pygame.mixer.Sound("PythonProjects/pygame/Assets/flappybird materials/sounds/die.mp3")
game_sounds["flap"] = pygame.mixer.Sound("PythonProjects/pygame/Assets/flappybird materials/sounds/flap.mp3")
game_sounds["hit"] = pygame.mixer.Sound("PythonProjects/pygame/Assets/flappybird materials/sounds/hit.mp3")
game_sounds["point"] = pygame.mixer.Sound("PythonProjects/pygame/Assets/flappybird materials/sounds/point.mp3")
game_sounds["swoosh"] = pygame.mixer.Sound("PythonProjects/pygame/Assets/flappybird materials/sounds/swoosh.mp3")


gravity = 0
velocity = 0
base_acc = 0
def menuscreen():
    global gravity, velocity,base_acc
    clock.tick(FPS)
    velocity += 0.3        
    gravity += velocity 
    if gravity > 20:
        gravity = 20
        velocity = -3
    if gravity < -20:
        gravity = -20
        velocity = 3
    
    base_acc -=25
    if base_acc<-100:
        base_acc = 0

    writtenx = int(screenWidth * 0.28)
    writteny = int(screenHeight * 0.15 + gravity)
    playerx = int(screenWidth * 0.7)
    playery = int(screenHeight * 0.2 + gravity)
    basex = 0 + base_acc
    basey = int(screenHeight * 0.8)
    startbtnx = int(screenWidth * 0.375)
    startbtny = int(screenHeight * 0.6)
    screen.blit(game_images["background"], (0, 0))
    screen.blit(game_images["base"], (basex, basey))
    screen.blit(game_images["player"], (playerx, playery))
    screen.blit(game_images["startbtn"], (startbtnx, startbtny))
    screen.blit(game_images["flpbird"], (writtenx, writteny))

def gamescreen():
    score = 0

    playerx = int(screenWidth * 0.3)
    playery = int(screenHeight * 0.5)
    basex = 0
    basey = int(screenHeight * 0.8)

    # INITIAL PIPES
    pipe1 = randompipe(None)
    pipe2 = randompipe(pipe1[0]["x"])

    upper_pipes = [pipe1[0], pipe2[0]]
    lower_pipes = [pipe1[1], pipe2[1]]

    pipevelx = -4

    playervely = -9
    playerMaxvely = 10
    playeraccy = 1
    playerflapacc = -8
    playerflapped = False

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    if playery > 0:
                        playervely = playerflapacc
                        playerflapped = True
                        game_sounds["flap"].play()

        crash = isCollide(playerx, playery, upper_pipes, lower_pipes)
        if crash:
            game_sounds["die"].play()
            return score
        
        playermidpos = playerx + game_images["player"].get_width()
        for pipe in upper_pipes:
            pipemidpos = pipe["x"] + game_images["pipe"][0].get_width() // 2
            if pipemidpos <= playermidpos < pipemidpos + 4:
                score += 1
                game_sounds["point"].play()

        
        if playervely < playerMaxvely and not playerflapped:
            playervely += playeraccy
        if playerflapped:
            playerflapped = False

        playerHeight = game_images["player"].get_height()
        playery += min(playervely, basey - playery - playerHeight)

        
        for up, low in zip(upper_pipes, lower_pipes):
            up["x"] += pipevelx
            low["x"] += pipevelx

        
        if upper_pipes[-1]["x"] < screenWidth - 300:
            last_pipe_x = upper_pipes[-1]["x"]
            pipe = randompipe(last_pipe_x)

            upper_pipes.append(pipe[0])
            lower_pipes.append(pipe[1])

       
        if upper_pipes[0]["x"] < -game_images["pipe"][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)

        
        screen.blit(game_images["background"], (0, 0))

        for up, low in zip(upper_pipes, lower_pipes):
            screen.blit(game_images["pipe"][0], (up["x"], up["y"]))
            screen.blit(game_images["pipe"][1], (low["x"], low["y"]))

        screen.blit(game_images["base"], (basex, basey))
        screen.blit(game_images["player"], (playerx, playery))

       
        my_digits = [int(x) for x in str(score)]
        width = sum(game_images["numbers"][d].get_width() for d in my_digits)

        xoffset = (screenWidth - width) // 2
        for digit in my_digits:
            screen.blit(game_images["numbers"][digit], (xoffset, screenHeight // 2))
            xoffset += game_images["numbers"][digit].get_width()

        pygame.display.update()
        clock.tick(FPS)


def isCollide(playerx, playery, upper_pipes, lower_pipes):
    player_w = game_images["player"].get_width()
    player_h = game_images["player"].get_height()

    pipe_w = game_images["pipe"][0].get_width()
    pipe_h = game_images["pipe"][0].get_height()

    basey = screenHeight - game_images["base"].get_height()

    if playery >= basey - player_h or playery <= 0:
        game_sounds["hit"].play()
        return True

    for pipe in upper_pipes:
        pipe_x = pipe["x"]
        pipe_y = pipe["y"]

        if (playerx < pipe_x + pipe_w and
            playerx + player_w > pipe_x and
            playery < pipe_y + pipe_h):
            
            game_sounds["hit"].play()

            return True
            
    for pipe in lower_pipes:
        pipe_x = pipe["x"]
        pipe_y = pipe["y"]

        if (playerx < pipe_x + pipe_w and
            playerx + player_w > pipe_x and
            playery + player_h > pipe_y):
            
            game_sounds["hit"].play()
            return True

    return False
    

    

def randompipe(last_pipe_x):
    pipeHeight = game_images["pipe"][0].get_height()
    baseHeight = game_images["base"].get_height()
    max_offset = screenHeight//4
    min_offset = screenHeight // 5
    offset  = random.randint(min_offset,max_offset)
    y2 = offset + random.randrange(0, screenHeight - baseHeight - int(1.2 * offset))

    if last_pipe_x is None:
        pipex = screenWidth + 10
    else:
        pipe_gap = random.randint(350, 500)
        pipex = last_pipe_x + pipe_gap

    y1 = pipeHeight - y2 + offset

    return [
        {"x": pipex, "y": -y1},
        {"x": pipex, "y": y2}
    ]


def endgamescreen(score):
    
    while True:
        screen.blit(game_images["background"], (0, 0))

        basey = int(screenHeight * 0.8)
        screen.blit(game_images["base"], (0, basey))

        font = pygame.font.Font(None, 80)
        text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text.get_rect(center=(screenWidth // 2, screenHeight // 3))
        screen.blit(text, text_rect)

        small_font = pygame.font.Font(None, 50)
        score_text = small_font.render(f"Score: {score}", True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(screenWidth // 2, screenHeight // 2))
        screen.blit(score_text, score_rect)

        info_font = pygame.font.Font(None, 40)
        restart_text = info_font.render("Press SPACE to Restart", True, (0, 0, 0))
        menu_text = info_font.render("Press ESC for Menu", True, (0, 0, 0))

        screen.blit(restart_text, (screenWidth // 2 - 150, screenHeight * 0.65))
        screen.blit(menu_text, (screenWidth // 2 - 140, screenHeight * 0.72))

        pygame.display.update()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    return "game"   # restart
                if event.key == K_ESCAPE:
                    return "menu"   
    

if __name__ =="__main__":

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif mode == "menu":
                    if event.key == pygame.K_RETURN:
                        mode = "game"               
        pygame.display.update()

        if mode == "menu":
            menuscreen()
        elif mode == "game":
            final_score = gamescreen()
            mode = "end_game"
        elif mode == "end_game":
            mode = endgamescreen(final_score)


        clock.tick(FPS)

    pygame.quit()