
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

			[[1,1,1,1],
			 [0,0,0,0],
			 [0,0,0,0],
			 [0,0,0,0]],

			[[0,1,0,0],
			 [0,1,0,0],
			 [0,1,0,0],
			 [0,1,0,0]]
	],

    1 : [ #left z block
	    	[[1,1,0,0],
	         [0,1,1,0],
	         [0,0,0,0],
	         [0,0,0,0]],

	        [[0,0,1,0],
	         [0,1,1,0],
	         [0,1,0,0],
	         [0,0,0,0]],

	        [[1,1,0,0],
	         [0,1,1,0],
	         [0,0,0,0],
	         [0,0,0,0]],

			[[0,1,0,0],
			 [1,1,0,0],
			 [1,0,0,0],
			 [0,0,0,0]]
	],
    2 : [ # s block
    		[[0,1,1,0],
	    	 [1,1,0,0],
	    	 [0,0,0,0],
	    	 [0,0,0,0]],

			[[0,1,0,0],
	    	 [0,1,1,0],
	    	 [0,0,1,0],
	    	 [0,0,0,0]],

	    	[[0,0,1,1],
	    	 [0,1,1,0],
	    	 [0,0,0,0],
	    	 [0,0,0,0]],


	    	[[1,0,0,0],
	    	 [1,1,0,0],
	    	 [0,1,0,0],
	    	 [0,0,0,0]]
	],
    3 : [ #square block
			[[0,1,1,0],
			 [0,1,1,0],
			 [0,0,0,0],
			 [0,0,0,0]]
    ],
    4 : [ #right L block

    		[[0,0,1,0],
    		 [1,1,1,0],
    		 [0,0,0,0],
    		 [0,0,0,0]],

    		[[0,1,0,0],
    		 [0,1,0,0],
    		 [0,1,1,0],
    		 [0,0,0,0]],

    		[[1,1,1,0],
    		 [1,0,0,0],
    		 [0,0,0,0],
    		 [0,0,0,0]],

    		[[1,1,0,0],
    		 [0,1,0,0],
    		 [0,1,0,0],
    		 [0,0,0,0]]

    ],
    5 : [ #left L block

    		[[1,0,0,0],
    		 [1,1,1,0],
    		 [0,0,0,0],
    		 [0,0,0,0]],

    		[[0,1,1,0],
    		 [0,1,0,0],
    		 [0,1,0,0],
    		 [0,0,0,0]],

    		[[1,1,1,0],
    		 [0,0,1,0],
    		 [0,0,0,0],
    		 [0,0,0,0]],

    		[[0,1,0,0],
    		 [0,1,0,0],
    		 [1,1,0,0],
    		 [0,0,0,0]]

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
	def __init__(self, width, height, weights):
		self.board = np.zeros(shape=(height,width + 2), dtype='uint32')

		self.weights = weights
		for i in range(0,height):
			self.board[i][0] = 1
			self.board[i][width+1] = 1
		self.saved_block = 0 #not yet implemented


	#return the best possible move, given the type of block
	def get_move(self, block):
		best_move = (0, 3, -9999999) # (form_index, x-cord, fitness)
		new_board = None
		#iterate through all the possible form of the block
		#find the best form and position to place it
		for i, form in enumerate(blocks[block]):
			opt_move, opt_board = self.find_opt_move(form) #most optimal move for this form
			#opt_move = (x_cord, fitness)
			#comparing fitness value
			if opt_move[1] > best_move[2]:
				best_move = (i, opt_move[0], opt_move[1])
				new_board = opt_board
		if new_board is not None:
			self.board  = new_board

		return best_move


	def collides(self, board, puzzle, x, y):
		for r in range(0, len(puzzle)):
			for c in range(0, len(puzzle[0])):
				val = 0
				#if out of bound then just give it a virtual "" 
				if y + r >= len(board) or x + c >= len(board[0]):
					val = 1
				else:
					val = board[y+r][x+c]
				if(val + puzzle[r][c] > 1):
					return True
		return False


	#return a new board
	def place_puzzle(self, n_board, x, puzzle):
		y = 1
		#looping from bottom to top for efficiency
		while y < len(n_board) and not self.collides(n_board,puzzle,x,y):
			y+=1;

		y -= 1
		for r in range(0, len(puzzle)):
			for c in range(0, len(puzzle[0])):
				row = min(y+r, len(n_board) - 1)
				col = min(x+c, len(n_board[0]) - 1)

				n_board[row][col] = n_board[row][col] + puzzle[r][c];


	#return points scored
	#also clear rows
	def rows_cleared(self,board, height = None):
		rows_to_clear = []
		r_bound = 1
		if height != None:
			r_bound = len(board) - height;

		for r in reversed(range(r_bound, len(board))):
			for c in range(0, len(board[0] - 1)):
				if(board[r][c] == 0):
					break;
				elif c == len(board[0]) - 1:
					rows_to_clear.append(r);

		stack = np.zeros(shape=(len(rows_to_clear),len(board[0])), dtype='uint8')
		for i in range(0,len(rows_to_clear)):
			stack[i][0] = 1
			stack[i][len(stack[0]) - 1] = 1
		new_board = np.vstack([stack,np.delete(board,rows_to_clear, axis = 0)])
		return len(rows_to_clear), new_board

	def max_height(self, board):
		for r in range(0, len(board)):
			for c in range(1, len(board[0]) - 1):
				if board[r][c] >= 1:
					return len(board) - r;

		return 0;

	def all_heights(self, board):
		heights = np.zeros(shape=len(board[0]) - 2, dtype='int32');
		for c in range(1, len(board[0])- 1):
			for r in range(0,len(board)):
				if board[r][c] >= 1:
					heights[c - 1] = len(board) - r;
					break;
		return heights;

	#return the sum of all the absolute differences of all height pairs
	def sumPairs(self,arr):
		sum = 0
		for i in range(0, len(arr) - 1):
			sum += abs(arr[i] - arr[i+1])
		return sum

	def roughness_2(self,arr):
		sum = 0
		arr = sorted(arr)
		n = len(arr)
		for i in range(n - 1, -1, -1):
			sum += i*arr[i] - (n-1-i) * arr[i]
		return sum
 	
 	#number of holes in the board
	def num_holes(self, board, height = None, heights = None):
		holes = 0
		r_bound = 1;
		if height != None:
			r_bound = len(board) - height
		if heights is None:
			heights = self.all_heights(board)
		for r in reversed(range(r_bound, len(board))):
			for c in range(1, len(board[0]) - 1):
				if board[r][c] == 0 and len(board) - r < heights[c - 1]:
					holes+=1;
		return holes;

				

	#find the most optimal move for the given formation of the puzzle
	def find_opt_move(self, puzzle):
		best_position, best_board = (3, -99999), None
		for x in range(0, len(self.board[0])):
			if not self.collides(self.board,puzzle,x,0):
				new_board = np.copy(self.board)
				self.place_puzzle(new_board, x, puzzle)
				m_height = self.max_height(new_board)
				rows_cleared, new_board = self.rows_cleared(new_board, height = m_height)
				m_height -= rows_cleared
				weighted_height = pow(m_height,1.5)
				heights = self.all_heights(new_board)
				cumulative_height = np.sum(heights)
				relative_height = m_height - np.min(heights)
				roughness = self.sumPairs(heights)
				holes = self.num_holes(new_board, height = m_height, heights = heights)
				# fitness = Score = A * Sum of Heights
	    		#             +  B * Number of Clears
	    		#             +  C * Number of Holes 
	    		#             +  D * Number of Blockades 
				fitness = rows_cleared * self.weights[0]+ weighted_height * self.weights[1] \
						+ cumulative_height * self.weights[2]  + relative_height * self.weights[3] \
						+ holes * self.weights[4]  + roughness * self.weights[5]
				if best_position[1] < fitness:
					best_position = (x,fitness)
					best_board = new_board
		return best_position, best_board






