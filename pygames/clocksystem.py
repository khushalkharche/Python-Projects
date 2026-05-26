from datetime import datetime
import pygame

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

info = pygame.display.Info()
screenWidth, screenHeight = info.current_w, info.current_h
screen = pygame.display.set_mode((screenWidth, screenHeight))

alarm_sound = pygame.mixer.Sound("PythonProjects/pygame/Assets/clock materials/alarm.mp3")

pygame.display.set_caption("CLOCK SYSTEM")

# logo
image = pygame.image.load("PythonProjects/pygame/Assets/clock materials/clock.png")
pygame.display.set_icon(image)


# =========================================================
# BUTTON CLASS
# =========================================================
class Button:
    def __init__(self, index, total_buttons, screenWidth, screenHeight, text, action, y_offset=None):
        self.text = text
        self.action = action

        self.width = int(screenWidth * 0.12)
        self.height = int(screenHeight * 0.06)

        gap = int(screenWidth * 0.02)
        total_width = total_buttons * self.width + (total_buttons - 1) * gap

        start_x = (screenWidth - total_width) // 2
        y = y_offset if y_offset else int(screenHeight * 0.05)
        x = start_x + index * (self.width + gap)

        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.font = pygame.font.SysFont("Arial", 28, bold=True)

        self.base_color = (30, 41, 59)
        self.hover_color = (51, 65, 85)
        self.active_color = (0, 150, 255)

        self.text_color = (180, 180, 180)
        self.active_text_color = (255, 255, 255)

    def draw(self, screen, active_action):
        mouse_pos = pygame.mouse.get_pos()

        if self.action == active_action:
            color = self.active_color
            text_color = self.active_text_color
        elif self.rect.collidepoint(mouse_pos):
            color = self.hover_color
            text_color = (255, 255, 255)
        else:
            color = self.base_color
            text_color = self.text_color

        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
       
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return self.action
        return None

labels = ["Clock", "Alarm", "Stopwatch", "Timer"]

buttons = []
for i, label in enumerate(labels):
    btn = Button(i, len(labels), screenWidth, screenHeight, label, label.lower())
    buttons.append(btn)


# =========================================================
# CLOCK CLASS
# =========================================================
class Clock:
    def __init__(self, screenWidth, screenHeight):
        self.box_width = int(screenWidth * 0.6)
        self.box_height = int(screenHeight * 0.25)

        self.box_x = (screenWidth - self.box_width) // 2
        self.box_y = (screenHeight - self.box_height) // 2

        self.rect = pygame.Rect(self.box_x, self.box_y, self.box_width, self.box_height)

        font_size = int(screenHeight * 0.12)
        self.font = pygame.font.SysFont("Arial", font_size, bold=True)

    def draw(self, screen):
        now = datetime.now().strftime("%I:%M:%S %p")

        pygame.draw.rect(screen, (30, 30, 30), self.rect, border_radius=12)

        time_surface = self.font.render(now, True, "white")
        time_rect = time_surface.get_rect(center=self.rect.center)

        screen.blit(time_surface, time_rect)

clock = Clock(screenWidth, screenHeight)

