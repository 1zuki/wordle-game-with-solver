import pygame
import Logic
import Solver
import time

## game UI n back end
SCREEN_SIZE = (1024, 1024)
LETTER_COLOR = (255, 255, 255)

START_X = 194
START_Y = 124
OFFSET_X = 103.5
OFFSET_Y = 104.4
SIZE = 94

# wordle feed back color
WRONG = (65, 65, 67)
WRONG_POS = (182, 161, 66)
CORRECT = (83, 138, 78)

# game
class wordleGame:
    def __init__(self, solver = None, solver_visual = False, solver_speed = False):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 110)

        self.background = pygame.image.load("/home/izu/Izu/Projects/wordle-game/assets/background.png")

        self.solver = solver
        self.sol_visual = solver_visual
        self.sol_speed = solver_speed

        self.reset()

    def reset(self):
        self.answer = Logic.choose_word()
        self.choices = []
        self.feedback = []
        self.temp = []

        self.running = True
        self.game_over = False
        
        if self.solver:
            self.solver.reset()

        print("Answer:", self.answer)

    def human_input(self, event):
        if event.key == pygame.K_BACKSPACE and self.temp:
            self.temp.pop()

        elif event.key == pygame.K_RETURN:
            self.submit_row()

        else:
            char = event.unicode

            if char.isalpha() and len(char) == 1 and len(self.temp) < 5:
                self.temp.append(char.lower())

    def solver_input(self):
        turn = len(self.choices)
        guess = self.solver.next_guess(turn)
        self.temp = list(guess)
        self.submit_row()

    def submit_row(self):
        word = "".join(self.temp)
        
        if not Logic.validate_choice(word):
            return
        
        self.choices.append(word)
        feedback = Logic.validate_ans(word, self.answer)
        self.feedback.append(feedback)

        if self.solver:
            self.solver.apply_feedback(word, feedback)

        self.temp.clear()

        if Logic.is_won(feedback):
            self.game_over = True

        if len(self.choices) >= 6:
            self.game_over = True

    def render(self):
        self.screen.blit(self.background, (0, 0))

        # choices
        for oy, word in enumerate(self.choices):
            for ox in range(5):
                dx = int(START_X + OFFSET_X * ox)
                dy = int(START_Y + OFFSET_Y * oy)

                feedback = self.feedback[oy][ox]

                if feedback == 1:
                    color = CORRECT

                elif feedback == 0:
                    color = WRONG_POS

                else:
                    color = WRONG

                pygame.draw.rect(self.screen, color, (dx, dy, SIZE, SIZE))

                char_x = dx + SIZE // 2
                char_y = dy + SIZE // 2

                text = self.font.render(word[ox].upper(), True, LETTER_COLOR)
                text_rect = text.get_rect()
                text_rect.center = (char_x, char_y)
                self.screen.blit(text, text_rect)
        
        # temp
        oy = len(self.choices)
        
        for ox, char in enumerate(self.temp):
            char_x = int(START_X + OFFSET_X * ox + SIZE / 2)
            char_y = int(START_Y + OFFSET_Y * oy + SIZE / 2)

            text = self.font.render(char.upper(), True, LETTER_COLOR)
            text_rect = text.get_rect()
            text_rect.center = (char_x, char_y)

            self.screen.blit(text, text_rect)

        # update screen
        pygame.display.update()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if not self.game_over and not self.sol_visual:
                    if event.type == pygame.KEYDOWN:
                        self.human_input(event)

            if not self.game_over and self.sol_visual:
                self.solver_input()

                if not self.sol_speed:
                    pygame.time.delay(15)
            
            self.render()

            if self.game_over:
                print("Won")
                self.reset()

            if not self.sol_speed:
                self.clock.tick(60)

HUMAN = "human"
SOL_VIS = "solver_visual"
SOL_SPEED = "solver_speed"

if __name__ == "__main__":
    solver = None
    MODE = HUMAN

    if MODE != HUMAN:
        with open("/home/izu/Izu/Projects/wordle-game/assets/answer-nytimes.txt") as f:
            words = [w.strip().lower() for w in f if len(w.strip()) == 5]

        solver = Solver.WordleSolver(words, Logic.validate_ans)

    game = wordleGame(
        solver = solver,
        solver_visual = (MODE != HUMAN),
        solver_speed = (MODE == SOL_SPEED)
    )

    game.run()