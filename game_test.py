from game import Game
import random as r
import time
session = Game(10,30);



# session.place_puzzle(session.board,0,[[0,1,1,0],
# 									 [0,1,1,0],
# 									 [0,0,0,0],
# 			 						 [0,0,0,0]])
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
# print(session.board)
# print(heights)
# print(session.sumPairs(heights))

while(True):
	i = r.randint(0,6)
	session.get_move(i)
	print(session.board)
	time.sleep(0.2)