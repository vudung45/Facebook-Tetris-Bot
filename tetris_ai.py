import cv2
import mss
import mss.tools
from PIL import ImageGrab
import numpy as np
from game import Game
import keyboard
import time
import pyautogui as pyg


pyg.PAUSE = 0.06
monitor = {'top': 315, 'left': 388, 'width': 180, 'height': 360}
sct = mss.mss()
ss = cv2.resize(np.array(sct.grab(monitor)),(monitor['width'],monitor['height']));

#first_piece_region = cv2.selectROI(screen_frame);
first_piece_region = (70, 0, 20, 20)
next_piece_region = (534,350, 20, 20)
gray = cv2.cvtColor(ss, cv2.COLOR_RGB2GRAY)
template = cv2.resize(cv2.imread('start.jpg',0), (100, 30));

res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
loc = np.where(res >= 0.5)
pyg.click(monitor['left'] + loc[1][0], monitor['top'] + loc[0][0])
pyg.click(monitor['left'] + loc[1][0], monitor['top'] + loc[0][0])

# #RGB
# color_to_piece = {
# 	0 : [59, 168, 199,255], #I block light blue 0
# 	1 : [212, 69, 95 ,255], #z block red 1
# 	2 : [107, 181, 59 ,255], 	#s block green 2
# 	3 : [214, 174, 68, 255], #square block yellow 3
# 	4 : [214, 120, 58, 255], # L orange 4
# 	5 : [64, 105, 197, 255], # reverse L dark blue 5
# 	6 : [187, 72, 168, 255], # t block purple 6
# 	7 : [0, 0, 0 , 255] # no-block black
# }

# BGR
color_to_piece = {
	0 : [199, 168, 59, 255], #I block light blue 0
	1 : [95, 69, 212, 255], #z block red 1
	2 : [59, 181, 107, 255], 	#s block green 2
	3 : [68, 174, 214, 255], #square block yellow 3
	4 : [58, 120, 214, 255], # L orange 4
	5 : [197, 105, 64, 255], # reverse L dark blue 5
	6 : [168, 72, 187, 255], # t block purple 6
	7 : [0, 0, 0, 255] # no-block black
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
		move[0]-= 1

	if(move[1] > 4):
		while move[1] > 4:
	 		pyg.keyDown("right")
	 		pyg.keyUp("right")
	 		move[1]-=1
	elif (move[1] < 4):
		while move[1] < 4:
			pyg.keyDown("left")
			pyg.keyUp("left")
			move[1]+=1
	pyg.keyDown("space")
	pyg.keyUp("space")

# def move_piece(move):
# 	move = list(move)
# 	while move[0] > 0:
# 		keyboard.press("up arrow");
# 		keyboard.release("up arrow");
# 		time.sleep(0.05)
# 		move[0]-= 1

# 	if(move[1] > 4):
# 		while move[1] > 4:
# 	 		keyboard.press("right arrow");
# 	 		keyboard.release("right arrow");
# 	 		time.sleep(0.05)
# 	 		move[1]-=1
# 	elif (move[1] < 4):
# 		while move[1] < 4:
# 			keyboard.press("left arrow");
# 			keyboard.release("left arrow");
# 			time.sleep(0.05)
# 			move[1]+=1
# 	keyboard.press("spacebar");
# 	keyboard.release("spacebar");
# 	time.sleep(0.05)

game_started = False
weights = [0.22568649650722883, -0.08679520494876472, \
			-0.1152727732730796, 0.15842464424735841, \
			-0.75452215909537684, -0.021586109522043928]

# weights = [0.52568649650722883, -0.08679520494876472, \
# 			-0.315272773273079, 0.15842464424735841, \
# 			-0.75452215909537684, -0.021586109522043928]

session = Game(10,40, weights)
time.sleep(4)
#time.sleep(4.5)
next_piece = 7
while(True):
	ti = time.time()
	screen_frame = cv2.resize(np.array(sct.grab(monitor)),(monitor['width'],monitor['height']));
	move = None
	x,y,w,h = first_piece_region
	input_block = screen_frame[y :y + h, x:x + w]
	avg_color = np.mean(input_block, axis=(0,1))
	block_type = match_block(avg_color)
	if(block_type != 7):
		print("block_type:" + str(block_type))
		#game_started = True
		moves = session.get_move(block_type)
		#print(moves)
		move_piece(moves)


