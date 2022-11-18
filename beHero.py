import numpy as np, sys
import server as sv, game as g
print("Welcome to beHero")
if len(sys.argv) > 1:
    len_matrix = int(sys.argv[1])
    game = g.Game(len_matrix)
    server = sv.Server(game)

else:
    print("Se debe introducir el largo del tablero")
    sys.exit()