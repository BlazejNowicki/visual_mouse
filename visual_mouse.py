from HandRecognitionModule import HandRecognition
import pyautogui as pag
import cv2 as cv
from math import sqrt


def dist(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def operate_mouse(data_points, frame, left_click):
    # Define colors
    primary_color = (255, 0, 0)
    secondary_color = (0, 255, 0)
    accent_color = (0, 0, 255)
    thickness = 2

    image_height, image_width, _ = frame.shape
    first_hand = data_points[0]
    index_finger = first_hand[8][:2]
    # change scale from [0, 1] to pixels
    index_finger = [image_width * index_finger[0], image_height * index_finger[1]]
    center = (image_width // 2, image_height // 2)
    # print(index_finger)

    # draw guidelines
    inside_color = outside_color = primary_color

    index_finger_in_center = False
    index_finger_in_outer_circle = False
    if dist(index_finger, center) < 50:
        inside_color = secondary_color
        index_finger_in_center = True
    if dist(index_finger, center) < 250:
        outside_color = secondary_color
        index_finger_in_outer_circle = True

    cv.circle(frame, (image_width // 2, image_height // 2), 50, inside_color, thickness=thickness)
    cv.circle(frame, (image_width // 2, image_height // 2), 250, outside_color, thickness=thickness)

    # Detect right click
    # left_click = False
    index_knuckle = first_hand[5][:2]
    index_knuckle = [image_width * index_knuckle[0], image_height * index_knuckle[1]]
    middle_finger = first_hand[12][:2]
    middle_finger = [image_width * middle_finger[0], image_height * middle_finger[1]]
    
    left_click_flag = dist(middle_finger, index_knuckle) < dist(middle_finger, index_finger) and index_finger_in_center
    if left_click_flag and not left_click:
        left_click = True
        pag.leftClick()
        print("left-click")
        cv.circle(frame, (50,50), 10, accent_color, cv.FILLED)
    elif not left_click_flag and left_click:
        left_click = False

    # Moving mouse around
    # if not index_finger_in_center and index_finger_in_outer_circle:
    if index_finger_in_outer_circle:
        move_horizontally = (index_finger[0] - image_width//2) 
        move_vertically = (index_finger[1] - image_height//2) 
        # 50 to 250 px radius
        move_horizontally = 20 * ((move_horizontally)/200)**3
        move_vertically = 20 * ((move_vertically)/200)**3
        print(move_horizontally, move_vertically)
        pag.move(move_horizontally, move_vertically, _pause=False)

    return left_click



def main():
    webcam = cv.VideoCapture(0)
    hand_rec = HandRecognition()
    left_click = False
    while webcam.isOpened():
        success, frame = webcam.read()
        frame = cv.flip(frame, 1)
        if not success:
            print("Unable to read video frame")
            continue
        data_points, frame = hand_rec.detect_hands(frame, print_image=False, flip_image=False)
        # print(data_points)

        if data_points:
            left_click = operate_mouse(data_points, frame, left_click)

        cv.imshow("Visual Mouse", frame)
        cv.waitKey(1)

if __name__ == "__main__":
    main()