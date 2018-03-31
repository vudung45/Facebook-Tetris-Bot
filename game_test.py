from game import Game
import random as r
import time
weights = [0.22568649650722883, -0.08679520494876472, \
			-0.6152727732730796, 0.05842464424735841, \
			-0.55452215909537684, -0.021586109522043928]
session = Game(10,30, weights);


session.place_puzzle(session.board,1,[[1,1,0,0],
	         [0,1,1,0],
	         [0,0,0,0],
	         [0,0,0,0]])
# session.place_puzzle(session.board,3,[[0,1,1,0],
# 									 [0,1,1,0],
# 									 [0,0,0,0],
# 			 						 [0,0,0,0]])
# session.place_puzzle(session.board,2,[[1,1,0,0],
# 						    		 [0,1,0,0],
# 						    		 [0,1,0,0],
# 						    		 [0,0,0,0]])
# session.place_puzzle(session.board,6,[[1,1,1,1],
# 						    		 [0,0,0,0],
# 						    		 [0,0,0,0],
# 						    		 [0,0,0,0]])
# # session.place_puzzle(session.board,8,[[0,0,1,0],
# # 						    		 [0,0,1,0],
# # 						    		 [0,0,1,0],
# # 						    		 [0,0,1,0]])
# move = session.get_move(0);
# #print(move)
# #rows_cleared, session.board = session.rows_cleared(session.board);

# #print(rows_cleared)
# heights = session.all_heights(session.board)
print(session.board)
# print(heights)
# print(session.sumPairs(heights))

# while(True):
# 	i = r.randint(0,6)
# 	session.get_move(i)
# 	print(session.board)
# 	print("Num holes: "+str(session.num_holes(session.board)));
# 	heights = session.all_heights(session.board)
# 	print(heights)
# 	print("Roughness: "+str(session.sumPairs(heights)));
# 	time.sleep(0.2)