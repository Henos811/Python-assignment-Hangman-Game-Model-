import pygame

import math
import random

pygame.init()

# Screen setup
WIDTH = 1000
HEIGHT = 700
window = pygame.display.set_mode((WIDTH, HEIGHT))


pygame.init()
WIDTH = 1000
HEIGHT = 700
pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Hangman Game Model')

# Button setup
BUTTON_RADIUS = 25
GAP = 15
letters = []
start_x = round((WIDTH - (BUTTON_RADIUS * 2 + GAP) * 13) / 2)
start_y = 500
A = 65

for i in range(26):
    x = start_x + GAP * 2 + ((BUTTON_RADIUS * 2 + GAP) * (i % 13))
    y = start_y + ((i // 13) * (GAP + BUTTON_RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# Fonts
LETTER_FONT = pygame.font.SysFont("", 30)
WORD_FONT = pygame.font.SysFont("comicsans", 60)
TITLE_FONT = pygame.font.SysFont("snapitc", 70)


# Load images
images = []
for i in range(7):
    image = pygame.image.load("images/hangman" + str(i) + ".png")
    images.append(image)

# Word list
word_list = [
    "ELEPHANT", "SUNSHINE", "MOUNTAIN", "WATERFALL", "CHOCOLATE",
    "ADVENTURE", "BUTTERFLY", "RAINBOW", "TELESCOPE", "JOURNEY",
    "WHISPER", "VOLCANO", "GARDEN", "MYSTERY", "TREASURE",
    "OCEAN", "FIREFLY", "HARMONY", "VICTORY", "WONDER"
]

# Colors
BG_COLOR = (255, 243, 227)
BLACK = (0, 0, 0)

# Game state
hangman_status = 0
word = random.choice(word_list)
guessed = []

def draw():
    window.fill(BG_COLOR)
    
    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    window.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "

    text = WORD_FONT.render(display_word, 1, BLACK)
    window.blit(text, (400, 200))

    for letter in letters:
        x, y, ltr, visible = letter
        mouse_x, mouse_y = pygame.mouse.get_pos()

    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            distance = math.hypot(mouse_x - x, mouse_y - y)
            is_hovered = distance <= BUTTON_RADIUS

            if is_hovered:
                pygame.draw.circle(window, BLACK, (x, y), BUTTON_RADIUS)
                text_color = (255, 255, 255)
            else:
                pygame.draw.circle(window, BLACK, (x, y), BUTTON_RADIUS, 3)
                text_color = BLACK

            text = LETTER_FONT.render(ltr, 1, text_color)
            window.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    window.blit(images[hangman_status], (150, 150))
    pygame.display.update()

def display_message(message, reveal_word=None):
    main_text = WORD_FONT.render(message, 1, BLACK)
    word_text = None
    if reveal_word:
        word_text = WORD_FONT.render(f"The word was: {reveal_word}", 1, BLACK)

    restart_rect = pygame.Rect(WIDTH/2 - 150, HEIGHT/2 + 80, 130, 50)
    quit_rect = pygame.Rect(WIDTH/2 + 20, HEIGHT/2 + 80, 130, 50)
    

    while True:
        window.fill(BG_COLOR)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # main message
        window.blit(main_text, (WIDTH/2 - main_text.get_width() / 2, HEIGHT / 2 - main_text.get_height() / 2))

        # revealed word 
        if word_text:
            window.blit(word_text, (WIDTH/2 - word_text.get_width() / 2, 100))

        # Buttons
        restart_hover = restart_rect.collidepoint(mouse_x, mouse_y)
        quit_hover = quit_rect.collidepoint(mouse_x, mouse_y)

        pygame.draw.rect(window, BLACK, restart_rect, border_radius=10, width=0 if restart_hover else 3)
        pygame.draw.rect(window, BLACK, quit_rect, border_radius=10, width=0 if quit_hover else 3)

        restart_text = LETTER_FONT.render("Restart", 1, (255, 255, 255) if restart_hover else BLACK)
        quit_text = LETTER_FONT.render("Quit", 1, (255, 255, 255) if quit_hover else BLACK)

        window.blit(restart_text, (restart_rect.x + (restart_rect.width - restart_text.get_width()) / 2,
                                   restart_rect.y + (restart_rect.height - restart_text.get_height()) / 2))
        window.blit(quit_text, (quit_rect.x + (quit_rect.width - quit_text.get_width()) / 2,
                                quit_rect.y + (quit_rect.height - quit_text.get_height()) / 2))

        
        pygame.display.update()
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    return "restart"
                elif quit_rect.collidepoint(event.pos):
                    return "quit"
                


def run_game():
    global hangman_status, guessed, word, letters

    # Reset game
    hangman_status = 0
    guessed = []
    word = random.choice(word_list)
    for letter in letters:
        letter[3] = True

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                cursor_x, cursor_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - cursor_x) ** 2 + (y - cursor_y) ** 2)
                        if dis < BUTTON_RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            return display_message("You Won!", reveal_word=word)
        if hangman_status == 6:
            return display_message("You Lost.", reveal_word=word)

def main():
    while True:
        result = run_game()
        if result == "quit":
            break

main()
pygame.quit()
