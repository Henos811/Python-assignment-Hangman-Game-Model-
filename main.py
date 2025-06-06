import pygame
import math
import random
import time

pygame.init()

# Screen setup
WIDTH = 1500
HEIGHT = 700
window = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Hangman Game Model')

# Colors
BG_COLOR = (255, 243, 227)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

#score global configuration
max_mistakes = 8 
wins = 0
losses = 0
difficulty = "medium"

# Timer configuration
timer_limits = {
    "easy": 180,    # 3 minutes
    "medium": 120,  # 2 minutes
    "hard": 90      # 1.5 minutes
}

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
LETTER_FONT = pygame.font.SysFont("tahoma", 30)
WORD_FONT = pygame.font.SysFont("comicsans", 60)
TITLE_FONT = pygame.font.SysFont("snapitc", 80)
TIMER_FONT = pygame.font.SysFont("arial", 40, bold=True)

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
    "ABUNDANTLY","ACHIEVEMENT","ACTIVATION","ADORATIONS","AMBIGUOUSLY","ATTRACTION","BEAUTIFULLY",
    "BREATHTAKING","BRILLIANTLY","CELEBRATION", "CHALLENGED","CHALLENGER", "CIRCULATION","COMPELLING", "CONFLICTED",
    "CONVERGENCE", "CONVICTION", "COURAGEOUS", "CREATIVELY", "DAZZLINGLY", "DEFICIENCY", "DELIGHTFUL", "DEMOCRATIC", "DESPERATION", "DETERMINED", "DEVELOPMENT", "DEVASTATION", "DISCOVERIES", "DISTRACTION",
    "DRAMATICALLY","EFFICIENCY","ELOQUENTLY","ENTHUSIASM","EXCELLENCE","EXCURSIONS","EXPEDITION","EXPLOSIVELY","EXTRAVAGANT","FASCINATING","FEASIBILITY","FLOURISHING","FORTUNATELY",
    "FRIENDSHIP","FRIGHTENING","FULFILLMENT", "GENERATION", "GRATEFULLY", "HEARTWARMING", "INCREDIBLE", "INFLUENTIAL", "INNOVATION", "INQUISITIVE", "INSPIRATION", "INTELLIGENT", "INTRICACIES",
    "INTRIGUING", "IRRESISTIBLE","JUSTIFIABLE","INFORMATIVE", "INTREPIDLY", "IRIDESCENT", "LUXURIANCE", "MAGNIFICENT", "MASTERPIECE", "MERCURIALLY", "METICULOUS", "MODERNISTIC",
    "MYSTERIOUS", "NONCHALANT", "NOTEWORTHY", "OPPORTUNITY", "OPTIMISTIC", "ORGANIZATION", "OVERWHELMING", "PARTICIPATE", "PASSIONATE", "PERCEPTION", "PERFECTION", "PERSPECTIVE","PHILOSOPHER",
    "PLAUSIBILITY", "PLAYFULNESS", "POLITENESS","PRACTICALITY", "PREVALENCE", "PRODUCTIVITY", "PROFICIENCY", "PROSPERITY", "QUOTATIONS", "RECEPTIVELY", "RECOGNITION",
    "REFRESHMENT", "REMINISCENT","RESILIENCE","RESOLUTION","SIGNIFICANT","STIMULATING","STRIKINGLY", "SUCCESSION","SYMMETRICAL"
]

# Game state
hangman_status = 0
word = ""
guessed = []
start_time = 0
time_limit = 0

# Timer functions
def get_remaining_time():
    elapsed = time.time() - start_time
    remaining = max(0, time_limit - elapsed)
    return remaining

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def get_timer_color(remaining_time):
    if remaining_time > time_limit * 0.5:
        return GREEN
    elif remaining_time > time_limit * 0.25:
        return ORANGE
    else:
        return RED

# Hangman Drawing Function 
def draw_hangman(status):
    offset_x = 80
    offset_y = 200
    
#static_drawings
    pygame.draw.line(window, BLACK, (offset_x, offset_y + 250), (offset_x + 150, offset_y + 250), 5)
    pygame.draw.line(window, BLACK, (offset_x + 75, offset_y + 250), (offset_x + 75, offset_y), 5)
    pygame.draw.line(window, BLACK, (offset_x + 75, offset_y), (offset_x + 175, offset_y), 5)     
        
# for each mistake draw the hangman
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

