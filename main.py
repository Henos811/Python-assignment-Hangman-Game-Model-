import pygame
import math
import random

pygame.init()

# Screen setup
WIDTH = 1000
HEIGHT = 700
window = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Hangman Game Model')

# Colors
BG_COLOR = (255, 243, 227)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


#score global configuration
max_mistakes = 8 
wins = 0
losses = 0
difficulty = "medium"

# Button setup
BUTTON_RADIUS = 25
GAP = 15
letters = []
start_x = round((WIDTH - (BUTTON_RADIUS * 2 + GAP) * 13) / 2)
start_y = 500
A_ord = 65

for i in range(26):
    x = start_x + GAP * 2 + ((BUTTON_RADIUS * 2 + GAP) * (i % 13))
    y = start_y + ((i // 13) * (GAP + BUTTON_RADIUS * 2))
    letters.append([x, y, chr(A_ord + i), True])

# Fonts
LETTER_FONT = pygame.font.SysFont("arial", 30)
WORD_FONT = pygame.font.SysFont("comicsans", 60)
TITLE_FONT = pygame.font.SysFont("snapitc", 80)


# Word list
word_list = [
    # Easy words (length <= 6)
    "APPLE", "HOUSE", "BRICK", "TABLE", "CHAIR", "WATER", "PLANT", "FRUIT", "MONEY",
    "RIVER", "LIGHT", "SHINE", "GRACE", "CANDY", "BREAD", "SMILE", "HEART", "PRIDE",
    "COAST", "CLOUD",
    
    # Medium words (7 <= length <= 8)
    "HOSPITAL", "LIBRARY", "MONSTER", "BALANCE", "CANYONS", "DIAMOND", "HARBORS",
    "CULTURE", "STREETS", "MYSTERY", "HORIZON", "BUTTONS", "FACTORY", "JOURNEY", "VOLCANO",
    
    # Hard words (length >= 9)
    "CHOCOLATE", "ADVENTURE", "BUTTERFLY", "TELESCOPE", "CONTROLLER", "INTERNATIONAL",
    "TRANQUILITY", "PHILOSOPHY", "CIRCUMSTANCE", "SENSATIONAL", "EXPERIENCE",
    "NOTIFICATION", "CONNECTION", "DIVERSITY", "ELECTRICITY", "SUBMARINE",
    "ADRENALINE", "INVINCIBLE", "CELEBRATION"
]

# Game state
hangman_status = 0
word = ""
guessed = []


# Hangman Drawing Function 
def draw_hangman(status):
    offset_x = 50
    offset_y = 100
    
#static_drawings
    pygame.draw.line(window, BLACK, (offset_x, offset_y + 250), (offset_x + 150, offset_y + 250), 5)
    pygame.draw.line(window, BLACK, (offset_x + 75, offset_y + 250), (offset_x + 75, offset_y), 5)
    pygame.draw.line(window, BLACK, (offset_x + 75, offset_y), (offset_x + 175, offset_y), 5)         
# for each mistake draw the hang man
    if status >= 1:
        start_point = (offset_x + 75, offset_y + 20)  
        end_point = (offset_x + 95, offset_y)           
        pygame.draw.line(window, BLACK, start_point, end_point, 5)

    if status >= 2:
        pygame.draw.line(window, BLACK, (offset_x + 175, offset_y), (offset_x + 175, offset_y + 30), 5)

    if status >= 3:
        pygame.draw.circle(window, BLACK, (offset_x + 175, offset_y + 30 + 25), 25, 5)

    if status >= 4:
        pygame.draw.line(window, BLACK, (offset_x + 175, offset_y + 30 + 25 + 25), (offset_x + 175, offset_y + 30 + 25 + 90), 5)

    if status >= 5:
        pygame.draw.line(window, BLACK,
                         (offset_x + 175, offset_y + 30 + 25 + 40),
                         (offset_x + 175 - 30, offset_y + 30 + 25 + 70), 5)
    
    if status >= 6:
        pygame.draw.line(window, BLACK,
                         (offset_x + 175, offset_y + 30 + 25 + 40),
                         (offset_x + 175 + 30, offset_y + 30 + 25 + 70), 5)
        
    if status >= 7:
        pygame.draw.line(window, BLACK,
                         (offset_x + 175, offset_y + 30 + 25 + 90),
                         (offset_x + 175 - 20, offset_y + 30 + 25 + 130), 5)
    
    if status >= 8:
        pygame.draw.line(window, BLACK,
                         (offset_x + 175, offset_y + 30 + 25 + 90),
                         (offset_x + 175 + 20, offset_y + 30 + 25 + 130), 5)
        
# Drawing Game UI Elements
def draw_score():
    score_text = LETTER_FONT.render(f"Wins: {wins}  Losses: {losses}", True, BLACK)
    window.blit(score_text, (20, 20))

def draw():
    window.fill(BG_COLOR)
    draw_score()

    #title
    title_text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))
    
    #secret word display underscore or guessed
    display_word = "".join([letter if letter in guessed else "_" for letter in word])
    word_text = WORD_FONT.render(display_word, 1, BLACK)
    window.blit(word_text, (400, 250))

    #draw hangman
    draw_hangman(hangman_status)

    #letter buttons and hover effect
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for x, y, ltr, visible in letters:
        if visible:
            distance = math.hypot(mouse_x - x, mouse_y - y)
            is_hovered = (distance <= BUTTON_RADIUS)
            if is_hovered:
                pygame.draw.circle(window, BLACK, (x, y), BUTTON_RADIUS, 0)
                letter_render = LETTER_FONT.render(ltr, True, White)
            else:
                pygame.draw.circle(window, BLACK, (x, y), BUTTON_RADIUS, 3)
                letter_render = LETTER_FONT.render(ltr, True, BLACK)
                text_color = BLACK
            window.blit(letter_render, (x - letter_render.get_width() // 2, y - letter_render.get_height() // 2))
            
    pygame.display.update()

#end game display
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