# =========================================================
# STOPWATCH CLASS
# =========================================================
class Stopwatch:
    def __init__(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.mode = None
        self.start_time = 0
        self.elapsed_time = 0

        self.time_position = (screenWidth // 2, int(screenHeight * 0.20))

        font_size = int(screenHeight * 0.12)
        self.font = pygame.font.SysFont("Arial", font_size, bold=True)
        self.lap_font = pygame.font.SysFont("Arial", 30)

        self.laps = []

        self.start_btn = Button(
            0, 1, screenWidth, screenHeight,
            "START", "start",
            y_offset=int(screenHeight * 0.75)
        )

        labels = ["RESUME", "STOP", "RESET", "LAP"]
        self.buttons = []

        for i, label in enumerate(labels):
            btn = Button(
                i, len(labels),
                screenWidth, screenHeight,
                label, label.lower(),
                y_offset=int(screenHeight * 0.75)
            )
            self.buttons.append(btn)

        self.actions = {
            "start": self.start,
            "stop": self.stop,
            "resume": self.resume,
            "reset": self.reset,
            "lap": self.add_lap
        }

    def start(self):
        self.start_time = pygame.time.get_ticks()
        self.mode = "running"

    def stop(self):
        self.mode = "stop"

    def resume(self):
        self.start_time = pygame.time.get_ticks() - self.elapsed_time
        self.mode = "running"

    def reset(self):
        self.elapsed_time = 0
        self.laps.clear()
        self.mode = None

    def add_lap(self):
        total_ms = self.elapsed_time
        total_sec = total_ms // 1000
        ms = (total_ms % 1000) // 10

        h = total_sec // 3600
        m = (total_sec % 3600) // 60
        s = total_sec % 60

        lap_time = f"{h:02}:{m:02}:{s:02}:{ms:02}"
        self.laps.append(lap_time)

    def update(self):
        if self.mode == "running":
            self.elapsed_time = pygame.time.get_ticks() - self.start_time

    def layout_buttons(self, buttons):
        count = len(buttons)

        btn_width = int(self.screenWidth * 0.12)
        btn_height = int(self.screenHeight * 0.06)
        gap = int(self.screenWidth * 0.02)

        total_width = count * btn_width + (count - 1) * gap

        start_x = (self.screenWidth - total_width) // 2
        y = int(self.screenHeight * 0.75)

        for i, btn in enumerate(buttons):
            x = start_x + i * (btn_width + gap)
            btn.rect = pygame.Rect(x, y, btn_width, btn_height)

    def draw(self, screen):
        total_ms = self.elapsed_time
        total_sec = total_ms // 1000
        ms = (total_ms % 1000) // 10

        h = total_sec // 3600
        m = (total_sec % 3600) // 60
        s = total_sec % 60

        time_str = f"{h:02}:{m:02}:{s:02}:{ms:02}"

        time_surface = self.font.render(time_str, True, "white")
        time_rect = time_surface.get_rect(center=self.time_position)
        screen.blit(time_surface, time_rect)

        if self.mode is None:
            active_buttons = [self.start_btn]

        elif self.mode == "running":
            active_buttons = [
                btn for btn in self.buttons
                if btn.action in ["stop", "reset", "lap"]
            ]

        elif self.mode == "stop":
            active_buttons = [
                btn for btn in self.buttons
                if btn.action in ["resume", "reset", "lap"]
            ]

        self.layout_buttons(active_buttons)

        for btn in active_buttons:
            btn.draw(screen, None)

        start_y = int(self.time_position[1] + 100)

        for i, lap in enumerate(self.laps[-5:]):
            lap_text = f"Lap {len(self.laps)-len(self.laps[-5:])+i+1}: {lap}"
            lap_surface = self.lap_font.render(lap_text, True, "white")
            screen.blit(lap_surface, (50, start_y + i * 40))

    def handle_event(self, event):

        if self.mode is None:
            action = self.start_btn.handle_event(event)
            if action:
                self.actions[action]()
                return

        for btn in self.buttons:
            action = btn.handle_event(event)
            if not action:
                continue
            if self.mode == "running" and action == "resume":
                continue
            if self.mode == "stop" and action == "stop":
                continue
            if action in self.actions:
                self.actions[action]()
                return

stopwatch = Stopwatch(screenWidth, screenHeight)

# =========================================================
# TIMER CLASS 
# =========================================================
class Timer:
    def __init__(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.input_box = pygame.Rect(screenWidth//2 - 200, screenHeight//2 - 50, 400, 60)
        self.font = pygame.font.SysFont("Arial", 40)

        self.input_text = ""
        self.active = False

        self.start_time = None
        self.duration = 0
        self.running = False

    def draw(self, screen):
        pygame.draw.rect(screen, (50, 50, 50), self.input_box, border_radius=10)

        text_surface = self.font.render(self.input_text, True, "white")
        screen.blit(text_surface, (self.input_box.x + 10, self.input_box.y + 10))

        inst = self.font.render("Enter Seconds", True, "white")
        screen.blit(inst, (self.screenWidth//2 - 150, self.screenHeight//2 - 120))

        # Countdown
        if self.running:
            elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
            remaining = max(0, self.duration - elapsed)

            time_str = str(remaining)
            time_surface = self.font.render(time_str, True, "white")
            screen.blit(time_surface, (self.screenWidth//2 - 50, self.screenHeight//2 + 80))

            if remaining == 0:
                alarm_sound.play()
                self.running = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.input_box.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                try:
                    self.duration = int(self.input_text)
                    self.start_time = pygame.time.get_ticks()
                    self.running = True
                    self.input_text = ""
                except:
                    self.input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                if event.unicode.isdigit():
                    self.input_text += event.unicode

        

timer = Timer(screenWidth, screenHeight)
# =========================================================
# ALARM CLASS
# =========================================================
class Alarm:
    def __init__(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.input_box = pygame.Rect(screenWidth//2 - 200, screenHeight//2 - 50, 400, 60)
        self.font = pygame.font.SysFont("Arial", 40)

        self.input_text = ""
        self.active = False
        self.alarm_time = None
        self.triggered = False

    def draw(self, screen):
        # Input box
        pygame.draw.rect(screen, (50, 50, 50), self.input_box, border_radius=10)

        text_surface = self.font.render(self.input_text, True, "white")
        screen.blit(text_surface, (self.input_box.x + 10, self.input_box.y + 10))

        # Instructions
        inst = self.font.render("Enter Time (HH:MM:SS)", True, "white")
        screen.blit(inst, (self.screenWidth//2 - 200, self.screenHeight//2 - 120))

        # Check alarm
        if self.alarm_time and not self.triggered:
            now = datetime.now().strftime("%H:%M:%S")
            if now == self.alarm_time:
                alarm_sound.play()
                self.triggered = True

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.input_box.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.alarm_time = self.input_text
                self.input_text = ""
                self.triggered = False
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                self.input_text += event.unicode

alarm = Alarm(screenWidth, screenHeight)

mode = "clock"
running = True
# =========================================================
# MAIN LOOP
# =========================================================
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # NAV BUTTONS
        for button in buttons:
            result = button.handle_event(event)
            if result:
                mode = result

        # STOPWATCH EVENTS
        if mode == "stopwatch":
            stopwatch.handle_event(event)
        if mode == "alarm":
            alarm.handle_event(event)
        if mode == "timer":
            timer.handle_event(event)

    # UPDATE
    if mode == "stopwatch":
        stopwatch.update()
    
    # DRAW
    screen.fill("black")

    for button in buttons:
        button.draw(screen, mode)

    if mode == "clock":
        clock.draw(screen)

    elif mode == "stopwatch":
        stopwatch.draw(screen)

    elif mode == "alarm":
        alarm.draw(screen)

    elif mode == "timer":
        timer.draw(screen)

    pygame.display.update()

pygame.quit()