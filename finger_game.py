import cv2
import mediapipe as mp
import numpy as np
import pygame
import random


pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gesture Shooting Game")
clock = pygame.time.Clock()

pygame.mixer.init()
pass_sound = pygame.mixer.Sound("pass.mp3")
wow_sound = pygame.mixer.Sound("wow.mp3")
beep_sound=pygame.mixer.Sound("crash.mp3")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

REGION_WIDTH = WIDTH // 4
missile_image = pygame.image.load("missile.png").convert_alpha()
missile_image = pygame.transform.scale(missile_image, (50, 50))


enemy_size = 50
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_speed = 5





mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

def detect_finger_count(image):
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            if all(pt.x and pt.y for pt in hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP.value:]):
                return sum(1 for pt in hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP.value:]
                           if pt.y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP.value].y)
    return 0

cap = cv2.VideoCapture(0)


class GameState:
    START_MENU = 0
    IN_GAME = 1
    GAME_OVER = 2

game_state = GameState.START_MENU


def draw_start_button():
    pygame.draw.rect(screen, RED, (WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50))
    pygame.draw.polygon(screen, BLACK, [(WIDTH // 2 + 10, HEIGHT // 2), (WIDTH // 2 - 20, HEIGHT // 2 + 15), (WIDTH // 2 - 20, HEIGHT // 2 - 15)])

def draw_replay_button():
    
    pygame.draw.rect(screen, RED, (WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50))
    font = pygame.font.Font(None, 24)
    replay_text = font.render("Replay", True, BLACK)
    text_rect = replay_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(replay_text, text_rect)

running = True
score = 0
highest_score = 0
font = pygame.font.Font(None, 24)
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == GameState.START_MENU:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
                if button_rect.collidepoint(mouse_x, mouse_y):
                    game_state = GameState.IN_GAME
            elif game_state == GameState.GAME_OVER:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
                if button_rect.collidepoint(mouse_x, mouse_y):
                    game_state = GameState.IN_GAME
                    score = 0
                    enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]

    if game_state == GameState.START_MENU:
  
        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render("Play Finger Shooting", True, BLACK)
        title_text_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_text_rect)
        
  
        draw_start_button()
        
        pygame.display.flip()
        continue
    
    if game_state == GameState.IN_GAME:
        sound_played=False
        enemy_pos[1] += enemy_speed
        if enemy_pos[1] > HEIGHT:
            game_state = GameState.GAME_OVER
        

        screen.blit(missile_image, enemy_pos)

        for i in range(1, 5):
            pygame.draw.line(screen, RED, (i * REGION_WIDTH, 0), (i * REGION_WIDTH, HEIGHT), 2)
            text = font.render("Area " + str(i), True, BLACK)
            text_rect = text.get_rect(center=(i * REGION_WIDTH - REGION_WIDTH // 2, 30))
            screen.blit(text, text_rect)
        
        _, frame = cap.read()
        if frame is not None:
            if enemy_pos[0] < REGION_WIDTH:
                required_fingers = 1
            elif enemy_pos[0] < 2 * REGION_WIDTH:
                required_fingers = 2
            elif enemy_pos[0] < 3 * REGION_WIDTH:
                required_fingers = 3
            else:
                required_fingers = 4
            
            fingers_count = detect_finger_count(frame)
            if fingers_count == required_fingers:
                score += 1 
                if(score==highest_score):
                    pygame.mixer.Sound.play(wow_sound)
                else:
                    pygame.mixer.Sound.play(pass_sound)
                if score > highest_score:
                    highest_score = score  
                enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
        
            cv2.imshow('Camera', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        score_text = font.render("Score: " + str(score), True, BLACK)
        highest_score_text = font.render("Highest Score: " + str(highest_score), True, BLACK)
        screen.blit(score_text, (10, HEIGHT - 30))
        screen.blit(highest_score_text, (WIDTH - highest_score_text.get_width() - 10, HEIGHT - 30))
     
    if game_state == GameState.GAME_OVER:

        if not sound_played:
            pygame.mixer.Sound.play(beep_sound)
            sound_played=True
        # Draw game over message
        game_over_font = pygame.font.Font(None, 48)
        game_over_text = game_over_font.render("Game Over", True, BLACK)
        game_over_text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(game_over_text, game_over_text_rect)
        
    
        

        draw_replay_button()
        

        score_text = font.render("Score: " + str(score), True, BLACK)
        highest_score_text = font.render("Highest Score: " + str(highest_score), True, BLACK)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 50))
        screen.blit(highest_score_text, (WIDTH // 2 - highest_score_text.get_width() // 2, HEIGHT // 2 + 80))
        
    pygame.display.flip()
    clock.tick(30)

hands.close()
cap.release()
cv2.destroyAllWindows()
pygame.quit()
