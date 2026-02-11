import Game
import Logic
import Solver

HUMAN = "human"
SOL_VIS = "solver_visual"
SOL_SPEED = "solver_speed"

if __name__ == "__main__":
    solver = None
    MODE = SOL_SPEED

    if MODE != HUMAN:
        with open("/home/izu/Izu/Projects/wordle-game/assets/answer-nytimes.txt") as f:
            words = [w.strip().lower() for w in f if len(w.strip()) == 5]

        solver = Solver.WordleSolver(words, Logic.validate_ans)

    game = Game.wordleGame(
        solver = solver,
        solver_visual = (MODE != HUMAN),
        solver_speed = (MODE == SOL_SPEED)
    )

    game.run()