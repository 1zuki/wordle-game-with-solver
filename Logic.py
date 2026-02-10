import random

WRONG = -1
CORRECT = 1
WRONG_POS = 0

with open("/home/izu/Izu/Projects/wordle-game/assets/answer-nytimes.txt") as file:
    ALL_ANS = [word.strip().lower() for word in file if len(word.strip()) == 5]

with open("/home/izu/Izu/Projects/wordle-game/assets/words.txt") as file:
    ALL_WORDS = [word.strip().lower() for word in file if len(word.strip()) == 5]

def choose_word():
    return random.choice(ALL_ANS)

def validate_choice(choice):
    if len(choice) == 5 and choice.lower() in ALL_WORDS:
        return True
    
    return False

def check_char_cnt(answer): 
    cnt = []
    cnt.append([answer[0], 1])

    for i in range(1, len(answer)):
        unique = True
        
        for j in range(len(cnt)):
            if answer[i] == cnt[j][0]:
                cnt[j][1] += 1
                unique = False
                break

        if unique:
            cnt.append([answer[i], 1])
    
    return cnt

def find_cnt(cnt, char):
    for i in cnt:
        if i[0] == char:
            return i
        
    return None

def validate_ans(choice, answer):
    cnt = check_char_cnt(answer)
    detail = [WRONG] * 5

    # correct
    for i in range(5):
        if choice[i] == answer[i]:
            detail[i] = CORRECT

            char = find_cnt(cnt, choice[i])
            char[1] -= 1

    for i in range(5):
        if detail[i] == WRONG:
            char = find_cnt(cnt, choice[i])

            if char and char[1] > 0:
                detail[i] = WRONG_POS
                char[1] -= 1

    return detail

def is_won(detail):
    changed = False

    for i in range(len(detail) - 1):
        if detail[i] != 1:
            changed = True
            break

        if detail[i] != detail[i - 1]:
            changed = True
            break

    return changed

# debug
if __name__ == "__main__":
    answer = choose_word()
    have_correct_ans = False

    print(answer)
    print(check_char_cnt(answer))

    loop = 0

    while loop < 6: # 6 tries
        choice = input()
        choice = choice.strip().lower()

        if len(choice) != 5 or not choice.isalpha() or choice not in ALL_ANS:
            print("Invalid, retype")

        else:
            check = validate_ans(choice, answer)

            print(check)

            if choice == answer:
                have_correct_ans = True
                break

            loop += 1

    if have_correct_ans:
        print("Congrats")
    else:
        print("Failed")