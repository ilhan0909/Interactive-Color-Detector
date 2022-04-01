import cv2
import pandas as pd
import argparse
from colormap import rgb2hex

# Creating argument parser to take image path from command line
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']

# Reading the image with opencv
img = cv2.imread(args['image'])

# Declaring global variables
clicked = False
r = g = b = x_pos = y_pos = 0

# Reading csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)


# Function for calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum = 10000  # (Just to be sure of the code when trying up to 8k images)
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


# function to get x,y coordinates of mouse click
def draw_function(event, x, y, param, reg):
    if event == cv2.EVENT_LBUTTONDOWN:
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = img[y, x]

        b = int(b)
        g = int(g)
        r = int(r)


cv2.namedWindow('Interactive Color Detector')
cv2.setMouseCallback('Interactive Color Detector', draw_function)

while 1:

    cv2.imshow('Interactive Color Detector', img)
    if clicked:
        # cv2.rectangle(image, start point, end point, color, thickness) -1 fills entire rectangle
        cv2.rectangle(img, (1, 1), (705, 25), (b, g, r), -1)

        # Creating text string to display( Color name and RGB and Hex values )
        text = get_color_name(r, g, b) + ' R:' + str(r) + ' G:' + str(g) + ' B:' + str(b) + ' HexValue:' + rgb2hex(r, g, b)

        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text, (5, 20), 2, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

        # For very light colours we will display text in black colour
        if r+g+b >= 600:
            cv2.putText(img, text, (5, 20), 2, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
            
        clicked = False

    # Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break
    
cv2.destroyAllWindows()
