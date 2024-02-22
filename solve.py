from games_base import DotsAndBoxes
import random
import time
lookup = 0
# MiniMax ----------------------------
def minimax(state, depth: int, mini=float("-inf"), maxi=float("inf")): 
    global lookup
    lookup+=1
    if state.terminal():
        return state.reward() * float("inf"), None
    if depth == 0:
        return state.reward(), None

    fact = None 
    if state.player == 1:
        best = float("-inf")
        for act in state.actions():
            nmin = best # mini
            value, _ = minimax(state.transition(act), depth-1, nmin, maxi)
            if value>best:
                fact = act
                best = value
                if value>maxi:
                    return best, act
    else:
        best = float("inf")
        for act in state.actions():
            nmax = best # maxi
            value, _ = minimax(state.transition(act), depth-1, mini, nmax)
            if value<best:
                fact = act
                best = value
                if value<mini:
                    return best, act

    return best, act


game = DotsAndBoxes(3,1)
print(game)

acts = game.actions()
if True:
    while not game.terminal():
        
        lookup = 0
        #a = random.choice(acts)
        val, a = minimax(game, 3)
        print("--------------------------------")
        print(f"Expectation: {val}")
        print(game.player)
        game = game.transition(a)
        print(a)
        print(game.points)
        print(game)
        print(f"Lookup: {lookup}")
        #s = input("dd")
        time.sleep(0.5)
        acts = game.actions()
    


#vl = minimax(game, 4)
