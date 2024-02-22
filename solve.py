from games_base import DotsAndBoxes
import random
import time

game = DotsAndBoxes(5,5)
print(game)

acts = game.actions()
while not game.terminal():
    
    a = random.choice(acts)
    print("--------------------------------")
    print(game.player)
    game = game.transition(a)
    print(a)
    print(game.points)
    print(game)
    #s = input("dd")
    time.sleep(0.5)
    acts = game.actions()



# MiniMax ----------------------------
def minimax(state, direct): 
    return 0


