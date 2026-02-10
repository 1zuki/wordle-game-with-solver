import math
import random
from collections import Counter

# config n local vars
WRONG = -1
WRONG_POS = 0
CORRECT = 1

class SolverState:
    def __init__(self, all_words):
        self.all_words = all_words
        self.reset()

    def reset(self):
        self.greens = [None] * 5
        self.yellows = [set() for _ in range(5)]
        self.min_count = Counter()
        self.max_count = {}
        self.guessed = set()
        self.possible = self.all_words.copy()

# constraints
def update_constraints(guess, feedback, state):
    guess_count = Counter()

    for i in range(5):
        if feedback[i] in (CORRECT, WRONG_POS):
            guess_count[guess[i]] += 1

    for i in range(5):
        c = guess[i]

        if feedback[i] == CORRECT:
            state.greens[i] = c

        elif feedback[i] == WRONG_POS:
            state.yellows[i].add(c)

        elif feedback[i] == WRONG:
            if c in guess_count:
                # exists but limited
                state.max_count[c] = min(
                    state.max_count.get(c, float("inf")),
                    guess_count[c]
                )
            else:
                state.max_count[c] = 0

    for c in guess_count:
        # hes pooofed
        state.min_count[c] = max(
            state.min_count.get(c, 0),
            guess_count[c]
        )


def valid(word, state):
    for i in range(5):
        if state.greens[i] and word[i] != state.greens[i]:
            return False
        
        for c in state.yellows[i]:
            if word[i] == c:
                return False

    cnt = Counter(word)

    # min counts
    for c in state.min_count:
        if cnt[c] < state.min_count[c]:
            return False

    # max cnts
    for c in state.max_count:
        if cnt[c] > state.max_count[c]:
            return False

    return True

## logic for hard words etc _acer (r l m p n s)
# probe
def is_probe_safe(word, state):
    for c in word:
        if c in state.max_count and state.max_count[c] == 0:
            return False

    for i in range(5):
        for c in state.yellows[i]:
            if word[i] == c:
                return False

    return True

def choose_probe_word(state):
    candidates = [
        w for w in state.all_words
        if w not in state.guessed and is_probe_safe(w, state)
    ]

    unknown_positions = [
        i for i in range(5)
        if state.greens[i] is None
    ]

    letter_freq = Counter()
    for w in state.possible:
        for i in unknown_positions:
            letter_freq[w[i]] += 1

    def score(w):
        return sum(letter_freq[c] for c in set(w) if c in letter_freq)

    return max(candidates, key=score)

# entrophy to find best word
def entropy(guess, possible, feedback_fn):
    patterns = Counter()

    for answer in possible:
        fb = tuple(feedback_fn(guess, answer))
        patterns[fb] += 1

    total = len(possible)
    H = 0.0

    for count in patterns.values():
        p = count / total
        H -= p * math.log2(p)
    
    return H

def choose_entropy_word(state, feedback_fn):
    pool = state.possible if len(state.possible) < 40 else state.all_words

    best_word = None
    best_score = -1

    for w in pool:
        if w in state.guessed:
            continue
        if len(state.possible) > 100 and len(set(w)) < 5:
            continue

        score = entropy(w, state.possible, feedback_fn)

        if score > best_score:
            best_score = score
            best_word = w

    return best_word

# solver
class WordleSolver:
    def __init__(self, all_words, feedback_fn, first_guess="crane"):
        self.state = SolverState(all_words)
        self.feedback_fn = feedback_fn
        self.first_guess = first_guess

    def reset(self):
        self.state.reset()

    def next_guess(self, turn, max_turns=6):
        if turn == 0:
            guess = self.first_guess
        else:
            remaining_turns = max_turns - turn

            if len(self.state.possible) > remaining_turns:
                guess = choose_probe_word(self.state)
            else:
                guess = choose_entropy_word(self.state, self.feedback_fn)

        self.state.guessed.add(guess)
        return guess

    def apply_feedback(self, guess, feedback):
        update_constraints(guess, feedback, self.state)
        self.state.possible = [
            w for w in self.state.possible if valid(w, self.state)
        ]

# main for speed testing
if __name__ == "__main__":
    import time

    with open("/home/izu/Izu/Projects/wordle-game/assets/answer-nytimes.txt") as f:
        WORDS = [w.strip().lower() for w in f if len(w.strip()) == 5]

    from Logic import validate_ans

    solver = WordleSolver(WORDS, validate_ans)

    GAMES = 1836
    total_turns = 0
    fails = 0

    start = time.time()

    for _ in range(GAMES):
        answer = random.choice(WORDS)
        solver.reset()

        solved = False
        for turn in range(6):
            guess = solver.next_guess(turn)
            fb = validate_ans(guess, answer)
            solver.apply_feedback(guess, fb)

            if guess == answer:
                total_turns += turn + 1
                solved = True
                break

        if not solved:
            fails += 1

    elapsed = time.time() - start

    print("Games:", GAMES)
    print("Fails:", fails)
    print("Win rate:", 1 - fails / GAMES)
    print("Avg game:", GAMES / elapsed)
    print("Avg turns:", total_turns / max(1, (GAMES - fails)))
    print("Time:", elapsed, "seconds")
