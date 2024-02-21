from games_base import DotsAndBoxes
import random

game = DotsAndBoxes(1,3)
print(game)

acts = game.actions()
while len(acts)>0:
    
    a = random.choice(acts)
    print("--------------------------------")
    print(game.player)
    game = game.transition(a)
    print(a)
    print(game.points)
    print(game)
    s = input("dd")
    acts = game.actions()
