import cv2
from PIL import ImageGrab
import numpy as np
from game import Game
import time
import pyautogui as pyg
import keyboard
ss = ImageGrab.grab();

screen_frame=  cv2.resize(np.array(ss), (1680,1050))

#first_piece_region = cv2.selectROI(screen_frame);
first_piece_region = (383,402, 20, 20)
next_piece_region = (534,350, 20, 20)
gray = cv2.cvtColor(screen_frame, cv2.COLOR_RGB2GRAY)
template = cv2.resize(cv2.imread('start.jpg',0),(100,30));

res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
loc = np.where(res >= 0.5)
print(loc[1][0],loc[0][0])
pyg.click(loc[1][0],loc[0][0])
pyg.click(loc[1][0],loc[0][0])

color_to_piece = {
	0 : [59, 168, 199,255], #I block light blue 0
	1 : [212, 69, 95 ,255], #z block red 1
	2 : [107, 181, 59 ,255], 	#s block green 2
	3 : [214, 174, 68, 255], #square block yellow 3
	4 : [214, 120, 58, 255], # L orange 4
	5 : [64, 105, 197, 255], # reverse L dark blue 5
	6 : [187, 72, 168, 255], # t block purple 6
	7 : [0, 0, 0 , 255] # no-block black
}

def match_block(input_block):
	result = 7
	for block in color_to_piece:
		if np.linalg.norm(color_to_piece[block] - input_block) < np.linalg.norm(color_to_piece[result] - input_block):
			result = block
	return result


def move_piece(move):
	move = list(move)
	while move[0] > 0:
		pyg.keyDown("up")
		pyg.keyUp("up")
		time.sleep(0.02)
		move[0]-= 1

	if(move[1] > 4):
		while move[1] > 4:
	 		pyg.keyDown("right")
	 		pyg.keyUp("right")
	 		time.sleep(0.02)
	 		move[1]-=1
	else:
		while move[1] < 4:
			pyg.keyDown("left")
			pyg.keyUp("left")
			time.sleep(0.02)
			move[1]+=1
	pyg.keyDown("space")
	time.sleep(0.01)
	pyg.keyUp("space")

game_started = False

weights = [0.22568649650722883, -0.08679520494876472, \
			-0.6152727732730796, 0.05842464424735841, \
			-0.55452215909537684, -0.021586109522043928]

session = Game(10,10, weights)
time.sleep(4.2)
next_piece = 7
while(True):
	ss = ImageGrab.grab();
	screen_frame=  cv2.resize(np.array(ss), (1680,1050))
	move = None
	# if not game_started:
	x,y,w,h = first_piece_region
	input_block = screen_frame[y :y + h, x:x + w]
	avg_color = np.mean(input_block, axis=(0,1))
	block_type = match_block(avg_color)
	if(block_type != 7):
		print("block_type:" + str(block_type))
		#game_started = True
		moves = session.get_move(block_type)
		print(moves)
		move_piece(moves)
	# else:
	# 	move = session.get_move(next_piece)
	# 	print(move)

	# if game_started:
	# 	x,y,w,h = next_piece_region
	# 	nput_block = screen_frame[y :y + h, x:x + w]
	# 	avg_color = np.mean(input_block, axis=(0,1))
	# 	block_type = match_block(avg_color)
	# 	if(block_type != 7):
	# 		print("next_piece:" + str(block_type))
	# 		next_piece = block_type


