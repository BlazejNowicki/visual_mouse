from HandRecognitionModule import HandRecognition
import pyautogui as ag
import cv2 as cv
from math import sqrt


def dist(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def operate_mouse(data_points, frame):
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
    if dist(index_finger, center) < 50:
        inside_color = secondary_color
        index_finger_in_center = True
    elif dist(index_finger, center) < 150:
        outside_color = secondary_color

    cv.circle(frame, (image_width // 2, image_height // 2), 50, inside_color, thickness=thickness)
    cv.circle(frame, (image_width // 2, image_height // 2), 150, outside_color, thickness=thickness)

    # Detect right click
    right_click = False
    index_knuckle = first_hand[5][:2]
    index_knuckle = [image_width * index_knuckle[0], image_height * index_knuckle[1]]
    middle_finger = first_hand[12][:2]
    middle_finger = [image_width * middle_finger[0], image_height * middle_finger[1]]
    if dist(middle_finger, index_knuckle) < dist(middle_finger, index_finger) and index_finger_in_center:
        right_click = True
    
    if right_click:
        cv.circle(frame, (50,50), 10, accent_color, cv.FILLED)

def main():
    webcam = cv.VideoCapture(0)
    hand_rec = HandRecognition()
    while webcam.isOpened():
        success, frame = webcam.read()
        frame = cv.flip(frame, 1)
        if not success:
            print("Unable to read video frame")
            continue
        data_points, frame = hand_rec.detect_hands(frame, print_image=False, flip_image=False)
        # print(data_points)

        if data_points:
            operate_mouse(data_points, frame)

        cv.imshow("Visual Mouse", frame)
        cv.waitKey(1)

if __name__ == "__main__":
    main()