import pygame
import cv2
import sys 

image_path = "assets/ganesh.jpeg"
music_path = "assets/bgm.mp3"
img = cv2.imread(image_path)

if img is None:
    print(f"Error , could not load '{image_path}'.")
    sys.exit()

h,w = img.shape[:2]
image_width = 700
image_height = int((h/w)*image_width)
img_resized = cv2.resize(img,(image_width,image_height), interpolation = cv2.INTER_AREA)

img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
img_blurred = cv2.GaussianBlur(img_gray, (5,5) ,0)
img_edges = cv2.Canny(img_blurred, 60, 150)
contours, _ = cv2.findContours(img_edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
colored_surface = pygame.image.frombuffer(img_rgb.tobytes(), img_rgb.shape[1::-1], "RGB")

pygame.mixer.init()
pygame.init()
display_info = pygame.display.Info()
canvas_w, canvas_h = display_info.current_w, display_info.current_h
offset_x = (canvas_w - image_width) // 2
offset_y = (canvas_h - image_height) // 2

lines_to_draw = []
for contour in contours:
    if len(contour) < 5:
        continue
    for i in range(len(contour)-1):
        pt1 = contour[i][0]
        pt2 = contour[i+1][0]
        p1 = (pt1[0] + offset_x, pt1[1] + offset_y)
        p2 = (pt2[0] + offset_x, pt2[1] + offset_y)
        lines_to_draw.append((p1, p2))
        
screen = pygame.display.set_mode((canvas_w,canvas_h),pygame.FULLSCREEN)
pygame.display.set_caption("Ganpati Bappa")
try:
    icon_image = pygame.image.load("assets/ganesh.jpeg")
    pygame.display.set_icon(icon_image)
except Exception as e:
    print("Could not load icon. Make sure 'icon.png' is in the correct folder.")
clock = pygame.time.Clock()

bg_color = (24, 27, 34)      
gold_color = (212, 155, 36) 

screen.fill(bg_color)
current_line = 0
lines_per_frame = 30
try:
    pygame.mixer.music.load(music_path) 
    pygame.mixer.music.play(loops = 1,start = 10.5) 
    pygame.mixer.music.set_volume(0.5) 
except Exception as e:
    print("Could not load music. Make sure 'bgm.mp3' is in the correct folder.")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                sys.exit()
            
    if current_line < len(lines_to_draw):
        for _ in range(lines_per_frame):
            if current_line < len(lines_to_draw):
                start_pos, end_pos = lines_to_draw[current_line]
                pygame.draw.line(screen, gold_color, start_pos, end_pos, width=2)
                current_line += 1  
    else:
        running = False      
    pygame.display.flip()
    clock.tick(30)

font = pygame.font.SysFont('georgia', 64, bold=True)
text_surface = font.render("HAPPY GANESH CHATURTHI", True, gold_color)
text_rect = text_surface.get_rect(center=(canvas_w // 2, 100))

text_alpha = 0
text_surface.set_alpha(text_alpha)

finished_bg = screen.copy()
running = True
text_fade_speed = 3  
hold_time = 0 

fade_overlay = pygame.Surface((canvas_w, canvas_h))
fade_overlay.fill((0, 0, 0)) 
fade_overlay_alpha = 0
fade_overlay.set_alpha(fade_overlay_alpha)

fade_finished = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and fade_finished:
            running = False

    if not fade_finished:
        screen.blit(finished_bg, (0, 0))
        if text_alpha < 255:
            text_alpha += text_fade_speed
            if text_alpha > 255:
                text_alpha = 255
            text_surface.set_alpha(text_alpha)
        else:
            if hold_time == 0:
                pygame.mixer.music.fadeout(2000)
            hold_time += 1

            if hold_time > 60:
                fade_overlay_alpha += 4
                if fade_overlay_alpha >= 255:
                    fade_overlay_alpha = 255
                    fade_finished = True 

                fade_overlay.set_alpha(fade_overlay_alpha)
        screen.blit(text_surface, text_rect)
        if hold_time > 60:
            screen.blit(fade_overlay, (0, 0))
    else:
        screen.fill((0, 0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()


