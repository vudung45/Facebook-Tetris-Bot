
import numpy as np

blocks = {
	0 : [ #bar
			[[1,1,1,1],
			 [0,0,0,0],
			 [0,0,0,0],
			 [0,0,0,0]],

			[[0,0,1,0],
			 [0,0,1,0],
			 [0,0,1,0],
			 [0,0,1,0]],

			[[0,1,0,0],
			 [0,1,0,0],
			 [0,1,0,0],
			 [0,1,0,0]]
	],

    1 : [ #left z block
	    	[[1,1,0,0],
	         [0,0,1,1],
	         [0,0,0,0],
	         [0,0,0,0]],

	        [[0,0,1,0],
	         [0,0,1,0],
	         [0,1,0,0],
	         [0,1,0,0]],

			[[0,1,0,0],
			 [0,1,0,0],
			 [1,0,0,0],
			 [1,0,0,0]]
	],
    2 : [ # right z block
    		[[0,0,1,1],
	    	 [1,1,0,0],
	    	 [0,0,0,0],
	    	 [0,0,0,0]],

			[[0,1,0,0],
	    	 [0,1,0,0],
	    	 [0,0,1,0],
	    	 [0,0,1,0]],


	    	[[1,0,0,0],
	    	 [1,0,0,0],
	    	 [0,1,0,0],
	    	 [0,1,0,0]]
	],
    3 : [ #square block
			[[0,1,1,0],
			 [0,1,1,0],
			 [0,0,0,0],
			 [0,0,0,0]]
    ],
    4 : [ #right L block

    		[[0,0,0,1],
    		 [1,1,1,1],
    		 [0,0,0,0],
    		 [0,0,0,0]],

    		[[0,1,0,0],
    		 [0,1,0,0],
    		 [0,1,0,0],
    		 [0,1,1,0]],

    		[[1,1,1,1],
    		 [1,0,0,0],
    		 [0,0,0,0],
    		 [0,0,0,0]],

    		[[1,1,0,0],
    		 [0,1,0,0],
    		 [0,1,0,0],
    		 [0,1,0,0]]

    ],
    5 : [ #left L block

    		[[1,0,0,0],
    		 [1,1,1,1],
    		 [0,0,0,0],
    		 [0,0,0,0]],

    		[[0,1,1,0],
    		 [0,1,0,0],
    		 [0,1,0,0],
    		 [0,1,0,0]],

    		[[1,1,1,1],
    		 [0,0,0,1],
    		 [0,0,0,0],
    		 [0,0,0,0]],

    		[[0,1,0,0],
    		 [0,1,0,0],
    		 [0,1,0,0],
    		 [1,1,0,0]]

    ],
    6 : [ #t block type
    		[[0,1,0,0],
    		 [1,1,1,0],
    		 [0,0,0,0],
    		 [0,0,0,0]],

    		[[0,1,0,0],
    		 [0,1,1,0],
    		 [0,1,0,0],
    		 [0,0,0,0]],

    		[[1,1,1,0],
    		 [0,1,0,0],
    		 [0,0,0,0],
    		 [0,0,0,0]],

    		[[0,1,0,0],
    		 [1,1,0,0],
    		 [0,1,0,0],
    		 [0,0,0,0]]
    ]
}


# image capture from Tetris facebook app
# then generate a virtual board 
class Game(object):
	def __init__(self, width, height):
		self.board = np.zeros(shape=(height + 1,width))
	
		self.saved_block = 0 #not yet implemented


	#return the best possible move, given the type of block
	def get_move(self, block):
		best_move = (0,3,0) # (form_index, x-cord, fitness)
		#iterate through all the possible form of the block
		#find the best form and position to place it
		for i, form in enumerate(blocks[block]):
			opt_move = self.find_opt_move(form) #most optimal move for this form
			#opt_move = (x_cord, fitness)
			#comparing fitness value
			if opt_move[1] > best_move[2]:
				best_move = (i, opt_move[0], opt_move[1])
		#place the puzzle
		self.place_puzzle(self.board, best_move[1], blocks[block][best_move[0]])
		return best_move


	def collides(self, board, puzzle, x, y):
		for r in range(0, len(puzzle)):
			for c in range(0, len(puzzle[0])):
				val = 0
				if y + r >= len(board) or x + c >= len(board[0]):
					val = 1
				else:
					val = board[y+r][x+c]
				if(val + puzzle[r][c] > 1):
					return True
		return False


	#return a new board
	def place_puzzle(self, n_board, x, puzzle):
		y = len(n_board) - 1
		#looping from bottom to top for efficiency
		while y > 0 and self.collides(n_board,puzzle,x,y):
			y-=1;

		#place the puzzle
		#print(y)
		for r in range(0, len(puzzle)):
			for c in range(0, len(puzzle[0])):
				if y + r < len(n_board) and x + c < len(n_board[0]):
					n_board[y+r][x+c] = n_board[y+r][x+c] + puzzle[r][c];


	#return points scored
	#also clear rows
	def rows_cleared(self,board, height = None):
		rows_to_clear = []
		r_bound = 0
		if height != None:
			r_bound = len(board) - height;

		for r in reversed(range(r_bound, len(board))):
			for c in range(0, len(board[0])):
				if(board[r][c] == 0):
					break;
				elif c == len(board[0]) - 1:
					rows_to_clear.append(r);
		np.delete(board,rows_to_clear, axis = 0);
		return len(rows_to_clear), np.delete(board,rows_to_clear, axis = 0)

	def max_height(self, board):
		for r in reversed(range(0, len(board))):
			for c in range(0, len(board[0])):
				if board[r][c] == 1:
					return len(board) - r;

		return 0;

	def all_heights(self, board):
		heights = np.zeros(shape=len(board[0]));
		for c in range(0, len(board[0])):
			for r in reversed(range(0,len(board))):
				if board[r][c] == 1:
					heights[c] = r
					break;

		return heights;

	#return the sum of all the absolute differences of all height pairs
	def sumPairs(self,arr):
		n = len(arr);
		sum = 0
		for i in range(n - 1, -1, -1):
			sum += i*arr[i] - (n-1-i) * arr[i]
		return sum
 	
 	#number of holes in the board
	def num_holes(self, board, height = None):
		holes = 0
		r_bound = 1;
		if height != None:
			r_bound = len(board) - height
		for r in reversed(range(r_bound, len(board))):
			for c in range(0, len(board[0])):
				if board[r][c] == 0 and board[r-1][c] == 1:
					holes+=1;
		return holes;
				

	#find the most optimal move for the given formation of the puzzle
	def find_opt_move(self, puzzle):
		best_position = (3,0)
		#all possible moves given the puzzle
		for x in range(0, len(self.board[0])):
			new_board = np.copy(self.board)
			self.place_puzzle(new_board, x, puzzle)
			m_height = self.max_height(new_board)
			rows_cleared , new_board = self.rows_cleared(new_board, height = m_height)
			m_height -= rows_cleared
			heights = self.all_heights(new_board)
			cumulative_height = np.sum(heights)
			relative_height = m_height - np.min(heights)
			roughness = self.sumPairs(heights)
			holes = self.num_holes(new_board,height = m_height)
			# fitness = Score = A * Sum of Heights
    		#             +  B * Number of Clears
    		#             +  C * Number of Holes 
    		#             +  D * Number of Blockades 
			fitness = rows_cleared * 0.22 + m_height * -0.87 \
			+ cumulative_height * -0.73 + relative_height * 0.178 - holes * 0.15 + roughness * -0.02
			if best_position[1] < fitness:
				best_position = (x,fitness)
		return best_position