def draw_timer():
    remaining_time = get_remaining_time()
    time_text = format_time(remaining_time)
    timer_color = get_timer_color(remaining_time)
    
    # Draw timer background
    timer_bg_rect = pygame.Rect(1270, 40, 200, 60)
    pygame.draw.rect(window, WHITE, timer_bg_rect, border_radius=10)
    pygame.draw.rect(window, timer_color, timer_bg_rect, width=3, border_radius=10)
    
    # Draw timer text
    timer_surface = TIMER_FONT.render(f"Time: {time_text}", True, timer_color)
    timer_rect = timer_surface.get_rect(center=timer_bg_rect.center)
    window.blit(timer_surface, timer_rect)

def draw():
    window.fill(BG_COLOR)
    draw_score()
    draw_timer()

    #title
    title_text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))
    
    #secret word display underscore or guessed
    display_word = " ".join([letter if letter in guessed else "_" for letter in word])
    word_text = WORD_FONT.render(display_word, 1, BLACK)
    window.blit(word_text, ((WIDTH - word_text.get_width()) // 2, 250))

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
                letter_render = LETTER_FONT.render(ltr, True, WHITE)
            else:
                pygame.draw.circle(window, BLACK, (x, y), BUTTON_RADIUS, 3)
                letter_render = LETTER_FONT.render(ltr, True, BLACK)
                text_color = BLACK
            window.blit(letter_render, (x - letter_render.get_width() // 2, y - letter_render.get_height() // 2))
            
    pygame.display.update()

#end game display
def display_message(message, reveal_word=None, time_remaining = None):
    global wins, losses
    main_text = WORD_FONT.render(message, 1, BLACK)
    word_text = WORD_FONT.render(f"The word was: {reveal_word}", True, BLACK) if reveal_word else None
    time_text = WORD_FONT.render(f"Remaining Time: {time_remaining}", True, BLACK) if time_remaining else None
    
    button_width, button_height, gap_between = 150, 50, 30
    total_width = 3 * button_width + 2 * gap_between
    start_x_btn = WIDTH // 2 - total_width // 2

    restart_rect = pygame.Rect(start_x_btn, HEIGHT // 2 + 80, button_width, button_height)
    change_rect  = pygame.Rect(start_x_btn + button_width + gap_between, HEIGHT // 2 + 80, button_width, button_height)
    quit_rect    = pygame.Rect(start_x_btn + 2 * (button_width + gap_between), HEIGHT // 2 + 80, button_width, button_height)
    

    while True:
        window.fill(BG_COLOR)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # main message
        window.blit(main_text, (WIDTH // 2 - main_text.get_width() // 2, HEIGHT // 2 - main_text.get_height() // 2))

        # revealed word 
        if word_text:
            window.blit(word_text, (WIDTH // 2 - word_text.get_width() // 2, 100))
        
        if time_remaining:
            window.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 200))
            

        # Buttons
        restart_hover = restart_rect.collidepoint(mouse_x, mouse_y)
        change_hover  = change_rect.collidepoint(mouse_x, mouse_y)
        quit_hover = quit_rect.collidepoint(mouse_x, mouse_y)

        pygame.draw.rect(window, BLACK, restart_rect, border_radius=10, width=0 if restart_hover else 3)
        pygame.draw.rect(window, BLACK, change_rect,  border_radius=10, width=0 if change_hover else 3)
        pygame.draw.rect(window, BLACK, quit_rect, border_radius=10, width=0 if quit_hover else 3)

        restart_text = LETTER_FONT.render("Restart", 1, (255, 255, 255) if restart_hover else BLACK)
        change_text  = LETTER_FONT.render("Difficulty", True, (255,255,255) if change_hover else BLACK)
        quit_text = LETTER_FONT.render("Quit", 1, (255, 255, 255) if quit_hover else BLACK)

        window.blit(restart_text, (restart_rect.x + (restart_rect.width - restart_text.get_width()) // 2,
                                   restart_rect.y + (restart_rect.height - restart_text.get_height()) // 2))
        window.blit(change_text,  (change_rect.x + (change_rect.width - change_text.get_width()) // 2,
                                   change_rect.y + (change_rect.height - change_text.get_height()) // 2))
        window.blit(quit_text, (quit_rect.x + (quit_rect.width - quit_text.get_width()) // 2,
                                quit_rect.y + (quit_rect.height - quit_text.get_height()) // 2))

        
        pygame.display.update()
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    return "restart"
                elif change_rect.collidepoint(event.pos):
                    return "change"
                elif quit_rect.collidepoint(event.pos):
                    return "quit"

#Difficulty
def main_menu():
    selecting = True
    while selecting:
        window.fill(BG_COLOR)
        game_title = TITLE_FONT.render("HANGMAN GAME", True, BLACK)
        window.blit(game_title, (WIDTH // 2 - game_title.get_width() // 2, 20))
        menu_title = WORD_FONT.render("Select Word Complexity", True, BLACK)
        window.blit(menu_title, (WIDTH // 2 - menu_title.get_width() // 2, 200))
        
        # Display timer information for each difficulty
        timer_info = LETTER_FONT.render("Timer Limits:", True, BLACK)
        window.blit(timer_info, ((WIDTH // 2 - timer_info.get_width() // 2) + 30, 450))
        
        easy_info = LETTER_FONT.render("Easy: 3:00", True, BLACK)
        medium_info = LETTER_FONT.render("Medium: 2:00", True, BLACK)
        hard_info = LETTER_FONT.render("Hard: 1:30", True, BLACK)
        
        window.blit(easy_info, (WIDTH // 2 - 230 + 75 - easy_info.get_width() // 2, 500))
        window.blit(medium_info, (WIDTH // 2 + 25 - medium_info.get_width() // 2, 500))
        window.blit(hard_info, (WIDTH // 2 + 205 - hard_info.get_width() // 2, 500))
        
        easy_rect   = pygame.Rect(WIDTH // 2 - 230, 360, 150, 50)
        medium_rect = pygame.Rect(WIDTH // 2 - 50, 360, 150, 50)
        hard_rect   = pygame.Rect(WIDTH // 2 + 130, 360, 150, 50)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for rect, text in [(easy_rect, "Easy"), (medium_rect, "Medium"), (hard_rect, "Hard")]:
            hover = rect.collidepoint(mouse_x, mouse_y)
            pygame.draw.rect(window, BLACK, rect, border_radius=10, width=0 if hover else 3)
            label = LETTER_FONT.render(text, True, (255,255,255) if hover else BLACK)
            window.blit(label, (rect.x + (rect.width - label.get_width()) // 2,
                                rect.y + (rect.height - label.get_height()) // 2))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos):
                    return "easy"
                elif medium_rect.collidepoint(event.pos):
                    return "medium"
                elif hard_rect.collidepoint(event.pos):
                    return "hard"

#Main game loop
def run_game():
    global hangman_status, guessed, word, letters, wins, losses, difficulty, start_time, time_limit

    # Reset game
    hangman_status = 0
    guessed = []
    start_time = time.time()
    time_limit = timer_limits[difficulty]

    if difficulty == "easy":
        filtered_words = [w for w in word_list if len(w) <= 6]
    elif difficulty == "medium":
        filtered_words = [w for w in word_list if 7 <= len(w) <= 8]
    elif difficulty == "hard":
        filtered_words = [w for w in word_list if len(w) >= 9 and len(w) <= 12]
    else:
        filtered_words = word_list
    
    word = random.choice(filtered_words)
    for letter in letters:
        letter[3] = True

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        # Check if time is up
        if get_remaining_time() <= 0:
            losses += 1
            result = display_message("Time's Up! You Lost.", reveal_word=word)
            return result

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if pygame.K_a <= event.key <= pygame.K_z:
                    letter_char = chr(event.key).upper()
                    if letter_char not in guessed:
                        guessed.append(letter_char)
                        if letter_char not in word:
                            hangman_status += 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                cursor_x, cursor_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.hypot(cursor_x - x, cursor_y - y)
                        if dis < BUTTON_RADIUS:
                            letter[3] = False
                            if ltr not in guessed:
                                guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

        draw()

        if set(word).issubset(set(guessed)):
            wins += 1
            remaining_time = get_remaining_time()
            time_bonus_msg = format_time(remaining_time)
            result = display_message("You Won!", reveal_word=f"{word}", time_remaining = f"{time_bonus_msg}")
            return result

        if hangman_status >= max_mistakes:
            losses += 1
            result = display_message("You Lost.", reveal_word=word)
            return result
        
def main():
    global difficulty
    selected = main_menu()
    if selected is None:
        return
    else:
        difficulty = selected
    while True:
        result = run_game()
        if result == "quit":
            break
        elif result == "change":
            new_diff = main_menu()
            if new_diff is None:
                break
            else:
                difficulty = new_diff

if __name__ == "__main__":
    main()
    pygame.quit()

print("Hangman game with timer has been created!")
print("\nTimer Features Added:")
print("- Easy: 3 minutes")
print("- Medium: 2 minutes") 
print("- Hard: 1.5 minutes")
print("- Color-coded timer (Green → Orange → Red)")
print("- Time remaining display")
print("- Game over when time runs out")
print("- Timer resets for each new game")
