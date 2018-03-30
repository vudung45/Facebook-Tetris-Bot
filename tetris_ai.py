import cv2
from PIL import ImageGrab
import numpy as np

screen_frame = cv2.resize(np.array(ImageGrab.grab()),(800,600));
game_region =   cv2.selectROI(screen_frame);
x , y , w , h = game_region
print((x,y,w,h))
cv2.destroyAllWindows()
while(True):
	screen_frame = cv2.resize(np.array(ImageGrab.grab()),(800,600));
	screen_frame = screen_frame[y :y + h, x:x + w]
	cv2.imshow("Captured",screen_frame)
	key = cv2.waitKey(25) & 0xFF
	if key == ord("q"):
		cv2.destroyAllWindows()
		break
